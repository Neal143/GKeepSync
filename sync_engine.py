"""
GKeepSync - Sync Engine
Sync logic: so sánh notes vs local files, tạo/cập nhật .md, auto scheduler.
"""

import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from config import Config
from keep_client import KeepClient
from utils.markdown_converter import note_to_markdown, sanitize_filename
from utils.nlm_worker import NLMWorker


class SyncEngine:
    """Handles syncing notes from Keep to local filesystem."""

    def __init__(self, keep_client: KeepClient):
        self._client = keep_client
        self._config = Config()
        self._timer: Optional[threading.Timer] = None
        self._is_syncing = False
        self._auto_sync_running = False
        self._nlm_worker = NLMWorker()

        # Callbacks
        self.on_sync_start: Optional[Callable] = None
        self.on_sync_progress: Optional[Callable[[str, int, int], None]] = None
        self.on_sync_complete: Optional[Callable[[int, int, str], None]] = None
        self.on_sync_complete: Optional[Callable[[int, int, str], None]] = None
        self.on_sync_error: Optional[Callable[[str], None]] = None
        self.on_sync_log: Optional[Callable[[str, str, str], None]] = None

    @property
    def is_syncing(self) -> bool:
        return self._is_syncing

    @property
    def is_auto_sync_running(self) -> bool:
        return self._auto_sync_running

    def sync_now(
        self,
        labels: Optional[list[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> tuple[int, int, str]:
        """
        Run sync immediately. Returns (synced_count, total_count, message).
        """
        if self._is_syncing:
            return 0, 0, "Đang sync, vui lòng đợi..."

        self._is_syncing = True
        if self.on_sync_start:
            self.on_sync_start()

        try:
            output_folder = self._config.get_output_folder()

            # --- NLM Pre-sync: Fetch all existing sources to avoid redundant uploads ---
            nlm_enabled = self._config.get("nlm_sync_enabled", False)
            nlm_nb_id = self._config.get("nlm_notebook_id", "")
            
            existing_nlm_titles = set()
            if nlm_enabled and nlm_nb_id:
                sources, error = self._nlm_worker.get_sources(nlm_nb_id)
                if not error:
                    # NLM titles are often returned with the .md extension.
                    # We strip the .md extension here to match filepath.stem later.
                    def _normalize_title(t):
                        t_str = t.strip().lower()
                        if t_str.endswith(".md"):
                            t_str = t_str[:-3]
                        return t_str

                    existing_nlm_titles = {
                        _normalize_title(s.get("title", ""))
                        for s in sources 
                        if isinstance(s, dict) and s.get("title")
                    }
                else:
                    if self.on_sync_log:
                        self.on_sync_log("NotebookLM", "warn", f"Không thể lấy danh sách nguồn: {error}")

            # Get notes from Keep
            notes = self._client.get_notes(
                labels=labels if labels else None,
                date_from=date_from,
                date_to=date_to,
            )

            total = len(notes)
            synced = 0
            updated = 0

            for i, note in enumerate(notes):
                try:
                    filepath = self._get_safe_filepath(note, output_folder)
                    title_stem = filepath.stem # Match what NLMWorker uses for title
                    
                    # Generate markdown content
                    md_content = note_to_markdown(note)

                    # Determine if we need to update local file and if we need to upload to NLM
                    should_write_file = True
                    should_upload_nlm = True
                    
                    # 1. Check local file status
                    existed_local = filepath.exists()
                    if existed_local:
                        with open(filepath, "r", encoding="utf-8") as f:
                            existing_full_content = f.read()
                        
                        if existing_full_content == md_content:
                            # Local file is identical to Keep note
                            should_write_file = False
                        else:
                            # Something changed. Check if it's just metadata (frontmatter).
                            existing_body = self._strip_frontmatter(existing_full_content)
                            current_body = self._strip_frontmatter(md_content)
                            
                            if existing_body == current_body:
                                # Only metadata changed, no need to upload to NLM
                                should_upload_nlm = False
                                if self.on_sync_log:
                                    self.on_sync_log(filepath.name, "gray", "Chỉ cập nhật metadata")
                            else:
                                updated += 1
                    
                    # 2. Check NLM status (User Criteria: upload if missing OR updated)
                    if nlm_enabled and nlm_nb_id:
                        is_on_nlm = title_stem.strip().lower() in existing_nlm_titles
                        
                        if not is_on_nlm:
                            # Criteria 1: "file chưa tồn tại trên notebook đích"
                            should_upload_nlm = True
                        elif not should_write_file:
                            # Local didn't change AND it's already on NLM
                            should_upload_nlm = False
                        # If should_write_file is True but it was ONLY metadata, 
                        # should_upload_nlm was already set to False above.
                    else:
                        should_upload_nlm = False

                    if not should_write_file:
                        synced += 1
                        if self.on_sync_progress:
                            self.on_sync_progress(note["title"], i + 1, total)
                        
                        # Even if local didn't change, we might still need to upload if it's missing from NLM
                        if nlm_enabled and nlm_nb_id and should_upload_nlm:
                            self._nlm_worker.enqueue(filepath, nlm_nb_id)
                            if self.on_sync_log:
                                self.on_sync_log(filepath.name, "gray", "Sẽ đẩy lên NotebookLM sau đó")
                        else:
                            if self.on_sync_log:
                                self.on_sync_log(filepath.name, "gray", "Đã có sẵn (không đổi)")
                        continue

                    # Write file
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(md_content)

                    synced += 1
                    
                    if self.on_sync_log:
                        self.on_sync_log(filepath.name, "success", "Đã ghi file thành công")

                    # --- NotebookLM sync ---
                    if should_upload_nlm:
                        if nlm_enabled and nlm_nb_id:
                            if is_on_nlm and not existed_local:
                                if self.on_sync_log:
                                    self.on_sync_log(filepath.name, "warn", "Thiếu file ở máy tính -> Xóa bản cũ trên NLM trước khi upload mới")
                        self._nlm_worker.enqueue(filepath, nlm_nb_id)

                    if self.on_sync_progress:
                        self.on_sync_progress(note["title"], i + 1, total)

                except Exception as e:
                    if self.on_sync_error:
                        self.on_sync_error(f"Lỗi đọc/ghi '{note['title']}': {e}")
                    if self.on_sync_log:
                        self.on_sync_log(note['title'], "error", str(e))

            # Update config
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._config.set("last_sync_time", now)
            self._config.save()

            msg = f"Đã sync {synced}/{total} notes ({updated} cập nhật)"

            if self.on_sync_complete:
                self.on_sync_complete(synced, total, msg)

            return synced, total, msg

        except Exception as e:
            error_msg = f"Lỗi sync: {e}"
            if self.on_sync_error:
                self.on_sync_error(error_msg)
            return 0, 0, error_msg
        finally:
            self._is_syncing = False

    def _strip_frontmatter(self, content: str) -> str:
        """Bỏ qua phần YAML frontmatter để chỉ so sánh nội dung chính."""
        lines = content.splitlines()
        if not lines or not lines[0].startswith("---"):
            return content
            
        # Tìm dòng "---" thứ hai
        try:
            second_sep_idx = lines.index("---", 1)
            return "\n".join(lines[second_sep_idx + 1:]).strip()
        except ValueError:
            return content

    def _get_safe_filepath(self, note: dict, output_folder: Path) -> Path:
        """Sinh tên file và kiểm tra trùng lặp."""
        base_name = sanitize_filename(note["title"])
        filename = f"{base_name}.md"
        filepath = output_folder / filename

        # Nếu file đã tồn tại NHƯNG thuộc về một id khác (trùng tên Title) thì gắn thêm ID
        if filepath.exists():
            existing_id = self._get_note_id_from_file(filepath)
            if existing_id and existing_id != note["id"]:
                short_id = note["id"][:8]
                filename = f"{base_name}_{short_id}.md"
                filepath = output_folder / filename
        
        return filepath

    def _get_note_id_from_file(self, filepath: Path) -> Optional[str]:
        """Extract keep_id from existing markdown file frontmatter."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                in_frontmatter = False
                for line in f:
                    line = line.strip()
                    if line == "---":
                        if in_frontmatter:
                            break
                        in_frontmatter = True
                        continue
                    if in_frontmatter and line.startswith("keep_id:"):
                        return line.split(":", 1)[1].strip().strip('"')
        except Exception:
            pass
        return None

    def start_auto_sync(
        self,
        interval_minutes: int,
        labels: Optional[list[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """Start periodic auto sync."""
        self.stop_auto_sync()
        self._auto_sync_running = True

        def _tick():
            if self._auto_sync_running:
                self.sync_now(labels=labels, date_from=date_from, date_to=date_to)
                if self._auto_sync_running:
                    self._timer = threading.Timer(
                        interval_minutes * 60, _tick
                    )
                    self._timer.daemon = True
                    self._timer.start()

        # Run first sync after interval
        self._timer = threading.Timer(interval_minutes * 60, _tick)
        self._timer.daemon = True
        self._timer.start()

    def stop_auto_sync(self):
        """Stop periodic auto sync."""
        self._auto_sync_running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def get_last_sync_time(self) -> str:
        return self._config.get("last_sync_time", "Chưa sync")

    def get_next_sync_time(self) -> str:
        """Calculate next auto sync time."""
        if not self._auto_sync_running:
            return "—"
        last = self._config.get("last_sync_time", "")
        interval = self._config.get("auto_sync_interval_minutes", 60)
        if last:
            try:
                last_dt = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
                from datetime import timedelta
                next_dt = last_dt + timedelta(minutes=interval)
                return next_dt.strftime("%H:%M")
            except Exception:
                pass
        return "—"
