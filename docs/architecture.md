# SmarterRoomba Architecture

## Goal

Add a high-level "brain" to a Roomba 694 while leaving motor control, cliff protection, charging, and other low-level responsibilities with the Roomba whenever possible.

Initial objective: turn Roomba sensor/odometry data into a persistent 2D map and eventually use that map for intentional navigation and cleaning.

## Architecture

```text
Home Server
├── robot gateway
├── telemetry/event store
├── localization / odometry
├── occupancy map
├── path planner (later)
└── optional ML intelligence (later)
        │
        │ local network
        ▼
Hardware Bridge
├── Arduino initially if suitable
└── ESP32 later if wireless bridge is required
        │
        │ Roomba Open Interface / serial (verify on hardware first)
        ▼
Roomba 694
├── bump sensors
├── cliff/safety sensors
├── wheel/encoder telemetry
├── battery/charging state
└── drive system
```

## Layers

### 1. Roomba

Treat the Roomba as the robot hardware platform. Do not bypass safety systems unnecessarily.

Responsibilities:
- Motors and drive hardware
- Existing bump/cliff sensing
- Battery and charging
- Low-level firmware behavior

### 2. Hardware bridge

A deliberately small adapter between the Roomba and server.

Responsibilities:
- Establish verified electrical/serial connection
- Read supported sensor packets
- Send supported commands
- Normalize messages
- Forward telemetry to the server
- Fail safely when communication is lost

The bridge should not contain mapping or AI logic.

### 3. Server brain

The home server owns high-level intelligence.

Initial modules:
- `gateway`: communication with bridge
- `telemetry`: normalized robot events
- `odometry`: estimate x/y/heading from wheel movement
- `mapping`: occupancy grid and collision observations
- `storage`: persist maps/runs/configuration

Later modules:
- `planner`: A*/other deterministic path planning
- `mission`: cleaning/exploration strategy
- `perception`: optional added distance/camera sensors
- `ml`: optional small models for classification/prediction

## Mapping V1

Start each run from a known origin `(0, 0, 0)`.

1. Read wheel movement/encoder telemetry.
2. Estimate robot pose `(x, y, heading)` using differential-drive odometry.
3. When a bump occurs, project an obstacle observation near the robot's bumper.
4. Write observations into an occupancy grid.
5. Persist the map and telemetry for debugging.

Wheel slip and accumulated odometry error are expected. V1 proves the pipeline rather than solving full SLAM.

## AI policy

No AI is required for V1.

Prefer deterministic algorithms for:
- telemetry parsing
- odometry
- occupancy mapping
- path planning
- collision avoidance

Add ML only when there is a concrete task where it improves on deterministic logic, such as visual/object classification or learning recurring environmental patterns.

## Safety boundaries

- Verify the exact Roomba 694 Open Interface support and connector pinout against authoritative documentation before wiring.
- Verify Arduino model and voltage/logic compatibility before connecting it.
- Never connect unknown Roomba power pins directly to MCU I/O.
- Preserve cliff detection and emergency-stop behavior.
- Server/bridge disconnect must not result in uncontrolled motion.
- Development begins with wheels off the floor or otherwise safely constrained when testing drive commands.

## Evolution

### Phase 1 — Connection
Roomba ↔ bridge communication and read-only telemetry.

### Phase 2 — Motion
Controlled movement plus encoder collection.

### Phase 3 — Mapping
Odometry + bump observations + persistent occupancy grid.

### Phase 4 — Navigation
Deterministic path planning and deliberate exploration.

### Phase 5 — Better perception
Optional ToF/LiDAR/camera hardware.

### Phase 6 — Intelligence
Small ML models only for justified perception/behavior tasks.
