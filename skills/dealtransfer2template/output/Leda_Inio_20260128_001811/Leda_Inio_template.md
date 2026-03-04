# Video Analytics Solution Proposal for Leda Inio

**Date:** January 28, 2026

---

## 2. PROJECT REQUIREMENT STATEMENT

**Project:** AI-Powered Video Analytics for Workplace Safety Compliance and Incident Prevention

**Project Owner:** Leda Inio

**Work Scope:** On-premise AI system to monitor workplace safety compliance and prevent accidents in real time

**Project Duration:** 6 months

**Camera Number:** 9 cameras

**AI Modules per Camera:** 7 modules per camera

**AI Modules:**
1. Safety Helmet Detection
2. Safety Mask Detection
3. Safety Vest Detection
4. Fire & Smoke Detection
5. Anti-collision Detection
6. Intrusion detection (Danger zone)
7. Human Down Detection

---

## 3. SCOPE OF WORK

### viAct Responsibilities
- AI software licensing and deployment
- System integration with existing 9 IP cameras
- AI model training and optimization
- Software maintenance and technical support
- User training and documentation
- System configuration and calibration

### Client Responsibilities
- Provide access to existing 9 IP cameras with RTSP links
- Ensure stable power supply for cameras
- Provide stable internet connection for system access
- Server room or designated space for on-premise workstation installation
- Local IT infrastructure setup and network configuration
- On-site coordination during installation and testing

---

## 4. SYSTEM ARCHITECTURE

**Deployment Model:** On-Premise

### Architecture Overview
- **Video Ingestion:** 9 IP cameras stream video via RTSP protocol to on-premise AI server
- **AI Processing:** Edge AI inference workstation processes all camera streams locally
- **Data Storage:** All video footage and alert data stored on-premise
- **User Access:** Web-based dashboard accessible via local network
- **Alert System:** Real-time alerts via Dashboard, Email, and Telegram

### System Components
1. **AI Inference Workstation:** Processes all 9 camera streams with 7 AI modules
2. **Dashboard Workstation:** For monitoring, alert management, and reporting
3. **Network Infrastructure:** Local network switches, cabling, and router
4. **Backup Storage:** Network-attached storage for video retention

---

## 5. SYSTEM REQUIREMENTS

### Network Requirements

**Local Network Bandwidth:**
- **Per-Camera Bandwidth:** 12 Mbps/camera
- **Total System Bandwidth:** 108 Mbps [NETWORK_001]

**Internet Connection:**
- **Minimum Upload Speed:** 50 Mbps [NETWORK_002]
- **Purpose:** Remote dashboard access, email/Telegram alerts, software updates

### Camera Requirements

**Minimum Specifications:**
- **Resolution:** 1080p (1920×1080) minimum @ 25fps
- **Connectivity:** IP-based with RTSP stream support
- **Quantity:** 9 cameras (already installed)

**Camera Positioning:**
- Mount cameras at appropriate height and angle for clear visibility
- Ensure adequate lighting conditions
- Avoid obstructions and blind spots

### AI Inference Workstation

**Recommended Specifications:**

| Component | Specification | Quantity |
|-----------|---------------|----------|
| **CPU** | Intel Core i7 or AMD Ryzen 7 (8+ cores) | 1 |
| **GPU** | NVIDIA RTX 4070 Super (12GB VRAM) | 1 |
| **RAM** | 32GB DDR4/DDR5 | 1 |
| **Storage** | 1TB NVMe SSD (OS + Applications) | 1 |
| **Storage** | 4TB HDD (Video Storage) [STORAGE_001] | 1 |
| **Network** | 10GbE Network Card | 1 |
| **Operating System** | Ubuntu 22.04 LTS | 1 |
| **Power Supply** | 750W 80+ Gold Certified | 1 |

**Justification:** Supports 9 cameras × 7 AI modules = 63 AI Load Index (ALI), well within capability of RTX 4070 Super.

### Dashboard Workstation

**Recommended Specifications:**

| Component | Specification | Quantity |
|-----------|---------------|----------|
| **CPU** | Intel Core i5 or AMD Ryzen 5 (6+ cores) | 1 |
| **RAM** | 16GB DDR4/DDR5 | 1 |
| **Storage** | 500GB SSD | 1 |
| **Network** | 1GbE Network Card | 1 |
| **Operating System** | Windows 10/11 or Ubuntu 22.04 LTS | 1 |
| **Monitor** | 24" Full HD (1920×1080) | 2 |

**Note:** No GPU required for dashboard workstation (viewing and management only).

### Power Requirements

- **Stable Power Source:** Required (client confirmed availability)
- **UPS Recommendation:** 1500VA UPS for AI inference workstation [POWER_001]
- **Power Backup:** Minimum 30 minutes backup for safe shutdown

---

## 6. IMPLEMENTATION PLAN (TIMELINE)

### Project Phases

| Phase | Description | Duration | Start Date | End Date |
|-------|-------------|----------|------------|----------|
| **T0** | Project Award / Contract Signed | — | [DATE_001] | [DATE_001] |
| **T1** | Hardware Deployment & Verification | 2 weeks | [DATE_001] | [DATE_002] |
| **T2** | Software Deployment & Configuration | 6 weeks | [DATE_002] | [DATE_003] |
| **T3** | Integration, Testing & UAT | 4 weeks | [DATE_003] | [DATE_004] |

### Phase Details

**T0: Project Award**
- Contract signing and project kickoff
- Technical team assignment
- Project planning and scheduling

**T1: Hardware Deployment & Verification** (2 weeks)
- Verify existing 9 IP camera functionality and RTSP access
- Install AI inference workstation and dashboard workstation
- Network configuration and testing
- Power and UPS setup verification
- Camera positioning optimization assessment

**T2: Software Deployment & Configuration** (6 weeks)
- Install AI software platform on on-premise servers
- Configure all 7 AI modules for 9 cameras
- Integrate with client's RTSP camera streams
- Set up alert channels (Dashboard, Email, Telegram)
- Initial calibration and tuning

**T3: Integration, Testing & UAT** (4 weeks)
- System integration testing
- User acceptance testing (UAT) with client stakeholders
- Fine-tune AI detection accuracy based on site conditions
- User training and handover documentation
- Project sign-off

**Total Project Duration:** 12 weeks (~3 months)

**Note:** The stated project duration is 6 months (S1), which includes buffer for potential delays, additional iterations, and extended support period.

---

## 7. PROPOSED MODULES & FUNCTIONAL DESCRIPTION

### Module 1: Safety Helmet Detection

**Module Type:** Standard

**Purpose Description:** Ensures compliance with safety regulations by identifying workers wearing safety helmets. Detects workers without a safety helmet on the construction site.

**Alert Trigger Logic:** AI will capture people not wearing a helmet or wearing the helmet, and trigger the real-time alerts.

**Detection Criteria:** Identifies workers with and without safety helmets in monitored areas.

**Preconditions:** Camera must maintain a suitable distance for clear observation of workers, typically between 5 to 10 meters.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1adkUPBJaBPbUVdirflpQwFOVai84p4k2/view?usp=sharing

---

### Module 2: Safety Mask Detection

**Module Type:** Standard

**Purpose Description:** Detects the use of protective masks where respiratory protection is required

**Alert Trigger Logic:** AI alerts when workers are not wearing required masks in controlled zones.

**Detection Criteria:** Identifies workers with and without safety masks in designated areas.

**Preconditions:** Camera must have clear facial visibility; angle must avoid obstructions.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1abtNV_P-CW-14tH7WY1oQ7Iok4BLTr0M/view?usp=sharing

---

### Module 3: Safety Vest Detection (Hi-vis vest detection)

**Module Type:** Standard

**Purpose Description:** Detects workers wearing high-visibility vests. These vests enhance visibility, especially in low-light conditions.

**Alert Trigger Logic:** Alert will be sent out immediately to remind workers missing a reflective vest. AI identifies missing vests and notifies in real time.

**Detection Criteria:** Identifies workers wearing or missing high-visibility vests.

**Preconditions:** Camera must maintain a suitable distance for clear observation of workers, typically between 5 to 10 meters.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1adkUPBJaBPbUVdirflpQwFOVai84p4k2/view?usp=sharing

---

### Module 4: Fire & Smoke Detection

**Module Type:** Standard

**Purpose Description:** Detects situations where fire or smoke is present in the monitored area, ensuring early intervention and safety compliance

**Alert Trigger Logic:** Automatically triggers an alert when fire or smoke is detected in the area, enabling quick response and mitigation actions.

**Detection Criteria:** Identifies visual indicators of fire or smoke in monitored areas.

**Preconditions:** Camera must directly face the work area, allowing a clear view of the work area – the area prone to fire hazards.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1hR2FZrlMhmPXq2qvbWm0D7uKZ6KDhtkc/view?usp=sharing

---

### Module 5: Anti-collision Detection

**Module Type:** Standard

**Purpose Description:** Detect and identify potential or actual workers dangerously close to moving machinery within 100 cm (3 feet) and between workers.

**Alert Trigger Logic:** Automatically triggers an alert when a near-miss from 100cm or a collision occurs.

**Detection Criteria:** Monitors proximity between workers and moving vehicles/machinery.

**Preconditions:** Requires providing images of different vehicle types for model training.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1h50cgHZ0qhxEdUoFLtnSUbxvAgGzX_YR/view?usp=sharing

---

### Module 6: Intrusion detection (Danger zone)

**Module Type:** Standard

**Purpose Description:** Alerts for unauthorized entry into restricted zones (e.g., construction sites, secure facilities). Enhances security and prevents unauthorized access.

**Alert Trigger Logic:** Alarms trigger if someone enters without authorization.

**Detection Criteria:** Identifies personnel entering designated danger zones or restricted areas.

**Preconditions:** Cameras cover perimeter areas, continuously monitoring for intruders.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1nOg_F26X5p00VwunI7vxq2NC3f3ENK2G/view?usp=sharing

---

### Module 7: Human Down Detection

**Module Type:** Standard

**Purpose Description:** Detects worker falls or immobility.

**Alert Trigger Logic:** AI will capture a worker's fall and inform immediately.

**Detection Criteria:** Identifies workers who have fallen or are immobile on the ground.

**Preconditions:** Camera must maintain a suitable distance for clear observation of workers, typically between 5 to 10 meters.

**Image URL:**

**Video URL:** https://drive.google.com/file/d/1td7wDI3hPH50adRF2SzcfxalXl_h7vw_/view?usp=sharing

---

## 8. USER INTERFACE & REPORTING

*Note: This section is skipped as there are no custom dashboard requirements beyond standard features.*

---

## SUPPORTING INFORMATION

### Compliance & Security

**Data Privacy:**
- No GDPR or specific data privacy requirements (S2 confirmed)
- All data stored on-premise, ensuring client retains full control

**Security Measures:**
- User authentication with role-based access control
- Encrypted data transmission (HTTPS/TLS)
- Secure remote access via VPN (if required)
- Regular security updates and patches

---

### Alert & Notification Channels

**Standard Alert Channels:**
1. **Dashboard:** Real-time alerts and notifications on web interface
2. **Email:** Immediate email alerts to designated personnel
3. **Telegram:** Instant push notifications to mobile devices

**Alert Information:**
- Timestamp and location
- Snapshot image of event
- Short video clip (15 seconds before to 10 seconds after)
- Severity level classification

---

### Reporting Features

**Standard Reports:**
- Daily summary of all alerts and events
- Weekly trend analysis and compliance reports
- Custom date range reports
- Export to Excel and PDF formats
- Evidence snapshots and video clips attached

**Dashboard Features:**
- Real-time monitoring of all 9 cameras
- Live alert timeline and event feed
- Multi-view camera grid display
- Historical event search and filtering
- User-defined alert rules and thresholds

---

## IMPLEMENTATION ASSUMPTIONS

1. **Camera Status:** Client has 9 IP cameras already installed and functional (S1 confirmed)
2. **Network Infrastructure:** Client has local network infrastructure to support 108 Mbps bandwidth
3. **Internet Connectivity:** Stable internet connection available for remote access and alerts (S2 confirmed)
4. **Power Supply:** Stable power source available (S2 confirmed)
5. **Server Room:** Designated space with adequate cooling and ventilation for workstation installation
6. **No Custom Requirements:** No custom AI use cases, dashboards, or hardware integrations (S2 confirmed)

---

## APPENDIX

### Glossary

- **AI:** Artificial Intelligence
- **RTSP:** Real Time Streaming Protocol
- **PPE:** Personal Protective Equipment
- **UAT:** User Acceptance Testing
- **ALI:** AI Load Index (Cameras × Modules per Camera)
- **UPS:** Uninterruptible Power Supply

---

*End of Proposal*
