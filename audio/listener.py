import sounddevice as sd
import numpy as np
import time

class AudioListener:
    def __init__(self, threshold=0.4, cooldown=2):
        self.threshold = threshold
        self.cooldown = cooldown
        self.on_trigger = None
        self.last_trigger_time = 0

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)

        volume = np.sqrt(np.mean(indata**2))
        print(f"[AUDIO LEVEL] {volume:.4f}")

        now = time.time()
        if volume > self.threshold:
            if now - self.last_trigger_time >= self.cooldown:
                self.last_trigger_time = now
                print(f"[AUDIO] Threshold crossed: {volume:.4f}")
                if self.on_trigger:
                    self.on_trigger()

    def start(self, on_trigger):
        print("[AUDIO] Listening continuously")
        self.on_trigger = on_trigger

        with sd.InputStream(channels=1, callback=self._audio_callback):
            while True:
                time.sleep(0.1)
