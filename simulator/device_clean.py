import time
import requests
from gateway.crypto_utils import generate_signature

GATEWAY_URL = "http://127.0.0.1:8000/api/v1/telemetry"
DEVICE_ID = "DEV-INFUSION-101"
SECRET_KEY = "medguard_secret_key_101"

def run_clean_device():
    print(f"[*] Starting Legitimate IoMT Node: {DEVICE_ID}")
    infused_total = 100.0

    while True:
        timestamp = time.time()
        infused_total += 0.5

        # Normal structured medical telemetry
        data = {
            "rate_ml_hr": 25.0,
            "volume_infused_ml": round(infused_total, 2),
            "medication": "0.9% Normal Saline",
            "battery_level": 98
        }

        signature = generate_signature(SECRET_KEY, data, timestamp)

        payload = {
            "device_id": DEVICE_ID,
            "timestamp": timestamp,
            "signature": signature,
            "data": data
        }

        try:
            resp = requests.post(GATEWAY_URL, json=payload, timeout=2.0)
            if resp.status_code == 200:
                print(f"[CLEAN NODE] Sent telemetry | Status: 200 OK | Infused: {infused_total:.1f} mL")
            else:
                print(f"[CLEAN NODE] Blocked: HTTP {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[!] Connection failed: {e}")

        time.sleep(2.0)

if __name__ == "__main__":
    run_clean_device()