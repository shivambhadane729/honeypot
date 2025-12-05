# Product Requirements Document (PRD)
## HoneyTrace - Multi-Layer Honeypot Infrastructure with Real-Time ML-Powered Intrusion Detection

**Version:** 1.0  
**Date:** December 2024  
**Status:** Production Ready  
**Author:** Honeypot Development Team

---

## 1. Executive Summary

### 1.1 Product Overview
HoneyTrace is an advanced multi-layer honeypot system designed to detect, log, enrich, and analyze cyber attack behavior in real-time. It combines traditional honeypot technology with machine learning ensemble-based anomaly detection to provide comprehensive threat intelligence and security monitoring.

### 1.2 Problem Statement
Organizations face increasing cybersecurity threats targeting development infrastructure:
- **Git repositories** are frequently compromised
- **CI/CD pipelines** are exploited for malicious code injection
- **Sensitive credentials** are stolen through automated attacks
- **Zero-day attacks** bypass traditional signature-based detection

Traditional security systems fail to:
- Detect novel attack patterns
- Provide real-time threat intelligence
- Correlate attack data across multiple services
- Offer actionable insights for security teams

### 1.3 Solution
HoneyTrace provides:
- **Deceptive Services**: Fake Git repositories and CI/CD runners that attract attackers
- **Real-Time Detection**: ML ensemble system (Random Forest + Isolation Forest) for immediate threat identification
- **Comprehensive Logging**: Centralized logging with GeoIP enrichment and attack correlation
- **Intuitive Dashboard**: Modern React-based interface for security analysts

### 1.4 Business Value
- **Threat Intelligence**: Understand attacker behavior and tactics
- **Early Warning System**: Detect attacks before they reach production
- **Security Research**: Analyze attack patterns and trends
- **Compliance**: Logging and monitoring capabilities for security audits

---

## 2. Product Goals & Objectives

### 2.1 Primary Goals
1. **Detect Attacks**: Identify malicious activity targeting development infrastructure
2. **Gather Intelligence**: Collect comprehensive data about attacker behavior
3. **Real-Time Analysis**: Provide immediate threat assessment using ML models
4. **User Experience**: Deliver intuitive dashboard for security analysts

### 2.2 Success Metrics
- **Detection Accuracy**: >90% true positive rate for known attacks
- **Anomaly Detection**: >60% accuracy for novel attacks
- **Response Time**: <100ms ML prediction latency per log entry
- **System Uptime**: >99% availability
- **User Satisfaction**: Positive feedback from security team

---

## 3. Target Users

### 3.1 Primary Users
- **Security Analysts**: Monitor threats and investigate incidents
- **Security Engineers**: Configure and maintain the honeypot system
- **Security Researchers**: Analyze attack patterns and trends

### 3.2 User Personas

**Persona 1: Security Analyst (Sarah)**
- **Role**: Monitors security alerts and investigates incidents
- **Needs**: Real-time alerts, easy-to-understand dashboards, detailed investigation tools
- **Pain Points**: Too many false positives, unclear threat context
- **Goals**: Quickly identify and respond to real threats

**Persona 2: Security Engineer (Mike)**
- **Role**: Maintains security infrastructure
- **Needs**: System configuration, model training, API access
- **Pain Points**: Complex setup, difficult troubleshooting
- **Goals**: Keep system running smoothly with minimal maintenance

---

## 4. Functional Requirements

### 4.1 Honeypot Services (FR-1)

#### FR-1.1: Fake Git Repository Service
- **Description**: Simulate a Git server with sensitive files
- **Port**: 8001
- **Endpoints**:
  - `POST /repo/push` - Accept Git push operations
  - `GET /repo/pull` - Accept Git pull operations
  - `GET /repo/.env` - Serve fake environment file
  - `GET /repo/secrets.yml` - Serve fake secrets file
  - `GET /repo/config.json` - Serve fake config file
- **Requirements**:
  - Log all access attempts
  - Generate realistic responses
  - Support multiple concurrent connections
  - Send logs to centralized logging server

#### FR-1.2: Fake CI/CD Runner Service
- **Description**: Simulate CI/CD pipeline execution
- **Port**: 8002
- **Endpoints**:
  - `POST /ci/run` - Accept CI job execution requests
  - `GET /ci/status` - Return fake job status
  - `GET /ci/creds` - Serve fake credentials
  - `GET /ci/logs` - Return fake build logs
- **Requirements**:
  - Simulate realistic CI/CD behavior
  - Log credential access attempts
  - Track job execution patterns
  - Send logs to centralized logging server

#### FR-1.3: Unified Honeypot Service
- **Description**: Combined service for all honeypot operations
- **Port**: 8000
- **Requirements**:
  - Integrate Git and CI/CD functionality
  - Single endpoint for simplified deployment
  - Consistent logging format

### 4.2 Logging & Analytics System (FR-2)

#### FR-2.1: Centralized Logging Server
- **Description**: Receive, enrich, and store all honeypot logs
- **Port**: 5000
- **API Endpoints**:
  - `POST /log` - Ingest log entries
  - `GET /logs` - Retrieve logs (with filtering)
  - `GET /stats` - Get statistics and analytics
  - `GET /health` - Health check endpoint
- **Requirements**:
  - Accept JSON log data from honeypot services
  - Enrich logs with GeoIP data (country, city, ISP, etc.)
  - Store logs in SQLite database
  - Support filtering and pagination
  - Provide real-time statistics

#### FR-2.2: GeoIP Enrichment
- **Description**: Add geographic and network information to logs
- **Data Sources**: ipapi.co API
- **Enriched Fields**:
  - Country
  - City
  - Region
  - Latitude/Longitude
  - Timezone
  - ISP
  - Organization
- **Requirements**:
  - Automatic enrichment on log ingestion
  - Handle API failures gracefully
  - Cache results to reduce API calls

#### FR-2.3: Database Storage
- **Description**: Store all logs with ML predictions
- **Database**: SQLite (`honeypot.db`)
- **Schema Requirements**:
  - Store all log fields (timestamp, source_ip, action, etc.)
  - Store GeoIP enrichment data
  - Store ML prediction results (ml_score, ml_risk_level, is_anomaly)
  - Support efficient querying and indexing
  - Maintain data integrity with hash-based deduplication

### 4.3 Machine Learning System (FR-3)

#### FR-3.1: Model Training System
- **Description**: Train ML models for attack detection
- **Dataset**: UNSW-NB15 (257,673 samples, 45 features)
- **Models**:
  - **Random Forest** (Supervised): 95.35% accuracy
  - **Isolation Forest** (Unsupervised): 61.51% accuracy
- **Requirements**:
  - Support hyperparameter tuning
  - Feature selection and preprocessing
  - Model evaluation and selection
  - Save trained models and preprocessing objects
  - Generate training reports

#### FR-3.2: Real-Time ML Prediction
- **Description**: Apply ML models to incoming logs in real-time
- **Ensemble System**:
  - Weighted combination: 70% Random Forest + 30% Isolation Forest
  - Combines supervised and unsupervised approaches
- **Outputs**:
  - `ml_score`: Combined score (0.0 - 1.0)
  - `ml_risk_level`: MINIMAL, LOW, MEDIUM, HIGH
  - `is_anomaly`: Binary flag (0 or 1)
  - `predicted_attack_type`: Attack classification
- **Requirements**:
  - <100ms prediction latency
  - Automatic scoring on log ingestion
  - Graceful degradation if models unavailable
  - Support model updates without downtime

#### FR-3.3: Attack Classification
- **Description**: Classify attacks by type
- **Attack Types**:
  - EXPLOIT: Git/commit-related attacks
  - BACKDOOR: Credential access attempts
  - DATA_EXFILTRATION: Sensitive file access
  - RECONNAISSANCE: Information gathering
  - HIGH_SEVERITY_ATTACK: High-risk attacks
  - KNOWN_ATTACK: Detected by Random Forest
  - UNKNOWN_ANOMALY: Detected by Isolation Forest
  - NORMAL: No threat detected

### 4.4 Frontend Dashboard (FR-4)

#### FR-4.1: Dashboard Overview Page
- **Description**: Main dashboard with KPIs and charts
- **Features**:
  - Total logs count
  - Unique IPs count
  - Recent activity (24h)
  - Average ML score
  - High-risk attacks count
  - Anomalies detected count
  - Charts: ML score trend, risk distribution, service distribution, actions, countries
  - System overview panel with ML model information
- **Requirements**:
  - Real-time updates (30-second refresh)
  - Responsive design
  - Interactive charts
  - Export functionality

#### FR-4.2: Live Events Page
- **Description**: Real-time stream of honeypot events
- **Features**:
  - Live event feed with auto-refresh
  - Filter by IP, ML score, action, service
  - Sort by timestamp, ML score
  - Expandable event details
  - Color-coded by risk level
- **Requirements**:
  - Real-time updates (10-second refresh)
  - Infinite scroll or pagination
  - Export to CSV

#### FR-4.3: Analytics Page
- **Description**: Statistical analysis and trends
- **Features**:
  - Total attacks and high-risk attacks
  - Unique IPs
  - Average ML score
  - Top countries, ports, IPs
  - Time series of attacks
  - Charts and visualizations
- **Requirements**:
  - Interactive charts
  - Date range filtering
  - Export functionality

#### FR-4.4: Map View Page
- **Description**: Geographic visualization of attacks
- **Features**:
  - World map with attack markers
  - Marker color based on ML score
  - Marker size based on attack count
  - Click markers for details
  - Filter by risk level, country
- **Requirements**:
  - Interactive map (Google Maps or similar)
  - Real-time updates
  - Zoom and pan functionality

#### FR-4.5: ML Insights Page
- **Description**: Dedicated ML model performance and insights
- **Features**:
  - Average anomaly score
  - High-score IPs list
  - Anomaly trend over time
  - Risk level distribution
  - Total anomalies detected
  - Model accuracy metrics
- **Requirements**:
  - Historical performance data
  - Model comparison charts
  - Feature importance visualization

#### FR-4.6: Alerts Page
- **Description**: Alert management and filtering
- **Features**:
  - Alert cards with statistics
  - Filter by risk level, country, service
  - Sort by score, timestamp
  - Expandable alert details
  - CSV export
  - Real-time updates
- **Requirements**:
  - Critical alert notifications
  - Alert acknowledgment
  - Alert resolution tracking

#### FR-4.7: Investigation Page
- **Description**: Deep-dive IP investigation tool
- **Features**:
  - Three-view tabs: Overview, Timeline, Detailed Logs
  - Overview: 6 metric cards, multiple charts
  - Timeline: Chronological event view
  - Detailed Logs: Expandable log entries with full JSON
  - Geographic details with map link
  - CSV export
- **Requirements**:
  - Comprehensive IP analysis
  - Attack pattern visualization
  - Export investigation results

### 4.5 Testing & Simulation (FR-5)

#### FR-5.1: Attack Simulator
- **Description**: Tool to test honeypot with realistic attack scenarios
- **Attack Types**:
  - Git repository attacks (push, clone, fetch)
  - Sensitive file access
  - CI/CD runner attacks
  - Credentials access attempts
  - Brute-force login attempts
  - Malformed payloads
  - Port/endpoint scanning
- **Features**:
  - Configurable attack count
  - Random IP generation
  - Concurrency support
  - Delay configuration
  - CSV export
  - Progress reporting
- **Requirements**:
  - Support 10,000+ attacks per run
  - Realistic attack patterns
  - Multi-threading support
  - Safety warnings

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- **ML Prediction Latency**: <100ms per log entry
- **Database Query Time**: <500ms for standard queries
- **API Response Time**: <1s for most endpoints
- **Frontend Load Time**: <3s initial load
- **Concurrent Connections**: Support 100+ concurrent requests
- **Database Size**: Handle 1M+ log entries efficiently

### 5.2 Scalability Requirements
- **Horizontal Scaling**: Support multiple honeypot service instances
- **Database Scaling**: SQLite can be migrated to PostgreSQL/MySQL for larger deployments
- **ML Model Scaling**: Support model updates without downtime
- **Frontend Scaling**: Static React app can be deployed on CDN

### 5.3 Security Requirements
- **Input Validation**: All API inputs validated and sanitized
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Frontend input sanitization
- **Rate Limiting**: Prevent API abuse
- **Authentication**: Optional API key authentication for production
- **Data Privacy**: No PII collection beyond IP addresses

### 5.4 Reliability Requirements
- **Uptime**: >99% availability
- **Error Handling**: Graceful degradation on failures
- **Logging**: Comprehensive error logging
- **Backup**: Regular database backups
- **Recovery**: Quick recovery from failures

### 5.5 Usability Requirements
- **User Interface**: Intuitive and modern design
- **Documentation**: Comprehensive user and developer documentation
- **Error Messages**: Clear and actionable error messages
- **Responsive Design**: Works on desktop and tablet devices
- **Accessibility**: WCAG 2.1 Level AA compliance (future)

### 5.6 Compatibility Requirements
- **Operating Systems**: Windows 10+, Linux, macOS
- **Python Version**: 3.8+
- **Node.js Version**: 14+
- **Browsers**: Chrome, Firefox, Safari, Edge (latest 2 versions)

---

## 6. Technical Architecture

### 6.1 System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    HoneyTrace System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Honeypot   │    │   Logging    │    │     ML       │ │
│  │   Services   │───►│   Server     │───►│  Ensemble    │ │
│  │  (Ports      │    │  (Port 5000) │    │  Predictor   │ │
│  │  8000-8002)  │    │              │    │              │ │
│  └──────────────┘    └──────┬───────┘    │  • RF (95%)  │ │
│                             │            │  • IF (61%)  │ │
│                             │            │  • Ensemble  │ │
│                             ▼            └──────────────┘ │
│                      ┌──────────────┐                     │
│                      │   Database   │                     │
│                      │  (SQLite)    │                     │
│                      │  + ML Scores │                     │
│                      └──────┬───────┘                     │
│                             │                             │
│                             ▼                             │
│                      ┌──────────────┐                     │
│                      │   Frontend   │                     │
│                      │   Dashboard  │                     │
│                      │  (React)     │                     │
│                      └──────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Technology Stack

#### Backend
- **Python 3.8+**: Primary programming language
- **Flask 2.3.3**: Web framework for logging server
- **SQLite**: Database for log storage
- **scikit-learn**: Machine learning library
- **pandas/numpy**: Data processing
- **requests**: HTTP client for GeoIP API

#### Frontend
- **React 18**: UI framework
- **Chart.js**: Chart library
- **React Router**: Navigation
- **Axios**: HTTP client
- **CSS3**: Styling

#### ML/AI
- **Random Forest**: Supervised learning model (95.35% accuracy)
- **Isolation Forest**: Unsupervised anomaly detection (61.51% accuracy)
- **UNSW-NB15**: Training dataset (257,673 samples)

### 6.3 Data Flow
1. **Attack Detection**: Attacker interacts with honeypot service
2. **Log Generation**: Honeypot service generates log entry
3. **Log Transmission**: Log sent to centralized logging server
4. **GeoIP Enrichment**: Log enriched with geographic data
5. **ML Prediction**: ML ensemble predicts attack probability
6. **Database Storage**: Log and ML results stored in database
7. **Frontend Display**: Dashboard displays data via API

---

## 7. User Stories

### 7.1 Security Analyst Stories
- **As a security analyst**, I want to see real-time alerts for high-risk attacks so I can respond immediately
- **As a security analyst**, I want to investigate specific IP addresses so I can understand attacker behavior
- **As a security analyst**, I want to filter alerts by risk level so I can prioritize my work
- **As a security analyst**, I want to export data to CSV so I can analyze it in Excel

### 7.2 Security Engineer Stories
- **As a security engineer**, I want to start all services with one command so I can deploy quickly
- **As a security engineer**, I want to train new ML models so I can improve detection accuracy
- **As a security engineer**, I want to monitor system health so I can ensure reliability
- **As a security engineer**, I want to configure risk thresholds so I can tune alert sensitivity

### 7.3 Security Researcher Stories
- **As a security researcher**, I want to analyze attack patterns so I can understand trends
- **As a security researcher**, I want to see geographic distribution of attacks so I can identify hotspots
- **As a security researcher**, I want to export logs so I can perform detailed analysis
- **As a security researcher**, I want to see ML model performance so I can evaluate effectiveness

---

## 8. Out of Scope (Future Enhancements)

### 8.1 Not Included in v1.0
- **Authentication/Authorization**: No user authentication system
- **Alert Notifications**: No email/SMS/Slack notifications
- **Blocking Functionality**: No automatic IP blocking
- **Machine Learning Training UI**: No web-based model training interface
- **Multi-Tenancy**: No support for multiple organizations
- **API Rate Limiting**: No rate limiting implementation
- **Data Retention Policies**: No automatic data cleanup
- **Real-Time WebSockets**: Uses polling instead of WebSockets

### 8.2 Future Roadmap
- **v1.1**: Authentication system, alert notifications
- **v1.2**: Web-based ML training interface
- **v1.3**: Automatic IP blocking, rate limiting
- **v2.0**: Multi-tenancy, PostgreSQL support
- **v2.1**: WebSocket real-time updates
- **v2.2**: Advanced analytics and reporting

---

## 9. Acceptance Criteria

### 9.1 Core Functionality
- ✅ All honeypot services run and accept connections
- ✅ Logging server receives and stores all logs
- ✅ ML models load and make predictions
- ✅ Frontend displays all pages correctly
- ✅ All API endpoints respond correctly

### 9.2 ML System
- ✅ Random Forest model achieves >90% accuracy
- ✅ Isolation Forest model achieves >60% accuracy
- ✅ Ensemble predictions combine both models
- ✅ ML scores stored in database
- ✅ Frontend displays ML insights

### 9.3 Frontend
- ✅ All 7 pages render correctly
- ✅ Charts display data accurately
- ✅ Real-time updates work
- ✅ Filtering and sorting work
- ✅ Export functionality works

### 9.4 Testing
- ✅ Attack simulator generates realistic attacks
- ✅ System handles 10,000+ attacks
- ✅ ML predictions trigger on all logs
- ✅ No critical errors in logs

---

## 10. Dependencies & Constraints

### 10.1 External Dependencies
- **ipapi.co**: Free tier for GeoIP enrichment (1000 requests/day)
- **UNSW-NB15 Dataset**: Public dataset for ML training
- **Python Packages**: See requirements.txt and ml_requirements.txt
- **Node.js Packages**: See db1/package.json

### 10.2 Constraints
- **GeoIP API Limits**: 1000 requests/day on free tier
- **SQLite Limitations**: Single-writer constraint for large deployments
- **Memory**: ML models require ~500MB RAM
- **Network**: Requires internet for GeoIP enrichment

### 10.3 Assumptions
- Honeypot runs in isolated/controlled network environment
- Users have Python 3.8+ and Node.js 14+ installed
- Users have basic knowledge of security systems
- System runs on single machine or local network

---

## 11. Risks & Mitigations

### 11.1 Technical Risks
- **Risk**: ML models may have high false positive rate
  - **Mitigation**: Tune thresholds based on real-world data, provide feedback mechanism
- **Risk**: SQLite may not scale for large deployments
  - **Mitigation**: Document migration path to PostgreSQL, optimize queries
- **Risk**: GeoIP API may rate-limit requests
  - **Mitigation**: Implement caching, provide fallback to offline GeoIP database

### 11.2 Security Risks
- **Risk**: Honeypot may be identified by attackers
  - **Mitigation**: Use realistic responses, deploy in production-like environments
- **Risk**: System itself may be attacked
  - **Mitigation**: Run in isolated network, implement security best practices

### 11.3 Operational Risks
- **Risk**: System may become unresponsive under high load
  - **Mitigation**: Implement rate limiting, optimize database queries
- **Risk**: ML models may require frequent retraining
  - **Mitigation**: Provide easy retraining scripts, document process

---

## 12. Success Criteria

### 12.1 Technical Success
- ✅ All services run without errors
- ✅ ML predictions complete in <100ms
- ✅ Frontend loads in <3s
- ✅ System handles 10,000+ logs without issues

### 12.2 Functional Success
- ✅ Detects >90% of known attacks
- ✅ Detects >60% of unknown attacks
- ✅ Dashboard provides actionable insights
- ✅ Users can investigate threats effectively

### 12.3 User Success
- ✅ Security team can monitor threats easily
- ✅ System provides valuable threat intelligence
- ✅ Documentation is clear and comprehensive
- ✅ System requires minimal maintenance

---

## 13. Glossary

- **Honeypot**: A security mechanism designed to attract and trap attackers
- **ML Score**: Machine learning prediction score (0.0-1.0)
- **Risk Level**: Categorized threat level (MINIMAL, LOW, MEDIUM, HIGH)
- **Ensemble**: Combination of multiple ML models for better predictions
- **GeoIP**: Geographic information derived from IP addresses
- **UNSW-NB15**: Network intrusion detection dataset
- **Random Forest**: Supervised ML algorithm using multiple decision trees
- **Isolation Forest**: Unsupervised ML algorithm for anomaly detection

---

## 14. References

- UNSW-NB15 Dataset: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- scikit-learn Documentation: https://scikit-learn.org/
- React Documentation: https://reactjs.org/
- Flask Documentation: https://flask.palletsprojects.com/

---

## 15. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | December 2024 | Development Team | Initial PRD creation |

---

**Status**: ✅ Approved for Production  
**Next Review**: After v1.0 deployment and user feedback

