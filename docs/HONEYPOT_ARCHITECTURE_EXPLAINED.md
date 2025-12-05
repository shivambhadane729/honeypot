# 🍯 Honeypot System Architecture - Complete Explanation

## 🎯 What is a Honeypot?

A **honeypot** is a **fake server** designed to **attract attackers**. It looks like a real service but is actually a trap that:
- ✅ Logs all attacker activity
- ✅ Doesn't expose real systems
- ✅ Helps you learn about attack patterns
- ✅ Detects malicious behavior

---

## 🏗️ Your Honeypot System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR HONEYPOT SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FAKE SERVERS (What Attackers "Attack")                  │  │
│  │  These are FAKE - not real services!                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Fake Git     │  │ Fake CI/CD   │  │ Consolidated │        │
│  │ Repository   │  │ Runner       │  │ Honeypot     │        │
│  │ Port 8001    │  │ Port 8002    │  │ Port 8000    │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                 │                  │                 │
│         └─────────────────┼──────────────────┘                 │
│                           │                                    │
│                           ▼                                    │
│                  ┌──────────────────┐                          │
│                  │  Logging Server │                          │
│                  │  Port 5000      │                          │
│                  │  (Backend API)  │                          │
│                  └────────┬─────────┘                          │
│                           │                                    │
│                           ▼                                    │
│                  ┌──────────────────┐                          │
│                  │  ML Prediction   │                          │
│                  │  System          │                          │
│                  └────────┬─────────┘                          │
│                           │                                    │
│                           ▼                                    │
│                  ┌──────────────────┐                          │
│                  │  SQLite Database │                          │
│                  │  honeypot.db     │                          │
│                  └────────┬─────────┘                          │
│                           │                                    │
│                           ▼                                    │
│                  ┌──────────────────┐                          │
│                  │  React Dashboard │                          │
│                  │  Port 3000       │                          │
│                  │  (Frontend UI)   │                          │
│                  └──────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎭 What Are You "Attacking"?

### **NOTHING REAL!** These are all **FAKE services**:

### 1. **Fake Git Repository** (Port 8001)
**What it looks like:** A real Git repository server  
**What it actually is:** A fake Python Flask server

**Attackers can:**
- `POST /repo/push` - Try to push malicious code
- `POST /repo/pull` - Try to pull repository data
- `GET /.env` - Try to steal environment variables
- `GET /secrets.yml` - Try to steal secrets
- `GET /config.json` - Try to steal configuration

**What happens:**
- Server responds like a real Git repo
- Serves fake files (not real secrets!)
- Logs everything the attacker does
- Sends logs to logging server

---

### 2. **Fake CI/CD Runner** (Port 8002)
**What it looks like:** A real CI/CD pipeline (like Jenkins, GitLab CI)  
**What it actually is:** A fake Python Flask server

**Attackers can:**
- `POST /ci/run` - Try to execute malicious jobs
- `GET /ci/credentials` - Try to steal CI/CD credentials
- `GET /ci/logs/<job_id>` - Try to view job logs
- `GET /ci/config` - Try to view configuration

**What happens:**
- Server responds like a real CI/CD system
- Shows fake job execution logs
- Provides fake credentials (not real!)
- Logs all attacker activity

---

### 3. **Consolidated Honeypot** (Port 8000)
**What it is:** Combined service with both Git + CI/CD endpoints  
**Purpose:** Single entry point for all honeypot operations

---

## 🔄 Complete Attack Flow Example

### Scenario: Attacker tries to steal `.env` file

```
Step 1: Attacker discovers your fake Git server
        └─> Attacker: "I found a Git repo at http://your-server:8001"

Step 2: Attacker tries to access sensitive file
        └─> Attacker sends: GET http://your-server:8001/.env

Step 3: Fake Git Repository receives request
        └─> fake_git_repo.py processes the request
        └─> Logs: "Someone tried to access .env file"
        └─> Serves FAKE .env file (not real secrets!)

Step 4: Log sent to Logging Server
        └─> POST http://localhost:5000/log
        └─> Contains: IP address, action, headers, etc.

Step 5: Logging Server processes
        └─> Enriches with GeoIP (country, city, ISP)
        └─> Runs ML prediction (is this an attack?)
        └─> Stores in SQLite database (honeypot.db)

Step 6: Frontend Dashboard displays
        └─> React app fetches from logging server
        └─> Shows attack in real-time
        └─> Displays ML score, risk level, location
```

---

## 🖥️ What Servers Are Running?

### **4 Separate Services:**

1. **Fake Git Repository** (`fake_git_repo.py`)
   - Port: **8001**
   - Purpose: Attract attackers looking for Git repos
   - Endpoints: `/repo/push`, `/repo/pull`, `/.env`, `/secrets.yml`

2. **Fake CI/CD Runner** (`fake_cicd_runner.py`)
   - Port: **8002**
   - Purpose: Attract attackers looking for CI/CD systems
   - Endpoints: `/ci/run`, `/ci/credentials`, `/ci/logs`

3. **Logging Server** (`logging_server/logging_server.py`)
   - Port: **5000**
   - Purpose: Collect and process all attack logs
   - Endpoints: `POST /log`, `GET /logs`, `GET /stats`
   - **This is your backend API**

4. **Frontend Dashboard** (`db1/` - React app)
   - Port: **3000**
   - Purpose: Visualize attacks in real-time
   - **This is your web interface**

---

## 🎯 What Gets "Attacked"?

### **Answer: FAKE SERVICES ONLY!**

- ❌ **NOT** your real database
- ❌ **NOT** your real servers
- ❌ **NOT** your real credentials
- ✅ **ONLY** fake Python Flask servers
- ✅ **ONLY** fake files and fake responses

### Example: Attacker tries `GET /.env`

**What they get:**
```yaml
# Fake .env file (not real!)
DATABASE_URL=fake://fake:fake@fake:5432/fake
API_KEY=fake_key_12345
SECRET_TOKEN=fake_secret_token
```

**What you get:**
- ✅ Attacker's IP address
- ✅ What they tried to access
- ✅ Their user agent
- ✅ Geographic location
- ✅ ML risk score
- ✅ Timestamp

**What they DON'T get:**
- ❌ Real credentials
- ❌ Real database access
- ❌ Real system information

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│  Attacker   │
│  (Internet) │
└──────┬──────┘
       │
       │ HTTP Request
       │ GET /.env
       ▼
┌─────────────────────┐
│ Fake Git Repository │  ← FAKE SERVER (Port 8001)
│ (fake_git_repo.py)  │
└──────┬──────────────┘
       │
       │ 1. Logs attack
       │ 2. Serves fake file
       │ 3. Sends log to logging server
       ▼
┌─────────────────────┐
│  Logging Server     │  ← BACKEND (Port 5000)
│ (logging_server.py) │
│                     │
│  • Receives log     │
│  • GeoIP enrichment │
│  • ML prediction    │
│  • Store in DB      │
└──────┬──────────────┘
       │
       │ Stores in SQLite
       ▼
┌─────────────────────┐
│  honeypot.db        │  ← DATABASE
│  (SQLite)           │
│                     │
│  • All attack logs  │
│  • ML scores        │
│  • GeoIP data       │
└──────┬──────────────┘
       │
       │ API calls
       ▼
┌─────────────────────┐
│  React Dashboard    │  ← FRONTEND (Port 3000)
│  (db1/)             │
│                     │
│  • Shows attacks    │
│  • Real-time updates│
│  • Charts & maps    │
└─────────────────────┘
```

---

## 🔍 Real Attack Example

### What an attacker sees:

```bash
# Attacker discovers your server
$ curl http://your-server:8001/.env

# Response (FAKE):
DATABASE_URL=postgresql://admin:password123@db.internal:5432/production
API_KEY=sk_live_1234567890abcdef
SECRET_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Attacker thinks:** "I got real credentials!"  
**Reality:** All fake! Nothing works!

### What you see in dashboard:

```
📊 Attack Detected
IP: 203.0.113.42
Country: United States
City: New York
Action: file_access
Target: .env
ML Score: 0.85 (HIGH RISK)
Risk Level: HIGH
Attack Type: DATA_EXFILTRATION
```

---

## 🗄️ Database Structure

**File:** `honeypot.db` (SQLite database)

**What's stored:**
- All attack logs
- IP addresses
- Actions performed
- ML predictions
- Geographic data
- Timestamps

**NOT stored:**
- Real credentials (they're fake!)
- Real system data
- Any sensitive information

---

## 🎨 Frontend Dashboard

**What it shows:**
- Real-time attack stream
- Geographic attack map
- ML risk scores
- Attack statistics
- IP investigation tools

**What it does:**
- Fetches data from logging server (Port 5000)
- Displays in beautiful charts
- Updates every 30 seconds
- Shows ML insights

---

## 🔐 Security Note

**Important:** These are **FAKE services** designed to attract attackers.

- ✅ Safe to expose (no real data)
- ✅ Logs all activity
- ✅ Helps detect threats
- ⚠️ Should run in isolated network
- ⚠️ Monitor all traffic

---

## 📝 Summary

**What you're "attacking":**
- ✅ Fake Git Repository (Port 8001)
- ✅ Fake CI/CD Runner (Port 8002)
- ✅ Consolidated Honeypot (Port 8000)

**What happens:**
1. Attacker interacts with fake service
2. Fake service logs everything
3. Logs sent to logging server (Port 5000)
4. ML system analyzes and scores
5. Data stored in database
6. Frontend displays in dashboard

**What you get:**
- ✅ Attack logs
- ✅ IP addresses
- ✅ Attack patterns
- ✅ ML risk scores
- ✅ Geographic data
- ✅ Real-time monitoring

**What attackers get:**
- ❌ Fake credentials
- ❌ Fake files
- ❌ Nothing real!

---

## 🚀 How to See It in Action

1. **Start all services:**
   ```bash
   python start_unified_honeypot.py
   ```

2. **Simulate an attack:**
   ```bash
   curl http://localhost:8001/.env
   ```

3. **Check dashboard:**
   - Open: http://localhost:3000
   - See the attack appear in real-time!

4. **Check database:**
   ```bash
   sqlite3 honeypot.db "SELECT * FROM logs ORDER BY id DESC LIMIT 5;"
   ```

---

## 💡 Key Takeaway

**You're not attacking anything real!**

You're running **fake servers** that:
- Look real to attackers
- Log everything they do
- Help you detect threats
- Keep your real systems safe

It's like a **security camera** that also **traps** attackers!

