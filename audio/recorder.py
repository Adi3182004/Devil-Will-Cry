import sounddevice as sd
import wave
import os
from datetime import datetime
import threading
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate=44100, channels=1, duration=10):
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.lock = threading.Lock()

    def record(self):
        with self.lock:
            os.makedirs("data/evidence", exist_ok=True)

            filename = datetime.now().strftime("audio_%Y%m%d_%H%M%S.wav")
            filepath = os.path.join("data/evidence", filename)

            print(f"[AUDIO] Recording {self.duration}s → {filepath}")

            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16"
            )

            sd.wait()

            with wave.open(filepath, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(recording.tobytes())

            print("[AUDIO] Audio saved")
            return filepath
