from enum import Enum
import threading
import time

class SystemState(Enum):
    IDLE = "IDLE"
    RISK_DETECTED = "RISK_DETECTED"
    EMERGENCY = "EMERGENCY"

class StateManager:
    def __init__(self):
        self.state = SystemState.IDLE
        self.lock = threading.Lock()

    def set_state(self, new_state):
        with self.lock:
            self.state = new_state
            print(f"[STATE] Changed to {self.state.value}")

    def get_state(self):
        with self.lock:
            return self.state

    def is_idle(self):
        return self.get_state() == SystemState.IDLE

    def is_risk(self):
        return self.get_state() == SystemState.RISK_DETECTED

    def is_emergency(self):
        return self.get_state() == SystemState.EMERGENCY
