"""
GKeepSync - NotebookLM Worker
Background worker thread that uploads local Markdown files to a NotebookLM
notebook via the `nlm` CLI. Handles source deduplication by deleting existing
sources with the same title before re-uploading.
"""

import json
import queue
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable, Optional

from utils.logger import logger

# Delay between consecutive NLM API calls to avoid rate limits (seconds).
NLM_RATE_LIMIT_DELAY = 2.5

# Path to the Python exe inside the uv-managed nlm tool environment.
# The ``nlm.exe`` shim compiled by uv allocates a Win32 console,
# causing the ``rich`` library to use the legacy Windows renderer
# which crashes on non-cp1252 characters (Vietnamese, emoji, etc).
# Calling Python directly avoids the shim's console allocation.
_UV_NLM_PYTHON = Path.home() / "AppData" / "Roaming" / "uv" / "tools" / "notebooklm-mcp-cli" / "Scripts" / "python.exe"

class NLMWorker:
    """Processes NLM upload tasks on a dedicated background thread."""

    def __init__(self):
        self._queue: queue.Queue[tuple[Path, str]] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._running = False

        # Optional callback for UI status updates.
        # func(filename: str, service: str ('keep' or 'nlm'), status: str ('pending', 'success', 'skipped', 'error'), msg: str)
        self.on_file_sync_status: Optional[Callable[[str, str, str, str], None]] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self):
        """Start the background worker thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("[NLM] Worker thread started.")

    def stop(self):
        """Signal the worker to stop after finishing its current task."""
        self._running = False
        # Put a sentinel value to unblock the queue.get()
        self._queue.put(None)  # type: ignore
        logger.info("[NLM] Worker thread stopping.")

    def enqueue(self, filepath: Path, notebook_id: str):
        """Add a file to the upload queue.

        The worker must be started via ``start()`` before enqueuing.
        """
        if not self._running:
            self.start()
        self._queue.put((filepath, notebook_id))
        logger.info("[NLM] Enqueued: %s", filepath.name)

    @property
    def pending_count(self) -> int:
        return self._queue.qsize()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _worker_loop(self):
        """Main loop – runs on the background thread."""
        logger.info("[NLM] Worker loop running.")
        while self._running:
            item = self._queue.get()
            if item is None:
                # Sentinel – time to exit.
                break
            filepath, notebook_id = item
            try:
                self._process_file(filepath, notebook_id)
            except Exception as exc:
                msg = f"[NLM] Unexpected error processing {filepath.name}: {exc}"
                logger.error(msg)
                if self.on_file_sync_status:
                    self.on_file_sync_status(filepath.name, "nlm", "error", str(exc))
            finally:
                self._queue.task_done()

    def _process_file(self, filepath: Path, notebook_id: str):
        """Delete any existing source with the same title, then upload."""
        title = filepath.stem  # e.g. "My Note" from "My Note.md"

        # --- Step 1: Get existing sources from the notebook ---
        existing_source_ids = self._find_sources_by_title(notebook_id, title)

        # --- Step 2: Delete old sources ---
        for source_id in existing_source_ids:
            logger.info("[NLM] Deleting old source %s (%s)...", source_id, title)
            self._run_nlm(
                ["nlm", "source", "delete", source_id, "--confirm"]
            )
            time.sleep(NLM_RATE_LIMIT_DELAY)

        # --- Step 3: Upload new version ---
        logger.info("[NLM] Uploading %s to notebook %s...", filepath.name, notebook_id)
        result = self._run_nlm(
            ["nlm", "source", "add", notebook_id, "--file", str(filepath)]
        )

        if result and result.returncode == 0:
            msg = f"[NLM] ✅ Uploaded: {filepath.name}"
            logger.info(msg)
            if self.on_file_sync_status:
                self.on_file_sync_status(filepath.name, "nlm", "success", "Tải lên thành công")
        else:
            stderr = result.stderr if result else "no output"
            msg = f"[NLM] ❌ Failed to upload {filepath.name}: {stderr}"
            logger.error(msg)
            if self.on_file_sync_status:
                self.on_file_sync_status(filepath.name, "nlm", "error", f"Lỗi: {stderr}")

        time.sleep(NLM_RATE_LIMIT_DELAY)

    def _find_sources_by_title(self, notebook_id: str, title: str) -> list[str]:
        """Return source IDs whose title matches the given title."""
        result = self._run_nlm(
            ["nlm", "source", "list", notebook_id, "--json"]
        )
        if not result:
            return []

        try:
            sources = self._parse_json(result.stdout)
            def _normalize_title(t: str) -> str:
                t_str = t.strip().lower()
                if t_str.endswith(".md"):
                    return t_str[:-3]
                return t_str

            target_norm = _normalize_title(title)

            # The JSON structure may be a list of dicts with "id" / "title" keys.
            matching = [
                s["id"]
                for s in sources
                if isinstance(s, dict) and _normalize_title(s.get("title", "")) == target_norm
            ]
            if matching:
                logger.info(
                    "[NLM] Found %d existing source(s) for '%s'.", len(matching), title
                )
            return matching
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.warning("[NLM] Failed to parse source list JSON: %s", exc)
            return []

    @staticmethod
    def _run_nlm(cmd: list[str]) -> Optional[subprocess.CompletedProcess]:
        """Run an nlm CLI command and return the result.

        Instead of calling ``nlm.exe`` (a uv shim that allocates a
        Win32 console), we invoke the uv-managed Python interpreter
        directly and import the CLI entry-point.  This avoids the
        ``rich`` library's legacy Windows renderer which crashes on
        non-cp1252 characters (Vietnamese, checkmarks, emoji).

        Falls back to calling ``nlm`` directly if the uv Python is
        not found (e.g. nlm was installed differently).
        """
        import os
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["NO_COLOR"] = "1"
        env["DATABRICKS_RUNTIME_VERSION"] = "1"  # Tricks rich into disabling Windows legacy render

        # Hide console window on Windows.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE

        # Build the actual command: either via uv Python or nlm.exe.
        if _UV_NLM_PYTHON.exists():
            # Translate ["nlm", "source", "add", ...] to
            # [python.exe, "-c", "from ... import cli_main; cli_main()",
            #  "source", "add", ...]
            nlm_args = cmd[1:]  # strip "nlm" prefix
            actual_cmd = [
                str(_UV_NLM_PYTHON), "-c",
                "import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8'); from notebooklm_tools.cli.main import cli_main; cli_main()",
            ] + nlm_args
        else:
            # Fallback: call nlm.exe directly (may crash on Unicode).
            actual_cmd = cmd
            logger.warning(
                "[NLM] uv Python not found at %s, falling back to nlm.exe",
                _UV_NLM_PYTHON,
            )

        try:
            return subprocess.run(
                actual_cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=120,
                check=False,
                env=env,
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except FileNotFoundError:
            logger.error(
                "[NLM] 'nlm' command not found. Is it installed? "
                "(npm install -g notebooklm-cli or uv tool install notebooklm-mcp-cli)"
            )
            return None
        except subprocess.TimeoutExpired:
            logger.error("[NLM] Command timed out: %s", " ".join(cmd))
            return None
        except Exception as exc:
            logger.error("[NLM] Error running command: %s", exc)
            return None

    @staticmethod
    def login() -> tuple[bool, str]:
        """Trigger `nlm login` browser authentication."""
        try:
            import os
            
            # Using popup console intentionally here for user browser interactions,
            # but bypassing the shim if possible.
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"
            
            if _UV_NLM_PYTHON.exists():
                actual_cmd = [
                    str(_UV_NLM_PYTHON), "-c",
                    "import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8'); from notebooklm_tools.cli.main import cli_main; cli_main()",
                    "login"
                ]
            else:
                actual_cmd = ["nlm", "login"]
            
            # Popen allows rich to output without crashing the auth flow
            proc = subprocess.Popen(
                actual_cmd,
                stdout=None,
                stderr=None,
                stdin=None,
                env=env
            )
            returncode = proc.wait(timeout=120)

            if returncode == 0:
                return True, "Login NLM thành công!"
            
            # Additional fallback check in case rich still crashed on close
            logger.warning("[NLM] login exited with code %d, verifying auth...", returncode)
            verify = NLMWorker._run_nlm(["nlm", "notebook", "list", "--json"])
            if verify and verify.returncode == 0:
                return True, "Login NLM thành công! (verified)"
            else:
                return False, f"Login thất bại (exit code {returncode})"
                
        except FileNotFoundError:
            return False, "Không tìm thấy lệnh 'nlm'. Bạn đã cài notebooklm-mcp-cli chưa?"
        except subprocess.TimeoutExpired:
            if 'proc' in locals():
                proc.kill()
            return False, "Login quá lâu (timeout 120s). Vui lòng thử lại."
        except Exception as e:
            return False, str(e)

    @staticmethod
    def check_auth_status() -> bool:
        """Check if already authenticated to NLM implicitly by fetching notebooks."""
        res = NLMWorker._run_nlm(["nlm", "notebook", "list", "--json"])
        if res and res.returncode == 0:
            return True
        return False

    @staticmethod
    def get_notebooks() -> tuple[list[dict], Optional[str]]:
        """Fetch all notebooks using `nlm notebook list --json`."""
        res = NLMWorker._run_nlm(["nlm", "notebook", "list", "--json"])
        if not res:
            return [], "Không thể chạy lệnh nlm."
        if res.returncode != 0:
            return [], f"Lỗi lấy notebook: {res.stderr}"

        try:
            # Sometime CLI outputs trailing texts or newlines, trying to parse just the JSON
            # In some variations of the script, it dumps list of dicts.
            data = NLMWorker._parse_json(res.stdout)
            if isinstance(data, list):
                return data, None
            elif isinstance(data, dict) and "notebooks" in data:
                return data["notebooks"], None
            elif isinstance(data, dict):
                return [data], None
            return [], "Format JSON không hợp lệ."
        except Exception as e:
            return [], f"Lỗi parse dữ liệu từ nlm: {e}"

    @staticmethod
    def get_sources(notebook_id: str) -> tuple[list[dict], Optional[str]]:
        """Fetch all sources for a specific notebook."""
        res = NLMWorker._run_nlm(["nlm", "source", "list", notebook_id, "--json"])
        if not res:
            return [], "Không thể chạy lệnh nlm."
        if res.returncode != 0:
            return [], f"Lỗi lấy nguồn: {res.stderr}"

        try:
            data = NLMWorker._parse_json(res.stdout)
            if isinstance(data, list):
                return data, None
            elif isinstance(data, dict) and "sources" in data:
                return data["sources"], None
            return [], "Format JSON nguồn không hợp lệ."
        except Exception as e:
            return [], f"Lỗi parse nguồn từ nlm: {e}"

    @staticmethod
    def _parse_json(text: str):
        """Extract and parse JSON from messy CLI output."""
        text = text.strip()
        # Find potential JSON start/end
        start_idx = text.find('[')
        start_dict_idx = text.find('{')
        
        # Determine which comes first
        if start_idx == -1 or (start_dict_idx != -1 and start_dict_idx < start_idx):
            start_idx = start_dict_idx
            
        if start_idx == -1:
            raise ValueError("No JSON block found in output")
            
        # Find last closing brace or bracket
        end_idx = max(text.rfind(']'), text.rfind('}'))
        
        if end_idx == -1 or end_idx < start_idx:
            raise ValueError("Incomplete JSON block in output")
            
        json_str = text[start_idx:end_idx+1]
        return json.loads(json_str)
