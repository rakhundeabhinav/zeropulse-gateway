# 🛡️ ZeroPulse // Zero-Trust IoMT Management & Security Gateway

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![WebSocket](https://img.shields.io/badge/Transport-WebSockets-4B5563.svg)](https://websockets.readthedocs.io/)
[![TailwindCSS](https://img.shields.io/badge/Frontend-TailwindCSS-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com/)

> **ZeroPulse** is a specialized Zero-Trust IoMT (Internet of Medical Things) security gateway designed to protect clinical infrastructure against ransomware, unauthorized payload tampering, and anomalous packet floods. Built with real-time heuristic Shannon Entropy inspection and dynamic blast-radius micro-isolation.

---

## 🌟 Key Capabilities

* **Zero-Trust Continuous Verification:** Strict cryptographic message validation using HMAC-SHA256 tokens and granular device identities.
* **Shannon Entropy Heuristic Engine:** Live payload analysis to flag high-entropy ($H > 4.0$) encrypted ransomware blobs before they reach medical core systems.
* **Autonomous Blast-Radius Containment:** Instant hardware quarantine protocol that revokes network ACLs for compromised nodes without manual intervention.
* **Full-Duplex SOC Telemetry Dashboard:** WebSocket-powered event streaming that monitors telemetry, anomalous spikes, and quarantine statuses simultaneously.
* **Adaptive Rate Limiting:** Sliding-window burst analyzer to detect unauthorized network scanning and DoS attempts on IoMT nodes.

---

## 🏗️ Architecture Flow
