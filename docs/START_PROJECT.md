# 🚀 How to Start the HoneyTrace Project

## Quick Start Guide

Follow these steps to start all components of the honeypot system.

---

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 14+** and **npm** installed
3. **All dependencies** installed (see Installation below)

### Check Prerequisites

```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

---

## 📦 Installation (First Time Setup)

### 1. Install Python Dependencies

```bash
# Navigate to project root
cd HONEYPOT

# Install backend dependencies
pip install -r requirements.txt

# Install logging server dependencies
pip install -r logging_server/requirements.txt

# Install ML dependencies
pip install -r ml_requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd db1
npm install
cd ..
```

### 3. Verify ML Models (Optional)

If models are not trained yet, train them:

```bash
# Train Random Forest
python ml_training_system.py

# Train Isolation Forest
python ml_isolation_forest_training.py
```

---

## 🎯 Starting the System

You need to start **3 components** in separate terminals:

### **Option 1: Manual Start (Recommended for Development)**

#### Step 1: Start Logging Server (Terminal 1)

```bash
cd logging_server
python logging_server.py
```

**Expected Output:**
```
🤖 Loading ML models (Random Forest + Isolation Forest)...
   ✅ Random Forest loaded (Accuracy: 0.9535)
   ✅ Isolation Forest loaded (Accuracy: 0.6151)
✅ ML models loaded successfully!
 * Running on http://127.0.0.1:5000
```

**Keep this terminal open!**

#### Step 2: Start Honeypot Services (Terminal 2)

```bash
python start_unified_honeypot.py
```

Or start individual services:

```bash
# Option A: Unified honeypot (all services combined)
python start_unified_honeypot.py

# Option B: Individual services
python fake_git_repo.py        # Port 8001
python fake_cicd_runner.py     # Port 8002
```

**Expected Output:**
```
🚀 Starting Honeypot Services...
✅ Fake Git Repository started on http://localhost:8001
✅ Fake CI/CD Runner started on http://localhost:8002
```

**Keep this terminal open!**

#### Step 3: Start Frontend Dashboard (Terminal 3)

```bash
cd db1
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view the app in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Browser will open automatically at http://localhost:3000**

---

### **Option 2: Using Batch Scripts (Windows)**

#### Windows Quick Start

1. **Start Logging Server** - Double-click: `start_backend.bat`

2. **Start Honeypot** - Run in terminal:
   ```cmd
   python start_unified_honeypot.py
   ```

3. **Start Frontend** - Run in terminal:
   ```cmd
   cd db1
   npm start
   ```

---

## 🎬 Complete Startup Sequence

### Terminal 1: Logging Server
```bash
cd HONEYPOT
cd logging_server
python logging_server.py
```

### Terminal 2: Honeypot Services
```bash
cd HONEYPOT
python start_unified_honeypot.py
```

### Terminal 3: Frontend Dashboard
```bash
cd HONEYPOT
cd db1
npm start
```

---

## ✅ Verification Checklist

After starting all services, verify they're running:

### 1. Check Logging Server
- Open browser: http://localhost:5000/health
- Should return: `{"status": "healthy"}`

### 2. Check Honeypot Services
- Fake Git: http://localhost:8001
- Fake CI/CD: http://localhost:8002
- Unified: http://localhost:8000

### 3. Check Frontend Dashboard
- Open browser: http://localhost:3000
- Should see the FSOCIETY dashboard

### 4. Check ML Models Loaded
- Look in Terminal 1 (Logging Server) for:
  ```
  ✅ Random Forest loaded
  ✅ Isolation Forest loaded
  ```

---

## 🔧 Troubleshooting

### Problem: Port Already in Use

**Solution:**
```bash
# Windows: Find and kill process on port
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in logging_server.py
```

### Problem: ML Models Not Loading

**Solution:**
1. Check if models exist:
   ```bash
   ls ml_models/*.pkl
   ```
2. Retrain models if missing:
   ```bash
   python ml_training_system.py
   python ml_isolation_forest_training.py
   ```

### Problem: Frontend Not Starting

**Solution:**
```bash
cd db1
rm -rf node_modules package-lock.json
npm install
npm start
```

### Problem: Module Not Found Errors

**Solution:**
```bash
# Install missing dependencies
pip install flask flask-cors pandas numpy scikit-learn joblib requests
```

---

## 📊 Service Ports Reference

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Logging Server | 5000 | http://localhost:5000 | Backend API + ML scoring |
| Unified Honeypot | 8000 | http://localhost:8000 | Combined services |
| Fake Git Repo | 8001 | http://localhost:8001 | Git honeypot |
| Fake CI/CD | 8002 | http://localhost:8002 | CI/CD honeypot |
| Frontend Dashboard | 3000 | http://localhost:3000 | React UI |

---

## 🎯 What Happens When You Start

1. **Logging Server** starts and:
   - Loads Random Forest model
   - Loads Isolation Forest model
   - Initializes ensemble predictor
   - Starts Flask API on port 5000
   - Connects to SQLite database

2. **Honeypot Services** start and:
   - Begin listening for connections
   - Log all access attempts
   - Send logs to logging server

3. **Frontend Dashboard** starts and:
   - Loads React application
   - Connects to logging server API
   - Displays real-time data
   - Shows ML predictions

---

## 🔄 Stopping the System

### To Stop Services:

1. **Terminal 1 (Logging Server)**: Press `Ctrl+C`
2. **Terminal 2 (Honeypot)**: Press `Ctrl+C`
3. **Terminal 3 (Frontend)**: Press `Ctrl+C`

All services will stop gracefully.

---

## 📝 First Test

After starting all services, test the system:

### Send a Test Log

```bash
cd logging_server
python send_test_log.py
```

### Check Dashboard

1. Open http://localhost:3000
2. Navigate to "Live Events" tab
3. You should see the test log with ML scores

### Check ML Scoring

1. Go to "ML Insights" tab
2. Verify ML scores are being calculated
3. Check risk levels are assigned

---

## 🚀 Production Deployment

For production deployment:

1. Use process managers (PM2, supervisor)
2. Set up as system services
3. Configure reverse proxy (nginx)
4. Enable HTTPS
5. Set up monitoring and logging

---

## 💡 Tips

- **Keep terminals open** - Services need to run continuously
- **Check logs** - Watch terminal outputs for errors
- **Test incrementally** - Start one service at a time
- **Use separate terminals** - Easier to monitor each service
- **Bookmark URLs** - Quick access to services

---

## 📞 Need Help?

1. Check **README.md** for project overview
2. Check **PROJECT_COMPLETION_SUMMARY.md** for feature status
3. Check terminal error messages
4. Verify all prerequisites are installed

---

## 🎉 Success!

If all services started successfully, you should see:

- ✅ Logging Server running on port 5000
- ✅ Honeypot services running on ports 8000-8002
- ✅ Frontend dashboard on port 3000
- ✅ ML models loaded and ready
- ✅ Database initialized and connected

**Your honeypot system is now live and ready to detect attacks!** 🛡️

