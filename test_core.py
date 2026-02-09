# from core.state_manager import StateManager, SystemState
# from core.threat_score import ThreatScore
# from core.countdown import CountdownTimer
# import time

# def emergency_triggered():
#     print("🚨 EMERGENCY MODE ACTIVATED 🚨")

# def test_state_manager():
#     print("\n--- Testing State Manager ---")
#     sm = StateManager()

#     assert sm.is_idle()
#     sm.set_state(SystemState.RISK_DETECTED)
#     assert sm.is_risk()
#     sm.set_state(SystemState.EMERGENCY)
#     assert sm.is_emergency()

#     print("✅ State Manager Test Passed")

# def test_threat_score():
#     print("\n--- Testing Threat Score ---")
#     ts = ThreatScore()

#     ts.add_scream_detected()
#     print("Score after scream:", ts.get_score())
#     assert not ts.is_threat_confirmed()

#     ts.add_panic_keyword()
#     print("Score after keyword:", ts.get_score())
#     assert ts.is_threat_confirmed()

#     ts.reset()
#     ts.add_manual_trigger()
#     assert ts.is_threat_confirmed()

#     print("✅ Threat Score Test Passed")

# def test_countdown_cancel():
#     print("\n--- Testing Countdown Cancel ---")

#     timer = CountdownTimer(5, emergency_triggered)
#     timer.start()
#     time.sleep(2)
#     timer.cancel()

#     time.sleep(4)
#     print("✅ Countdown Cancel Test Passed")

# def test_countdown_timeout():
#     print("\n--- Testing Countdown Timeout ---")

#     timer = CountdownTimer(5, emergency_triggered)
#     timer.start()

#     time.sleep(7)
#     print("✅ Countdown Timeout Test Passed")

# if __name__ == "__main__":
#     test_state_manager()
#     test_threat_score()
#     test_countdown_cancel()
#     test_countdown_timeout()

#     print("\n🔥 CORE SYSTEM TEST COMPLETED SUCCESSFULLY 🔥")
