<p align="center" width="100%">
 <img width="281" height="151" alt="miniflix" src="https://github.com/user-attachments/assets/0dc8c577-1e0d-4748-8212-bf2d962b3477" />
</p>

---

A DIY Netflix experiment looking at edge-adaptive streaming techniques and explores resilience / load recovery

A couple of forward-looking TODOs

## 🏁 Getting Started

Straight forward to run:

`docker compose build` 

`docker compose up`


### **RTMP (miniflix-rtmp)**
Ingest server running NGINX-RTMP. Accepts live video at `rtmp://localhost/live/stream` and forwards it to the packager.

### **Packager (miniflix-packager)**
FFmpeg-based transcoder that converts the RTMP stream into HLS segments and a playlist, writing them into the shared `media` volume.

### **Origin (miniflix-origin)**
NGINX web server that serves the MiniFlix web player and the generated HLS content at `http://localhost:8080/hls/rtmp.m3u8`.

## ⏩ Forward-looking TODOs
--- 

### 🎬 Streaming Pipeline

- [x] Finalize packager `run.sh` with stable RTMP → HLS handling  
- [ ] Ensure “cold start” HLS creation is reliable after start/stop  
- [ ] Add a simple health endpoint for packager & origin containers  
- [ ] Implement automatic cleanup of stale HLS segments  
- [ ] Add option for **per-session** HLS output directories  
- [ ] Add configurable HLS latency modes (1s, 2s, 4s segment sizes)  

---

### 🌐 Web Player 

- [ ] Implement light→dark red→black gradient background  
- [ ] Add per-session cache-busting logic  
- [ ] Add local bitrate / buffer telemetry overlay (debug HUD)  

---

### 🌐 Network Simulation (Mininet)

- [ ] Add example `miniflix_basic.py` topology  
- [ ] Add topology with multiple origins and failover routing  
- [ ] Add automated bandwidth sweeps (1–20 Mbps)  
- [ ] Add jitter/loss experiments  
- [ ] Add script to collect per-client playback results  
- [ ] Add Mininet launcher:

---

### 🧪   Netflix-esque Algorithms (Research & Sim)

- [ ] Implement **BOLA** (Buffer Occupancy–based Lyapunov Algorithm) inside the MiniFlix HLS.js player  
- [ ] Implement **BBA** (Buffer-Based Adaptation) as an alternative ABR strategy  
- [ ] Add an ABR comparison mode: BOLA vs BBA  

---

### 📉 Load Testing
- [ ] Add script to stress-test origin container
- [ ] Capture metrics: rebuffering, HLS latency, segment availability
- [ ] graphs for ABR decisions

---
## 📊 Observability 
- [ ] Add Prometheus + Grafana stack
