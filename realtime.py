import serial
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")

# Connect ESP32
ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)

print("System Started...\n")

while True:
    try:
        line = ser.readline().decode().strip()

        if not line:
            continue

        print("RAW:", line)

        parts = line.split(",")

        if len(parts) != 3:
            continue

        soil = float(parts[2])

        sample = pd.DataFrame([[soil]], columns=["soil"])

        pred = model.predict(sample)
        result = le.inverse_transform(pred)[0]

        print("Prediction:", result)

        # 🔥 CONTROL LOGIC
        if result == "DRY":
            print("⚠️ DRY → Pump ON")
            ser.write(b'1')
        else:
            print("✅ NOT DRY → Pump OFF")
            ser.write(b'0')

        print("----------------------")

    except Exception as e:
        print("ERROR:", e)