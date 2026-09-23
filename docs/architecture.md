# AlertX2 System Architecture

```mermaid
flowchart TD
    subgraph Mobile Client [Android Kivy App]
        UI[Kivy Screens & Controls]
        SM[Screen Manager]
        SVC[Client Services Layer]
        NAT[Native JNI & Plyer Hooks]
        LS[Local Persistent Storage]
        
        UI --> SM
        SM --> SVC
        SVC --> NAT
        SVC --> LS
    end

    subgraph Backend Cloud [FastAPI Async Core]
        API[FastAPI REST API /api/v1]
        WS[WebSocket Manager /ws/sos]
        AUTH[JWT Security & Auth]
        ORM[SQLAlchemy 2.0 Async ORM]
        NOTIF[Multi-Channel Notifier]
        BG[Async Background Workers]
        
        API --> AUTH
        API --> ORM
        WS --> ORM
        API --> NOTIF
        BG --> ORM
    end

    subgraph Storage & Infrastructure
        DB[(SQLite / PostgreSQL DB)]
        TEL[Twilio SMS & Voice Gateway]
        MAPS[Google Maps Geocoding]
    end

    SVC -->|REST HTTPS| API
    SVC -->|Bidirectional Telemetry| WS
    ORM --> DB
    NOTIF --> TEL
    API --> MAPS
```

## System Components

1. **Android Client (`android/`)**:
   - Built on Kivy and KivyMD for cross-platform modern mobile interfaces.
   - Utilizes `plyer` and Android Native JNI wrappers to access hardware sensors, GPS telemetry, SMS dispatch, and audio recording.
   - Offline-resilient with local persistent caching.

2. **Backend Engine (`backend/`)**:
   - Asynchronous FastAPI ASGI framework.
   - Real-time bi-directional WebSocket broadcasting for continuous live location streams.
   - High-throughput database layer via SQLAlchemy async engine supporting PostgreSQL and SQLite.

3. **External Services**:
   - Twilio Telephony for immediate emergency SMS alerts and automated emergency voice calls.
   - Google Maps for reverse geocoding and live navigation URLs.
