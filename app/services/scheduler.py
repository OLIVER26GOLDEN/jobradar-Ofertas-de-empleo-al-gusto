import os
import threading
import time
from collections.abc import Callable


class ScraperScheduler:
    def __init__(self, task: Callable[[str], int]) -> None:
        self.task = task
        self.thread: threading.Thread | None = None
        self.stop_event = threading.Event()

    def start(self) -> None:
        enabled = os.getenv("SCRAPER_SCHEDULER_ENABLED", "false").lower() == "true"
        if not enabled or self.thread and self.thread.is_alive():
            return

        interval_minutes = int(os.getenv("SCRAPER_INTERVAL_MINUTES", "360"))
        query = os.getenv("SCRAPER_DEFAULT_QUERY", "python")
        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self._run_loop,
            args=(query, interval_minutes),
            daemon=True,
        )
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

    def _run_loop(self, query: str, interval_minutes: int) -> None:
        interval_seconds = max(interval_minutes, 1) * 60
        while not self.stop_event.wait(interval_seconds):
            try:
                self.task(query)
            except Exception as exc:
                print(f"Error en scheduler de scraper: {exc}")
