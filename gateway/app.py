import os
import time
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from gateway.crypto_utils import verify_signature
from gateway.anomaly import calculate_shannon_entropy, TrafficRateAnalyzer

app = FastAPI(title="MedGuard Zero-Trust Gateway")

# Allow all origins, credentials, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Mock Zero-Trust Registry
DEVICE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "DEV-INFUSION-101": {
        "name": "Smart Infusion Pump 01",
        "type": "Infusion Pump",
        "secret": "medguard_secret_key_101",
        "status": "ACTIVE",
        "last_seen": time.time()
    },
    "DEV-VENT-202": {
        "name": "ICU Ventilator Unit A",
        "type": "Ventilator",
        "secret": "medguard_secret_key_202",
        "status": "ACTIVE",
        "last_seen": time.time()
    }
}

rate_analyzer = TrafficRateAnalyzer(max_requests=10, window_seconds=2.0)
active_connections: List[WebSocket] = []

class TelemetryPayload(BaseModel):
    device_id: str
    timestamp: float
    signature: str
    data: Dict[str, Any]

async def broadcast_event(event_data: dict):
    disconnected = []
    for ws in list(active_connections):
        try:
            await ws.send_json(event_data)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        if ws in active_connections:
            active_connections.remove(ws)

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return HTMLResponse("<h2>static/index.html not found</h2>")

@app.get("/api/v1/devices")
async def get_devices():
    return DEVICE_REGISTRY

@app.post("/api/v1/devices/{device_id}/reset")
async def reset_device_status(device_id: str):
    if device_id not in DEVICE_REGISTRY:
        raise HTTPException(status_code=404, detail="Device not found.")
    DEVICE_REGISTRY[device_id]["status"] = "ACTIVE"
    await broadcast_event({
        "type": "DEVICE_RESTORED",
        "device_id": device_id,
        "timestamp": time.time()
    })
    return {"status": "SUCCESS", "message": f"{device_id} restored to ACTIVE state."}

# WebSocket route accepting without origin restrictions
@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Await incoming message or keep connection alive
            await websocket.receive_text()
    except (WebSocketDisconnect, Exception):
        if websocket in active_connections:
            active_connections.remove(websocket)

@app.post("/api/v1/telemetry")
async def ingest_telemetry(payload: TelemetryPayload):
    dev_id = payload.device_id

    if dev_id not in DEVICE_REGISTRY:
        raise HTTPException(status_code=403, detail="Zero-Trust Rejection: Unregistered device identity.")

    device = DEVICE_REGISTRY[dev_id]

    if device["status"] == "QUARANTINED":
        raise HTTPException(status_code=403, detail="Zero-Trust Rejection: Device is currently QUARANTINED.")

    if not verify_signature(device["secret"], payload.signature, payload.data, payload.timestamp):
        device["status"] = "QUARANTINED"
        await broadcast_event({
            "type": "SECURITY_ALERT",
            "device_id": dev_id,
            "reason": "INVALID_SIGNATURE",
            "details": "Cryptographic signature validation failed. Access revoked.",
            "timestamp": time.time()
        })
        raise HTTPException(status_code=401, detail="Cryptographic verification failed.")

    if rate_analyzer.is_rate_exceeded(dev_id):
        device["status"] = "QUARANTINED"
        await broadcast_event({
            "type": "SECURITY_ALERT",
            "device_id": dev_id,
            "reason": "TRAFFIC_BURST_FLOOD",
            "details": "Packet burst rate exceeded threshold (possible network scan / DoS).",
            "timestamp": time.time()
        })
        raise HTTPException(status_code=429, detail="Traffic threshold breached. Device quarantined.")

    entropy_score = 0.0
    for val in payload.data.values():
        score = calculate_shannon_entropy(str(val))
        if score > entropy_score:
            entropy_score = score

    if not payload.data:
        entropy_score = calculate_shannon_entropy(str(payload.data))

    if entropy_score > 4.0:
        device["status"] = "QUARANTINED"
        await broadcast_event({
            "type": "SECURITY_ALERT",
            "device_id": dev_id,
            "reason": "RANSOMWARE_HIGH_ENTROPY",
            "details": f"High Shannon Entropy ({entropy_score:.2f}) detected in telemetry chunk.",
            "timestamp": time.time()
        })
        raise HTTPException(status_code=400, detail=f"High entropy detected ({entropy_score:.2f}). Device quarantined.")

    device["last_seen"] = time.time()
    await broadcast_event({
        "type": "TELEMETRY_ACCEPTED",
        "device_id": dev_id,
        "entropy": round(entropy_score, 2),
        "data": payload.data,
        "timestamp": payload.timestamp
    })

    return {"status": "INGESTED", "entropy": entropy_score}
