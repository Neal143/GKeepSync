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


class NLMWorker:
    """Processes NLM upload tasks on a dedicated background thread."""

    def __init__(self):
        self._queue: queue.Queue[tuple[Path, str]] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._running = False

        # Optional callback for UI status updates.
        self.on_upload_success: Optional[Callable[[str], None]] = None
        self.on_upload_error: Optional[Callable[[str], None]] = None

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
                if self.on_upload_error:
                    self.on_upload_error(msg)
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
            if self.on_upload_success:
                self.on_upload_success(filepath.name)
        else:
            stderr = result.stderr if result else "no output"
            msg = f"[NLM] ❌ Failed to upload {filepath.name}: {stderr}"
            logger.error(msg)
            if self.on_upload_error:
                self.on_upload_error(msg)

        time.sleep(NLM_RATE_LIMIT_DELAY)

    def _find_sources_by_title(self, notebook_id: str, title: str) -> list[str]:
        """Return source IDs whose title matches the given title."""
        result = self._run_nlm(
            ["nlm", "source", "list", notebook_id, "--json"]
        )
        if not result or result.returncode != 0:
            logger.warning("[NLM] Could not list sources for notebook %s", notebook_id)
            return []

        try:
            sources = json.loads(result.stdout)
            # The JSON structure may be a list of dicts with "id" / "title" keys.
            matching = [
                s["id"]
                for s in sources
                if s.get("title", "").strip().lower() == title.strip().lower()
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
        """Run an nlm CLI command and return the result."""
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                creationflags=subprocess.CREATE_NO_WINDOW,  # Windows: hide console
            )
        except FileNotFoundError:
            logger.error(
                "[NLM] 'nlm' command not found. Is it installed globally? "
                "(npm install -g notebooklm-cli)"
            )
            return None
        except subprocess.TimeoutExpired:
            logger.error("[NLM] Command timed out: %s", " ".join(cmd))
            return None
        except Exception as exc:
            logger.error("[NLM] Error running command: %s", exc)
            return None
