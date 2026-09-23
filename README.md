# AlertX2 - Personal Safety & Emergency Response System

[![CI - Backend Tests](https://github.com/AlertX/AlertX2/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/AlertX/AlertX2/actions)
[![Build Check](https://github.com/AlertX/AlertX2/actions/workflows/build-check.yml/badge.svg)](https://github.com/AlertX/AlertX2/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**AlertX2** is a mission-critical personal safety and emergency response platform built for immediate, real-time protection. It couples a mobile Android application (developed with Kivy / Buildozer) with an asynchronous FastAPI backend service, enabling instantaneous SOS triggers, live location streaming, automated emergency SMS & voice calling, offline resiliency, and AI-assisted safety guidance.

---

## Key Features

- **Instant SOS Dispatch**: Single-tap and hardware trigger activation with countdown abort windows.
- **Real-Time Geolocation Tracking**: Continuous breadcrumb updates transmitted over WebSockets to emergency contacts and backend observers.
- **Multi-Channel Alerting**: Automated emergency dispatch through SMS, voice calling (IVR alert), and WhatsApp.
- **Safety Timers & Check-ins**: Automated countdown timers (e.g. for walking home alone or meeting someone new) requiring pin confirmation before triggering alerts.
- **First Aid & Safety Guides**: Offline-available interactive step-by-step guides for medical emergencies and natural disasters.
- **Evidence Vault**: Secure local and cloud capture of audio logs and incident telemetry.
- **AI Safety Assistant**: Instant context-aware guidance during critical situations.

---

## Repository Layout

```
AlertX2/
├── android/            # Kivy/KivyMD mobile application with Android native bindings
│   ├── app/            # Screens, components, services, models, native wrappers, state
│   ├── kv/             # Kivy declarative UI layouts
│   ├── assets/         # App icons, illustrations, and images
│   ├── buildozer.spec  # Android APK packaging config
│   └── tests/          # Client-side unit tests
├── backend/            # FastAPI async backend service
│   ├── app/            # Core config, models, schemas, services, API routers, WebSockets
│   ├── alembic/        # Database migrations
│   ├── tests/          # Pytest suite
│   └── Dockerfile      # Containerization configuration
├── docs/               # System architecture, API documentation, and security specs
├── scripts/            # Development, deployment, and build scripts
└── .github/workflows/  # CI/CD pipelines
```

---

## Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Android App (Development Mode)

```bash
cd android
pip install -r requirements.txt
python main.py
```

### 3. Build Android APK

```bash
cd android
buildozer -v android debug
```

---

## Documentation

- [System Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Database Schema & ERD](docs/database.md)
- [SOS State Flow](docs/sos-flow.md)
- [Security & Threat Model](docs/security.md)
- [Android Integration Guide](docs/android-integration.md)
- [Production Deployment](docs/deployment.md)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
