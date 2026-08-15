import base64
import os
import time
import requests
from gateway.crypto_utils import generate_signature

GATEWAY_URL = "http://127.0.0.1:8000/api/v1/telemetry"
DEVICE_ID = "DEV-INFUSION-101"
SECRET_KEY = "medguard_secret_key_101"

def attack_high_entropy():
    print("\n--- ATTACK VECTOR 1: Ransomware High-Entropy Payload ---")
    timestamp = time.time()
    
    random_ciphertext = base64.b64encode(os.urandom(1024)).decode("utf-8")
    data = {"encrypted_chunk": random_ciphertext}
    
    signature = generate_signature(SECRET_KEY, data, timestamp)
    payload = {
        "device_id": DEVICE_ID,
        "timestamp": timestamp,
        "signature": signature,
        "data": data
    }
    
    resp = requests.post(GATEWAY_URL, json=payload)
    print(f"Gateway Response: HTTP {resp.status_code} -> {resp.text}")

def attack_packet_burst():
    print("\n--- ATTACK VECTOR 2: Excessive Packet Rate / DoS Flood ---")
    for i in range(15):
        timestamp = time.time()
        data = {"flood_packet_index": i}
        signature = generate_signature(SECRET_KEY, data, timestamp)
        payload = {
            "device_id": DEVICE_ID,
            "timestamp": timestamp,
            "signature": signature,
            "data": data
        }
        resp = requests.post(GATEWAY_URL, json=payload)
        print(f"Packet {i+1}/15 -> HTTP {resp.status_code}")
        time.sleep(0.05)

if __name__ == "__main__":
    print("Select Attack Vector:")
    print("1. Inject High-Entropy Ransomware Blob")
    print("2. Launch Rapid Packet Burst (DoS / Scan)")
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        attack_high_entropy()
    elif choice == "2":
        attack_packet_burst()
    else:
        print("Invalid choice.")
