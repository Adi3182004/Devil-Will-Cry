class ThreatScore:
    def __init__(self, threshold=60):
        self.score = 0
        self.threshold = threshold

    def reset(self):
        self.score = 0

    def add_manual_trigger(self):
        self.score += 100

    def add_scream_detected(self):
        self.score += 50

    def add_panic_keyword(self):
        self.score += 40

    def add_sudden_motion(self):
        self.score += 30

    def is_threat_confirmed(self):
        return self.score >= self.threshold

    def get_score(self):
        return self.score
