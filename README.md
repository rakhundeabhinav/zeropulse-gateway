# 🛡️ ZeroPulse — Zero-Trust IoMT Security Gateway

> A real-time **Zero-Trust security gateway for IoMT infrastructure**, designed to detect suspicious medical-device traffic and automatically isolate compromised nodes.

## 🚀 Features

* 🔐 **HMAC-SHA256 Authentication** — verifies device identity and message integrity.
* 📊 **Shannon Entropy Detection** — identifies high-randomness/ransomware-like payloads.
* 🚨 **Auto Quarantine** — isolates suspicious devices using blast-radius containment.
* ⚡ **Rate Limiting** — detects traffic floods and abnormal request bursts.
* 🖥️ **Live SOC Dashboard** — real-time security telemetry via WebSockets.

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
