# 🎯 How Attacks Work - Simple Explanation

## 🎭 The Big Picture

**You have FAKE servers that attract attackers, log everything, and show it in a dashboard.**

---

## 🖥️ What Servers Are Running?

### 1. **Fake Git Repository** (Port 8001)
- **File:** `fake_git_repo.py`
- **What it does:** Pretends to be a Git server
- **What attackers see:** A real Git repository
- **Reality:** Just a Python script serving fake files

### 2. **Fake CI/CD Runner** (Port 8002)
- **File:** `fake_cicd_runner.py`
- **What it does:** Pretends to be a CI/CD system (like Jenkins)
- **What attackers see:** A real CI/CD pipeline
- **Reality:** Just a Python script showing fake job logs

### 3. **Logging Server** (Port 5000)
- **File:** `logging_server/logging_server.py`
- **What it does:** Receives logs from fake servers
- **What it does:** Runs ML predictions, stores in database
- **This is your BACKEND**

### 4. **Frontend Dashboard** (Port 3000)
- **Directory:** `db1/`
- **What it does:** Shows attacks in a web interface
- **This is your UI**

---

## 🔄 Step-by-Step: What Happens During an Attack

### Example: Attacker tries to steal `.env` file

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Attacker discovers your fake server            │
└─────────────────────────────────────────────────────────┘
Attacker types in browser: http://your-server:8001/.env


┌─────────────────────────────────────────────────────────┐
│ STEP 2: Fake Git Repository receives request            │
│ File: fake_git_repo.py                                  │
└─────────────────────────────────────────────────────────┘
✅ Logs: "Someone from IP 203.0.113.42 tried to access .env"
✅ Serves FAKE .env file (not real secrets!)
✅ Creates log entry with all details


┌─────────────────────────────────────────────────────────┐
│ STEP 3: Log sent to Logging Server                     │
│ POST http://localhost:5000/log                         │
└─────────────────────────────────────────────────────────┘
Log contains:
- IP address: 203.0.113.42
- Action: file_access
- Target: .env
- User agent: curl/7.68.0
- Timestamp: 2024-01-15 10:30:00


┌─────────────────────────────────────────────────────────┐
│ STEP 4: Logging Server processes                        │
│ File: logging_server/logging_server.py                 │
└─────────────────────────────────────────────────────────┘
✅ Adds GeoIP data (country, city, ISP)
✅ Runs ML prediction (is this an attack?)
✅ Calculates risk score
✅ Stores in SQLite database (honeypot.db)


┌─────────────────────────────────────────────────────────┐
│ STEP 5: Frontend Dashboard displays                     │
│ URL: http://localhost:3000                             │
└─────────────────────────────────────────────────────────┘
✅ Shows attack in "Live Events" page
✅ Displays on map (geographic location)
✅ Shows ML risk score: 0.85 (HIGH)
✅ Updates in real-time
```

---

## 🎯 What Are Attackers Actually "Attacking"?

### **Answer: FAKE Python Flask Servers**

**NOT:**
- ❌ Your real database
- ❌ Your real servers
- ❌ Your real credentials
- ❌ Your real systems

**YES:**
- ✅ Fake Python scripts (`fake_git_repo.py`, `fake_cicd_runner.py`)
- ✅ Fake files (`.env`, `secrets.yml` - all fake content!)
- ✅ Fake responses (looks real, but isn't)

---

## 📂 File Structure - What Each File Does

```
HONEYPOT/
│
├── fake_git_repo.py          ← FAKE Git server (Port 8001)
│   └── Attracts attackers looking for Git repos
│   └── Serves fake .env, secrets.yml files
│
├── fake_cicd_runner.py       ← FAKE CI/CD server (Port 8002)
│   └── Attracts attackers looking for CI/CD systems
│   └── Shows fake job logs, credentials
│
├── Honeypot/honeypot_services.py  ← Combined fake service (Port 8000)
│   └── Both Git + CI/CD in one
│
├── logging_server/
│   └── logging_server.py     ← BACKEND (Port 5000)
│       └── Receives logs from fake servers
│       └── Runs ML predictions
│       └── Stores in database
│
├── db1/                      ← FRONTEND (Port 3000)
│   └── React dashboard
│   └── Shows attacks visually
│
└── honeypot.db               ← DATABASE
    └── SQLite database
    └── Stores all attack logs
```

---

## 🔍 Real Example: What Happens

### Attacker's View:

```bash
# Attacker tries to access secrets
$ curl http://your-server:8001/secrets.yml

# Response (FAKE):
database_password: "fake_password_123"
api_key: "fake_key_abcdef"
secret_token: "fake_token_xyz"
```

**Attacker thinks:** "I got real secrets!"  
**Reality:** All fake! Nothing works!

### Your View (in Dashboard):

```
🚨 Attack Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IP Address:     203.0.113.42
Location:       New York, United States
Action:         file_access
Target:         secrets.yml
ML Score:       0.85 (HIGH RISK)
Risk Level:     HIGH
Attack Type:    DATA_EXFILTRATION
Time:           2024-01-15 10:30:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎬 Complete Attack Flow

```
1. Attacker → Fake Git Server (Port 8001)
   "I want to access .env file"
   
2. Fake Git Server → Logs attack
   "Someone tried to access .env from IP 203.0.113.42"
   
3. Fake Git Server → Sends log to Logging Server (Port 5000)
   POST /log {ip, action, target, ...}
   
4. Logging Server → Adds GeoIP data
   "IP is from New York, USA"
   
5. Logging Server → Runs ML prediction
   "ML Score: 0.85 (HIGH RISK)"
   
6. Logging Server → Stores in database
   SQLite: honeypot.db
   
7. Frontend Dashboard → Fetches from Logging Server
   GET /api/live-events
   
8. Frontend Dashboard → Displays attack
   Shows in real-time on screen
```

---

## 💡 Key Points

1. **Nothing Real is Attacked**
   - All servers are fake Python scripts
   - All files are fake (not real secrets)
   - No real systems are exposed

2. **Everything is Logged**
   - Every request is captured
   - IP addresses recorded
   - Actions tracked
   - ML scores calculated

3. **You See Everything**
   - Real-time dashboard
   - Attack statistics
   - Geographic maps
   - ML insights

4. **Attackers Get Nothing**
   - Fake credentials
   - Fake files
   - No real access

---

## 🚀 Try It Yourself

### 1. Start the system:
```bash
python start_unified_honeypot.py
```

### 2. Simulate an attack:
```bash
curl http://localhost:8001/.env
```

### 3. Check the dashboard:
- Open: http://localhost:3000
- Go to "Live Events" page
- See your attack appear!

### 4. Check the database:
```bash
sqlite3 honeypot.db "SELECT source_ip, action, ml_score FROM logs ORDER BY id DESC LIMIT 5;"
```

---

## 📊 Summary

**What you have:**
- ✅ 3 fake servers (Git, CI/CD, Combined)
- ✅ 1 logging server (backend)
- ✅ 1 frontend dashboard (UI)
- ✅ 1 database (stores logs)

**What gets attacked:**
- ✅ Only the fake servers
- ✅ Nothing real!

**What you get:**
- ✅ Complete attack logs
- ✅ IP addresses
- ✅ ML risk scores
- ✅ Real-time monitoring

**What attackers get:**
- ❌ Fake files
- ❌ Fake credentials
- ❌ Nothing useful!

---

## 🎯 Bottom Line

**You're running FAKE servers that:**
1. Look real to attackers
2. Log everything they do
3. Show it in your dashboard
4. Keep your real systems safe

**It's like a security camera that also traps attackers!**

