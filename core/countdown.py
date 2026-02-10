import threading
import time

class CountdownTimer:
    def __init__(self, seconds, on_timeout, on_tick=None):
        self.seconds = seconds
        self.on_timeout = on_timeout
        self.on_tick = on_tick
        self.cancelled = False
        self.thread = None

    def start(self):
        self.cancelled = False
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def cancel(self):
        self.cancelled = True
        print("[COUNTDOWN] Cancelled by user")

    def _run(self):
        for remaining in range(self.seconds, 0, -1):
            if self.cancelled:
                return

            if self.on_tick:
                try:
                    self.on_tick(remaining)
                except Exception as e:
                    print("[COUNTDOWN] Tick callback error:", e)

            print(f"[COUNTDOWN] Emergency in {remaining} seconds")
            time.sleep(1)

        if not self.cancelled:
            if self.on_tick:
                try:
                    self.on_tick(0)
                except Exception:
                    pass

            print("[COUNTDOWN] Timeout reached")
            self.on_timeout()
