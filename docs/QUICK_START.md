# ⚡ Quick Start Guide

## 🚀 Start Everything with One Click (Windows)

**Double-click:** `start_all.bat`

This will open 3 separate windows:
1. Logging Server (Port 5000)
2. Honeypot Services (Ports 8000-8002)
3. Frontend Dashboard (Port 3000)

---

## 📋 Manual Start (Step-by-Step)

### Terminal 1: Logging Server
```bash
cd logging_server
python logging_server.py
```

### Terminal 2: Honeypot Services
```bash
python start_unified_honeypot.py
```

### Terminal 3: Frontend Dashboard
```bash
cd db1
npm start
```

---

## ✅ Verify Everything is Running

1. **Logging Server**: http://localhost:5000/health
2. **Honeypot**: http://localhost:8000
3. **Dashboard**: http://localhost:3000

---

## 📖 Full Documentation

For detailed instructions, troubleshooting, and more:
- See **START_PROJECT.md** for complete startup guide
- See **README.md** for project overview

---

**That's it! Your honeypot system is now running.** 🛡️
