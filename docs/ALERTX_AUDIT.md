# ALERTX System Audit & Architectural Assessment

**Application Name**: ALERTX  
**Tagline**: *Safety when you need it most.*  
**Date**: September 23, 2026  
**Auditor**: Lead Software Engineer  

---

## 1. Executive Summary

This audit assesses the current codebase against the specifications for **AlertX**, a mission-critical public safety platform combining a **Kivy/KivyMD** Android client with a **FastAPI / PostgreSQL** asynchronous backend, adhering strictly to the **Stitch design system source of truth** (`stitch_alertx_safety_app_ui`).

The previous scaffolding established the directory layout, basic models, mock services, and initial API routers. However, to meet real production standards and eliminate all placeholders, significant upgrades are required:
1. **Core SOS Activation**: Must remove any countdown on one-tap SOS; implement an instant local SOS state machine (`SAFE -> SOS_ACTIVATING -> SOS_ACTIVE -> SOS_RESOLVING -> SOS_RESOLVED / SOS_CANCELLED`), plus real 5-tap power key detection.
2. **Database Architecture**: Must strictly align with Section 8 schemas (`User`, `EmergencyContact`, `SOSIncident`, `TrackingSession`, `SafetyTimer`, `CheckIn`, `IncidentEvent`, `MedicalProfile`, `Evidence`, `CommunityReport`) with native PostgreSQL support, foreign keys, indexes, and Alembic migrations.
3. **Stitch Visual System**: The UI must be refactored into the 5 primary navigation tabs (`Home`, `Safety`, `Guides`, `Contacts`, `Profile`) using the exact color tokens (`#111316` surface, `#1E2023` container, `#D92D20` emergency red, `#8BCEFF` tracking blue, `#F79009` warning amber, `#12B76A` safe green) and typography matching `stitch_alertx_safety_app_ui/alertx_safety_core/DESIGN.md`.
4. **Offline Resilience & Priority Calling**: Core SOS and local state must operate independently of backend connectivity, queuing synchronization, and managing priority phone calls (Priority 1 -> 2 -> 3) through Android native telephony hooks.

---

## 2. Feature-by-Feature Technical Audit Table

| Feature | UI | Backend | Database | Android Native | Functional | Problems | Files |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Instant 1-Tap SOS** | Basic MD button | Basic endpoint | Basic incident model | Basic mock call | Partial | Previous version had an abort countdown; spec requires **immediate** local activation, acquiring GPS, incident creation, priority call attempt, and offline queueing without delay. | `android/app/screens/home.py`, `android/app/services/sos_service.py`, `backend/app/api/v1/sos.py`, `backend/app/models/sos_incident.py` |
| **5-Tap SOS Detector** | Toggle chip in Home | Endpoint accepts type | Stores `trigger_type` | None (Mocked) | Incomplete | Needs touch event and rapid tap detector with configurable max interval (default ~1.5s total window) that triggers the core SOS state machine. | `android/app/utils/tap_detector.py`, `android/app/screens/home.py` |
| **Local SOS State Machine** | Emergency screen | Updates status | Stores status string | None | Partial | Needs strict local state machine (`SAFE`, `SOS_ACTIVATING`, `SOS_ACTIVE`, `SOS_RESOLVING`, `SOS_RESOLVED`, `SOS_CANCELLED`) with state persistence in `local_store` for network loss. | `android/app/state/emergency_state.py`, `android/app/services/sos_service.py` |
| **Emergency Contacts & Priorities** | Simple list card | CRUD endpoints | Missing priority index | PyJNIus / Plyer call/SMS hooks | Partial | Needs explicit priority order (Priority 1 -> Contact A, Priority 2 -> Contact B), checkboxes for `receive_sos`, `receive_location`, `receive_checkin_alert`, and cascading call logic. | `android/app/screens/contacts.py`, `backend/app/models/contact.py`, `backend/app/schemas/contact.py` |
| **Live Tracking & WebSockets** | Simple text/link | WebSocket router & manager | Breadcrumbs table | GPS polling hook | Partial | Needs opaque secure token generation (`TrackingSession`), rate-limiting coordinate commits in PostgreSQL, public read-only responder view. | `backend/app/models/tracking_session.py`, `backend/app/websocket/sos_tracking.py`, `backend/app/api/v1/tracking.py` |
| **Safety Timer & Missed Check-in** | Single input button | Create/cancel endpoints | Basic timer model | System alarm / timer | Partial | Needs presets (5m, 15m, 30m, 1h, custom), countdown bar, automatic escalation to emergency contacts upon expiry with last known location. | `android/app/screens/safety.py`, `backend/app/models/safety_timer.py`, `backend/app/services/safety_service.py` |
| **Fake Call** | Missing in UI | N/A (Client tool) | N/A | Android Audio/Ringtone | Missing | Needs fake incoming call screen, customizable caller name/number, delayed trigger timer, and accept/decline audio playback. | `android/app/screens/fake_call.py`, `android/app/native/android_calls.py` |
| **Nearby Help & Safe Zones** | List of mock places | Not integrated | N/A | Location distance calc | Partial | Needs dynamic distance calculation based on current GPS coordinates to nearest police stations, hospitals, and fire precincts with direct 1-tap dial. | `android/app/screens/nearby.py`, `android/app/services/maps_service.py` |
| **Emergency Guides & First Aid** | Basic button list | Seed endpoint | Guide model with JSON | Offline local cache | Partial | Needs structured offline database for Medical (CPR, choking, bleeding), Environment (earthquake, fire, flood), and Personal Safety (assault, stalker), with step-by-step navigation. | `android/app/screens/guides.py`, `backend/app/models/guide.py`, `stitch_alertx_safety_app_ui/emergency_guides_first_aid/` |
| **AI Safety Assistant** | None in UI | Rule-based endpoint | None | None | Partial | Needs chat UI on mobile, non-diagnostic safety guidance, contextual tips, and explicit disclaimers; must never block core SOS. | `android/app/screens/assistant.py`, `backend/app/services/ai_service.py` |
| **Medical Profile** | Profile KV inputs | Profile upsert | MedicalProfile table | Local private storage | Partial | Needs blood group, allergies, medications, emergency physician, explicit privacy sharing toggles; never exposed on public tracking links. | `android/app/screens/profile.py`, `backend/app/models/medical_profile.py` |
| **Incident Evidence Vault** | None in UI | Upload endpoints | Evidence table | Native mic recording | Partial | Ambient audio capture during active SOS, local WAV/MP4 storage, auto-sync when network returns, checksum verification. | `android/app/native/android_recording.py`, `backend/app/models/evidence.py`, `backend/app/services/evidence_service.py` |
| **Community Safety Reporting** | None in UI | Basic endpoints | Basic Report table | Camera/photo hook | Incomplete | Hazard reporting (Accident, Fire, Road hazard, Unsafe location), description, GPS tagging, optional media attachment. | `android/app/screens/community.py`, `backend/app/models/report.py`, `backend/app/schemas/report.py` |
| **Stitch Visual Styling & 5 Tabs** | Generic KivyMD theme | N/A | N/A | N/A | Incomplete | Must match Stitch design tokens (`#111316` background, `#D92D20` SOS, `#8BCEFF` tracking, Inter typography) across the 5 primary tabs: Home, Safety, Guides, Contacts, Profile. | `android/kv/`, `android/app/components/`, `android/main.py` |

---

## 3. Technology Stack Verification

- **Android Client**:
  - Python 3.10+
  - Kivy 2.3.0 & KivyMD 1.2.0
  - Plyer 2.1.0 & PyJNIus
  - Buildozer (`buildozer.spec` targeting Android API 33)
  - Zero React / Expo / HTML wrappers in the production Android build.
- **Backend Service**:
  - Python 3.10+
  - FastAPI
  - PostgreSQL with SQLAlchemy 2.0 async engine (`asyncpg` & `psycopg`) + SQLite local fallback for testing
  - Pydantic v2
  - Alembic migrations
  - Asynchronous WebSockets (`/ws/tracking/{secure_token}`)

---

## 4. Required Remediations & Next Steps

1. **Database Schema Refactor**: Implement exact models for `User`, `EmergencyContact`, `SOSIncident`, `TrackingSession`, `SafetyTimer`, `CheckIn`, `IncidentEvent`, `MedicalProfile`, `Evidence`, `CommunityReport`.
2. **SOS Engine Upgrade**: Implement `InstantSOSManager` with local state machine, 5-tap rapid detector, idempotency key header, priority phone dialer, and offline queue.
3. **Stitch Theme & Components**: Integrate exact hex codes, corner radii, and component designs into Kivy KV files and Python components.
4. **Automated Tests**: Unit tests covering backend models, authentication, SOS idempotency, tracking sessions, and Android local state transitions.
