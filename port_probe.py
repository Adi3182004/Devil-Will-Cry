import serial
import time

ports = ["COM3", "COM4", "COM5", "COM6"]

for port in ports:
    try:
        print(f"\nTesting {port}")
        ser = serial.Serial(port, 9600, timeout=2)
        time.sleep(1)
        ser.write(b"AT\r")
        time.sleep(1)
        resp = ser.read_all().decode(errors="ignore")
        ser.close()
        print("Response:", resp if resp else "NO RESPONSE")
    except Exception as e:
        print("Failed:", e)
