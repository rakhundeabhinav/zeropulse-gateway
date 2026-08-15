# 🛡️ ZeroPulse // Zero-Trust IoMT Management & Security Gateway

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![WebSocket](https://img.shields.io/badge/Transport-WebSockets-4B5563.svg)](https://websockets.readthedocs.io/)
[![TailwindCSS](https://img.shields.io/badge/Frontend-TailwindCSS-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com/)

> **ZeroPulse** is a specialized Zero-Trust IoMT (Internet of Medical Things) security gateway designed to protect clinical infrastructure against ransomware, unauthorized payload tampering, and anomalous packet floods. Built with real-time heuristic Shannon Entropy inspection and dynamic blast-radius micro-isolation.

🔗 **Live Public SOC Console:** [https://court-festivals-radar-packages.trycloudflare.com](https://court-festivals-radar-packages.trycloudflare.com)

---

## 🌟 Key Capabilities

* **Zero-Trust Continuous Verification:** Strict cryptographic message validation using HMAC-SHA256 tokens and granular device identities.
* **Shannon Entropy Heuristic Engine:** Live payload analysis to flag high-entropy ($H > 4.0$) encrypted ransomware blobs before they reach medical core systems.
* **Autonomous Blast-Radius Containment:** Instant hardware quarantine protocol that revokes network ACLs for compromised nodes without manual intervention.
* **Full-Duplex SOC Telemetry Dashboard:** WebSocket-powered event streaming that monitors telemetry, anomalous spikes, and quarantine statuses simultaneously.
* **Adaptive Rate Limiting:** Sliding-window burst analyzer to detect unauthorized network scanning and DoS attempts on IoMT nodes.

---

## 🏗️ Architecture Flow

## 🏗️ Architecture

```text
IoMT Device
     ↓
ZeroPulse Gateway
     ↓
HMAC Auth → Rate Analysis → Entropy Analysis
     ↓
 ┌───────────────┐
 │   Decision    │
 └───────┬───────┘
     ┌───┴───┐
     ↓       ↓
   ALLOW   QUARANTINE
     └───┬───┘
         ↓
   Live SOC Dashboard
```

## ⚡ Quick Start

```bash
git clone https://github.com/rakhundeabhinav/zeropulse-gateway.git
cd zeropulse-gateway

python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt

uvicorn gateway.app:app --host 127.0.0.1 --port 8000 --ws websockets
```

Open **http://127.0.0.1:8000**

### 🧪 Simulate Devices

```bash
# Normal device
python -m simulator.device_clean

# Simulated attack
python -m simulator.device_infected
```

## 🛠️ Tech Stack

**Python • FastAPI • WebSockets • TailwindCSS • HMAC-SHA256 • Shannon Entropy**

## ⚠️ Disclaimer

ZeroPulse is an **educational/research prototype** for simulated IoMT security testing and is not intended for direct deployment with real clinical devices.

## 👨‍💻 Author

**Abhinav Rakhunde**
[GitHub](https://github.com/rakhundeabhinav)
