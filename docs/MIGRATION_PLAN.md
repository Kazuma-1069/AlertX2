# ALERTX Migration & Rebuild Plan

**Application Name**: ALERTX  
**Tagline**: *Safety when you need it most.*  
**Date**: September 23, 2026  

---

## 1. Context & Architectural Mandate

The source repository contained Tailwind/HTML web designs in `stitch_alertx_safety_app_ui/` along with generic prototype scaffolding. The project specification strictly forbids using:
- React / React Native / Expo
- Flutter / FlutterFlow
- Ionic / Capacitor / Electron
- WebViews / HTML / Tailwind as the production Android UI

The production Android client must be a genuine **Python + Kivy + KivyMD + PyJNIus + Plyer + Buildozer** application. The backend must be an asynchronous **FastAPI + PostgreSQL + SQLAlchemy 2.0 + Pydantic + Alembic + WebSockets** engine.

This document details the exact migration and reconstruction plan to translate the Stitch design source-of-truth and domain requirements into real, working Python code.

---

## 2. Migration Breakdown by Subsystem

### 2.1 UI Layer: Stitch HTML/Tailwind -> KivyMD & KV Declarative Rules

The Stitch mockup provides 7 key references:
1. `alertx_safety_core/DESIGN.md`: Primary design tokens (colors, typography, grid, corner radii, elevation).
2. `home_sos_ready/code.html`: Resting home screen with prominent SOS button, GPS/battery telemetry banner, and quick actions.
3. `sos_active_emergency_mode/code.html`: Active emergency view with crimson pulse beacon, real-time breadcrumbs, emergency call hotline, and "I AM SAFE" cancel button.
4. `emergency_contacts_management/code.html`: Priority-tiered contacts (Priority 1, 2, 3), SMS/Call/WhatsApp flags, and Add Contact modal.
5. `safety_tools_timer/code.html`: Countdowns (5m, 15m, 30m, 1h, custom), check-in broadcast, and fake incoming call simulator.
6. `emergency_guides_first_aid/code.html`: Offline medical (CPR, choking), environmental (fire, earthquake), and threat response procedures.
7. `profile_sos_settings/code.html`: Emergency medical profile (blood group, allergies, medications, physician) and trigger settings (5-tap power key, shake detection).

**Migration Strategy**:
- Extract color hexes directly into Kivy `get_color_from_hex` constants:
  - Canvas / Background: `#111316`
  - Surface Card (Tier 1): `#1E2023`
  - Elevated Surface (Tier 2): `#282A2D`
  - SOS Critical Red: `#D92D20`
  - Radiating Beacon Glow: `#EF4444` / Light: `#FFB4A8`
  - Info / Tracking Blue: `#8BCEFF` (`#0BA5EC`)
  - Warning / Timer Amber: `#F79009` (`#FFB875`)
  - Safe / Clear Green: `#12B76A`
  - Text Primary: `#E2E2E6` / Text Muted: `#A0A2A6`
- Construct a dedicated Kivy navigation shell with **exactly 5 primary sections**:
  1. `HomeScreen` (`home`)
  2. `SafetyScreen` (`safety`)
  3. `GuidesScreen` (`guides`)
  4. `ContactsScreen` (`contacts`)
  5. `ProfileScreen` (`profile`)
  plus modal/subscreens: `EmergencyScreen`, `FakeCallScreen`, `GuideDetailScreen`, `IncidentDetailScreen`, `ReportScreen`.
- Replace HTML buttons with specialized KivyMD widgets: `SOSButton`, `ContactCard`, `GuideCard`, `SafetyCard`, `StatusIndicator`, `TimerWidget`, `BottomNavigation`, `EmergencyBanner`.

---

### 2.2 Core SOS Engine: Elimination of Countdown & Instant Local State

**Legacy Problem**:
The preliminary prototype implemented a countdown before initiating SOS. In life-critical emergencies, seconds count; an SOS button must trigger immediately without delay.

**Target Architecture**:
```text
User Tap / 5-Tap Rapid Press
  │
  ▼
[InstantSOSManager]
  │──> 1. Set local state = SOS_ACTIVE (Instant UI transition to Emergency Mode)
  │──> 2. Acquire GPS coordinates via Plyer / PyJNIus
  │──> 3. Start ambient audio recording (if enabled)
  │──> 4. Trigger Native Telephony Call to Priority 1 Contact
  │──> 5. Dispatch Native SMS with Maps link to Priority Contacts
  │──> 6. Queue asynchronous sync with FastAPI /api/v1/sos
```
- If the phone is offline or backend is unreachable, steps 1, 2, 3, 4, 5 still execute on the device.
- Implements an explicit local state machine:
  `SAFE -> SOS_ACTIVATING -> SOS_ACTIVE -> SOS_RESOLVING -> SOS_RESOLVED` (or `SOS_CANCELLED`).
- Idempotency keys (`idempotency_key` header / UUID) are sent with SOS API calls so repeated button presses or network retries do not spawn multiple duplicate incidents.

---

### 2.3 Database Architecture: Strict Section 8 Realignment

All models are refactored to match Section 8 requirements:
1. **`User`**: `id`, `name`, `email`, `phone`, `hashed_password`, `is_active`, `created_at`, `updated_at`.
2. **`EmergencyContact`**: `id`, `user_id`, `name`, `phone`, `relationship`, `priority` (1, 2, 3...), `receive_sos`, `receive_location`, `receive_checkin_alert`, `created_at`, `updated_at`.
3. **`SOSIncident`**: `id`, `user_id`, `status` (ACTIVE, RESOLVED, CANCELLED), `activation_method` (BUTTON, FIVE_TAP, TIMER_EXPIRY), `started_at`, `resolved_at`, `cancelled_at`, `last_latitude`, `last_longitude`, `location_accuracy`.
4. **`TrackingSession`**: `id`, `incident_id`, `secure_token` (opaque url-safe string), `started_at`, `ended_at`, `active`.
5. **`SafetyTimer`**: `id`, `user_id`, `duration_minutes`, `started_at`, `expires_at`, `status` (ACTIVE, COMPLETED, EXPIRED, CANCELLED).
6. **`CheckIn`**: `id`, `user_id`, `destination`, `expected_arrival`, `status`, `started_at`, `completed_at`.
7. **`IncidentEvent`**: `id`, `incident_id`, `event_type`, `metadata_json`, `timestamp`.
8. **`MedicalProfile`**: `id`, `user_id`, `blood_group`, `allergies`, `medications`, `medical_information`, `is_shareable_with_responders`.
9. **`Evidence`**: `id`, `incident_id`, `type` (AUDIO, IMAGE, SENSOR), `storage_reference`, `created_at`, `upload_status`.
10. **`CommunityReport`**: `id`, `user_id`, `type`, `description`, `latitude`, `longitude`, `media_reference`, `status`, `created_at`.

Database engine supports both **PostgreSQL** (`postgresql+asyncpg://...`) and SQLite (`sqlite+aiosqlite://...`) for development and automated test suites.

---

### 2.4 Android Native Integrations (PyJNIus & Plyer)

Dedicated modules in `android/app/native/`:
- `android_permissions.py`: Contextual runtime permission requests for `ACCESS_FINE_LOCATION`, `SEND_SMS`, `CALL_PHONE`, `RECORD_AUDIO`, `FOREGROUND_SERVICE`.
- `android_location.py`: Native GPS acquisition with fallback.
- `android_calls.py`: Native `ACTION_CALL` intent via PyJNIus / Plyer to dial priority contacts directly.
- `android_sms.py`: Native Android `SmsManager` invocation to send direct emergency SMS messages.
- `android_battery.py`: Battery level and charging status detection.
- `android_network.py`: Connectivity broadcast receiver.
- `android_recording.py`: `MediaRecorder` ambient microphone capture.
- `android_service.py`: Foreground service with persistent status bar notification during active tracking.

---

## 3. Phased Execution Roadmap

- **Phase 1**: Audit and Migration Plan (Completed).
- **Phase 2**: Foundation — Refactor Database Models (Section 8), SQLAlchemy async session, Alembic migrations, Authentication, KivyMD theme and 5-section navigation shell.
- **Phase 3**: Core SOS — Instant 1-tap SOS engine, 5-tap detector, local state machine, Priority 1->2->3 calling, emergency SMS, live tracking sessions, and active emergency UI.
- **Phase 4**: Safety Tools — Safety Timer (5m/15m/30m/1h/custom), Check-in, Missed check-in auto-escalation, Fake Call generator, Nearby help radar.
- **Phase 5**: Guides & AI Assistant — Offline medical, environmental, and threat response procedures; situational AI assistant with safety disclaimers.
- **Phase 6**: Profile & Medical — Private medical profile, SOS power button / shake settings, privacy toggles.
- **Phase 7**: Evidence & Incident History — Audio recording vault, incident timeline (`IncidentEvent`), and local audit log.
- **Phase 8**: Community Reporting — Hazard reporting (accident, fire, hazard, unsafe zone), GPS tagging, submission API.
- **Phase 9**: Polish & Validation — Error/Offline/Empty states, unit tests for backend and Android, health check endpoints (`/health`, `/health/database`), updated README, and Buildozer validation.
