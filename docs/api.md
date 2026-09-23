# AlertX2 REST API Specification

Base URL: `/api/v1`

## Authentication

- `POST /auth/register`: Create a new user account.
- `POST /auth/login`: Authenticate and receive a JWT access token.

## User & Profile

- `GET /users/me`: Retrieve currently authenticated user profile.
- `PUT /users/me`: Update profile details.
- `POST /users/me/medical`: Upsert critical medical emergency info (blood type, allergies, medications).
- `PUT /users/me/settings`: Modify trigger thresholds and privacy preferences.

## Emergency Contacts

- `GET /contacts`: List all registered emergency contacts.
- `POST /contacts`: Add an emergency contact.
- `DELETE /contacts/{id}`: Delete an emergency contact.

## SOS Operations

- `POST /sos/trigger`: Initiate emergency mode. Dispatches notifications to contacts and opens live tracking room.
- `POST /sos/resolve`: Mark an emergency as resolved or false alarm.

## Telemetry & Tracking

- `POST /location/breadcrumb`: Ingest a GPS breadcrumb during an active SOS.
- `GET /tracking/{incident_uuid}`: Public live tracking route for emergency responders and contacts.
- `WS /ws/sos/{incident_uuid}`: Real-time WebSocket stream of coordinates.

## Safety & Assistance

- `POST /safety/timer`: Start an automated countdown timer.
- `POST /safety/timer/cancel`: Acknowledge safety and terminate timer.
- `POST /checkins`: Send quick location check-in to trusted circle.
- `GET /guides`: Retrieve categorized first-aid and survival procedures.
- `POST /assistant/query`: Situational AI query for safety advice.
