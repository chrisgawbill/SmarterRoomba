# SmarterRoomba

Turn a Roomba 694 into a smarter, server-assisted robot without replacing its proven low-level controls.

The project starts small: communicate with the Roomba, collect telemetry, estimate movement, and build a map from sensor events. More advanced navigation and optional ML come only after the deterministic foundation works.

## Target hardware

- iRobot Roomba 694 / 600-series
- Existing Arduino board where practical; exact model and electrical requirements must be verified before wiring
- Home server for mapping, persistence, and high-level navigation
- Optional ESP32 bridge later if Wi-Fi is needed and the existing Arduino is not suitable

## Principles

- Keep Roomba safety/low-level behavior on the Roomba where possible.
- Never guess electrical pinouts, logic levels, or power requirements.
- Build deterministic mapping/navigation before adding AI.
- Keep hardware bridge thin; put reusable intelligence on the server.
- Prefer established libraries over custom implementations when they fit.
- Build and verify one small capability at a time.

See `docs/architecture.md` and `docs/backlog.md`.
