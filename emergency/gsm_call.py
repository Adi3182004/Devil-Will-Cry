import serial
import time

class GSMCaller:
    def __init__(self, port="COM5", baudrate=9600, timeout=5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def call_number(self, number, duration=20):
        try:
            modem = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )

            time.sleep(1)
            modem.write(b"AT\r")
            time.sleep(0.5)

            modem.write(f"ATD{number};\r".encode())
            print("[GSM] Calling number...")

            time.sleep(duration)

            modem.write(b"ATH\r")
            time.sleep(1)

            modem.close()
            print("[GSM] Call ended")

        except Exception as e:
            print(f"[GSM] Call failed: {e}")
