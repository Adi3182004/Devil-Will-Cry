import serial
import time

class GSMSender:
    def __init__(self, port="COM5", baudrate=9600, timeout=5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def _connect(self):
        return serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

    def send_sms(self, number, message):
        try:
            modem = self._connect()
            time.sleep(1)

            modem.write(b"AT\r")
            time.sleep(0.5)

            modem.write(b"AT+CMGF=1\r")
            time.sleep(0.5)

            modem.write(f'AT+CMGS="{number}"\r'.encode())
            time.sleep(0.5)

            modem.write(message.encode() + b"\x1A")
            time.sleep(3)

            modem.close()
            print("[GSM] SMS sent successfully")

        except Exception as e:
            print(f"[GSM] SMS failed: {e}")
