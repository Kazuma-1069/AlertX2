# AlertX — Public Safety Application

> **Safety when you need it most.**

AlertX is a production-quality Android public safety application built with Python, Kivy, and KivyMD. It provides instant SOS activation, live location sharing, emergency contact management, safety timers, offline emergency guides, evidence recording, and community safety reporting.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start (Backend)](#quick-start-backend)
- [Quick Start (Android Build)](#quick-start-android-build)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Security](#security)
- [Testing](#testing)
- [Permissions](#android-permissions)
- [Design System](#design-system)

---

## Features

### 🚨 Instant SOS (Zero Countdown)
- **1-tap SOS button** — Immediately enters emergency state with no delay
- **5-tap rapid detector** — Sliding-window algorithm activates SOS from anywhere in the app
- **Offline-first state machine** — SOS state persists across app restarts
- Automatically: acquires GPS, calls priority-1 contact, SMS-broadcasts all emergency contacts, syncs to backend

### 📍 Live Location Sharing
- Real-time location breadcrumbs during active SOS
- Secure public tracking link with opaque token (no user ID exposed)
- Tracking session auto-created on SOS activation

### 👥 Emergency Contacts
- Priority-ordered contacts (1 = highest priority, called first)
- Per-contact toggles: `receive_sos`, `receive_location`, `receive_checkin_alert`
- Full CRUD with backend sync + local cache for offline

### ⏱️ Safety Timer & Check-In
- Custom countdown timer (5m / 15m / 30m / 1h presets or manual)
- Auto-escalates to SOS on expiry if not dismissed
- Fake call feature to safely exit dangerous situations

### 📖 Emergency Guides (Offline)
- CPR, Earthquake, Fire, First Aid, Flood, Heimlich
- Available fully offline — no network required
- Searchable by category

### 🎥 Evidence Vault
- Audio recording during emergencies
- Photo evidence capture
- Upload to backend with PENDING/UPLOADED/FAILED status tracking
- Local export of full incident report as JSON

### 🏘️ Community Reporting
- Report: ACCIDENT, FIRE, ROAD_HAZARD, UNSAFE_LOCATION, FLOODING, OTHER
- GPS-tagged reports
- Offline queue — retries when network available

### 🏥 Medical Profile
- Blood group, allergies, medications, emergency conditions, doctor contacts
- Optional sharing with emergency responders
- Stored locally + synced to backend

---

## Architecture

```
AlertX
├── android/               # Kivy/KivyMD Android app (Python)
│   ├── main.py            # App entrypoint + ScreenManager
│   ├── buildozer.spec     # Build configuration for APK
│   ├── app/
│   │   ├── config/        # Theme tokens (Stitch design system)
│   │   ├── screens/       # All UI screens
│   │   ├── components/    # Reusable widgets (SOSButton, BottomNav)
│   │   ├── services/      # SOS service, API client
│   │   ├── state/         # Emergency state machine (SOSState FSM)
│   │   ├── native/        # Android-native: calls, SMS (PyJNIus + Plyer)
│   │   └── utils/         # LocalStore, logger, tap detector, validators
│   ├── kv/                # KV layout files (one per screen)
│   └── tests/             # Android unit tests (pytest)
│
└── backend/               # FastAPI Python backend
    ├── app/
    │   ├── api/v1/        # REST endpoints
    │   ├── core/          # Config, DB, security (JWT + bcrypt)
    │   ├── models/        # SQLAlchemy ORM models
    │   ├── repositories/  # Data access layer
    │   ├── schemas/       # Pydantic request/response schemas
    │   └── services/      # Business logic
    └── tests/             # Backend unit tests (pytest)
```

---

## Technology Stack

### Android App
| Component | Technology |
|-----------|-----------|
| Language | Python 3.12 |
| UI Framework | Kivy 2.3 + KivyMD 1.2 |
| Android Integration | PyJNIus (direct Android API calls) |
| Device APIs | Plyer (GPS, SMS fallback, camera, audio) |
| Build System | Buildozer + python-for-android |
| Local Storage | JSON-backed LocalStore |

### Backend
| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL (prod) / SQLite (dev) |
| ORM | SQLAlchemy (async) |
| Auth | JWT (python-jose) + bcrypt |
| Migrations | Alembic |
| Real-time | WebSockets |

---

## Project Structure

```
android/
├── main.py
├── buildozer.spec
├── app/
│   ├── config/
│   │   └── theme.py              # Stitch design tokens
│   ├── screens/
│   │   ├── splash.py             # Splash screen
│   │   ├── onboarding.py         # First-launch onboarding
│   │   ├── auth.py               # Login / register
│   │   ├── home.py               # Home (SOS button, quick actions)
│   │   ├── emergency.py          # Active SOS emergency view
│   │   ├── safety.py             # Safety timer + check-in
│   │   ├── guides.py             # Emergency guide list
│   │   ├── guide_detail.py       # Full guide reader
│   │   ├── contacts.py           # Emergency contact management
│   │   ├── profile.py            # Medical profile + SOS settings
│   │   ├── incident.py           # SOS incident history
│   │   ├── incident_detail.py    # Incident timeline + evidence vault
│   │   ├── community.py          # Community safety reporting
│   │   ├── fake_call.py          # Fake incoming call (escape tool)
│   │   └── nearby.py             # Nearby emergency services
│   ├── components/
│   │   ├── sos_button.py         # SOSButton widget
│   │   └── bottom_navigation.py  # 5-tab bottom nav
│   ├── services/
│   │   └── sos_service.py        # Instant SOS orchestration
│   ├── state/
│   │   └── emergency_state.py    # SOSState FSM (SAFE→ACTIVE→RESOLVED)
│   ├── native/
│   │   ├── android_calls.py      # PyJNIus phone call + Plyer fallback
│   │   └── android_sms.py        # SmsManager broadcast + Plyer fallback
│   └── utils/
│       ├── tap_detector.py       # FiveTapDetector (sliding window)
│       ├── storage.py            # LocalStore (JSON persistence)
│       ├── local_store.py        # Alias for storage.py
│       ├── logger.py             # Structured logger
│       ├── validators.py         # Input validation
│       └── permissions.py       # Runtime Android permission helper
├── kv/
│   ├── home.kv
│   ├── emergency.kv
│   ├── safety.kv
│   ├── guides.kv
│   ├── guide_detail.kv
│   ├── contacts.kv
│   ├── profile.kv
│   ├── incident.kv
│   ├── incident_detail.kv
│   ├── community.kv
│   ├── fake_call.kv
│   ├── auth.kv
│   ├── splash.kv
│   └── onboarding.kv
└── tests/
    ├── test_sos.py
    ├── test_tap_detector.py
    ├── test_contacts.py
    ├── test_location.py
    └── test_safety.py

backend/
├── app/
│   ├── api/v1/
│   │   ├── auth.py
│   │   ├── sos.py
│   │   ├── contacts.py
│   │   ├── safety.py
│   │   ├── guides.py
│   │   ├── tracking.py
│   │   ├── evidence.py
│   │   ├── reports.py
│   │   └── location.py
│   ├── core/
│   │   ├── config.py             # Env-var settings
│   │   ├── database.py           # Async SQLAlchemy engine
│   │   └── security.py           # JWT + bcrypt (direct)
│   ├── models/                   # All SQLAlchemy models
│   ├── repositories/             # Repository pattern (data access)
│   ├── schemas/                  # Pydantic schemas
│   └── services/                 # Business logic services
├── tests/                        # 10 pytest tests
├── alembic/                      # DB migrations
└── requirements.txt
```

---

## Quick Start (Backend)

### Prerequisites
- Python 3.12+
- PostgreSQL (or use SQLite for development — automatic fallback)

### Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate        # Linux/macOS

# Install dependencies
pip install fastapi uvicorn sqlalchemy aiosqlite asyncpg python-jose bcrypt \
            python-multipart websockets pytest pytest-asyncio email-validator httpx

# Configure environment (optional — defaults to SQLite in dev)
copy .env.example .env
# Edit .env: set DATABASE_URL, SECRET_KEY, etc.

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Verify
```bash
curl http://localhost:8000/health
# → {"status":"healthy","service":"ALERTX","version":"2.0.0"}

curl http://localhost:8000/health/database
# → {"status":"healthy","database":"connected"}
```

---

## Quick Start (Android Build)

### Prerequisites (Linux/WSL recommended for Buildozer)
- Python 3.10+ (Buildozer requires Linux)
- Java JDK 17
- Android SDK/NDK (Buildozer downloads automatically)

```bash
# Install Buildozer
pip install buildozer

cd android/

# First build (downloads SDK/NDK — takes ~20 minutes)
buildozer android debug

# Deploy to connected device
buildozer android deploy run logcat
```

> **Windows Users**: Use WSL2 (Ubuntu) for Buildozer. The Python source and KV files are fully cross-platform.

---

## Configuration

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./alertx.db` | Database connection string |
| `SECRET_KEY` | `change-me-in-production` | JWT signing key |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiry |
| `ENVIRONMENT` | `development` | `development` or `production` |

### Android Config

Edit `android/app/utils/constants.py` to set:
- `API_BASE_URL` — backend URL (default: `http://10.0.2.2:8000` for Android emulator)
- `SOS_TAP_COUNT` — taps for 5-tap detector (default: 5)
- `SOS_TAP_WINDOW` — window in seconds (default: 1.5)

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login → JWT token |

### SOS
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sos` | Trigger SOS (idempotent via `X-Idempotency-Key` header) |
| POST | `/api/v1/sos/resolve` | Resolve active SOS |
| GET | `/api/v1/sos/active` | Get active incident |

### Tracking (Public — no auth)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tracking/{secure_token}` | Public tracking view (strips PII) |

### Contacts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/contacts` | List contacts (priority ordered) |
| POST | `/api/v1/contacts` | Add contact |
| PUT | `/api/v1/contacts/{id}` | Update contact |
| DELETE | `/api/v1/contacts/{id}` | Delete contact |

### Safety
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/safety/timer` | Start safety timer |
| POST | `/api/v1/safety/timer/cancel` | Cancel timer |
| POST | `/api/v1/safety/checkin` | Create check-in |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/reports` | Submit community report |
| GET | `/api/v1/reports` | List own reports |

### Evidence
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/evidence` | Upload evidence metadata |
| GET | `/api/v1/evidence/{incident_id}` | List incident evidence |

---

## Security

- **JWT tokens** — HS256, configurable expiry
- **bcrypt** password hashing (direct library — not passlib, due to bcrypt 5.x compatibility)
- **SOS idempotency** — `X-Idempotency-Key` header prevents duplicate incidents on retry
- **Secure tracking tokens** — `secrets.token_urlsafe(32)` — never expose internal IDs
- **Public tracking view** strips: `user_id`, medical info, internal DB IDs, private notes
- **Emergency contact fields** controlled per-contact: `receive_sos`, `receive_location`, `receive_checkin_alert`
- **No hardcoded secrets** — all via environment variables

---

## Testing

### Run All Tests
```bash
cd backend
.\venv\Scripts\pytest.exe tests\ ..\android\tests\ -v
```

### Backend Tests (10 tests)
```
test_auth.py::test_password_hashing         PASSED
test_auth.py::test_token_creation           PASSED
test_contacts.py::test_contact_schema       PASSED
test_guides.py::test_safety_guide_schema    PASSED
test_incidents.py::test_incident_summary    PASSED
test_location.py::test_breadcrumb_payload   PASSED
test_safety.py::test_safety_timer_schema    PASSED
test_security.py::test_jwt_tampering_fails  PASSED
test_sos.py::test_sos_trigger_request       PASSED
test_tracking.py::test_tracking_placeholder PASSED
```

### Android Tests (7 tests)
```
test_contacts.py::test_contact_model              PASSED
test_location.py::test_native_location_fallback   PASSED
test_safety.py::test_safety_timer_model           PASSED
test_sos.py::test_emergency_state_initial         PASSED
test_sos.py::test_state_transitions               PASSED
test_tap_detector.py::test_five_tap_success       PASSED
test_tap_detector.py::test_slow_taps_no_trigger   PASSED
```

---

## Android Permissions

| Permission | Required For |
|-----------|-------------|
| `ACCESS_FINE_LOCATION` | GPS during SOS |
| `ACCESS_BACKGROUND_LOCATION` | Location tracking while screen off |
| `SEND_SMS` | SMS to emergency contacts |
| `CALL_PHONE` | Auto-call priority contact |
| `RECORD_AUDIO` | Evidence recording |
| `CAMERA` | Photo evidence |
| `INTERNET` | Backend sync |
| `FOREGROUND_SERVICE` | Background SOS service |
| `VIBRATE` | SOS alerts |
| `READ_CONTACTS` | Import from phonebook |

---

## Design System

AlertX follows the **Stitch AlertX design system**. All UI tokens are defined in [`android/app/config/theme.py`](android/app/config/theme.py):

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#0D1117` | App background |
| Surface | `#161B22` | Cards, drawers |
| Accent Red | `#D92D20` | SOS button, critical actions |
| Accent Amber | `#E9A319` | Safety timer, warnings |
| Text Primary | `#F0F6FC` | Headlines |
| Text Secondary | `#8B949E` | Subtitles, metadata |
| Border | `#30363D` | Card borders, dividers |
| Success | `#2EA043` | Resolved status |

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

*AlertX — Built to protect people in their most vulnerable moments.*
