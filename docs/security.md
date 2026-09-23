# Security Architecture & Threat Model

1. **Authentication**:
   - Passwords hashed using standard `bcrypt` with salt rounds.
   - Stateless JWT tokens signed with HS256 / RS256 algorithms.

2. **Data in Transit**:
   - All REST communication encrypted over TLS 1.3 (HTTPS).
   - Real-time location streams secured over Secure WebSockets (WSS).

3. **Privacy**:
   - Public live tracking links use unguessable cryptographically generated UUIDv4 tokens.
   - Exact location coordinates are only exposed during an active SOS window or explicitly shared safety timers.
