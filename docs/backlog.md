# SmarterRoomba Backlog

Work one ticket at a time. PM owns reasoning and dispatch; coding agents execute the narrow scope defined in `AGENTS.md`.

## SR-001 — Repository + server skeleton

**Goal**  
Create the minimum project structure needed for the server-side brain without implementing robot behavior.

**Scope**
- Choose a small, conventional server runtime based on the repo's actual needs.
- Add directories/modules for gateway, telemetry, odometry, mapping, and storage.
- Add configuration/env handling and a minimal health/startup path.
- Add only dependencies required by this ticket.

**Constraints**
- No Roomba connection yet.
- No AI/ML, path planning, UI, SLAM framework, or speculative abstractions.
- Keep hardware behind an interface so development can proceed without the physical robot.

**Acceptance**
- Project installs/builds/runs using documented commands.
- Server starts and exposes/logs a simple health state.
- Core module boundaries match `docs/architecture.md`.

**Verify**  
Run install/build/test/start checks appropriate to the selected stack.

**Out of scope**  
Serial communication, movement, mapping implementation, web dashboard.

---

## SR-002 — Verify Roomba + Arduino hardware interface

**Goal**  
Document the exact safe interface between the Roomba 694 and the user's Arduino before any wiring or hardware-control code is written.

**Scope**
- Confirm exact Arduino model with the user.
- Verify Roomba 694 Open Interface availability from authoritative documentation.
- Record connector/pinout, serial settings, voltage/logic requirements, and required protection/level conversion.
- Produce a short parts/wiring plan only after those facts are verified.

**Constraints**
- Documentation/research ticket only.
- Never infer a pinout or electrical value from another Roomba/Arduino model.
- Do not instruct physical connection until compatibility is established.

**Acceptance**
- Exact Arduino model recorded.
- Each electrical assumption has an authoritative source.
- Required adapter/components are identified.
- Safe bench-test procedure is documented.

**Verify**  
PM checks every electrical claim against its cited hardware documentation.

**Out of scope**  
Firmware, motor commands, permanent robot modifications.

---

## SR-003 — Mock robot transport

**Goal**  
Let the server brain consume realistic robot telemetry without requiring the physical Roomba.

**Scope**
- Define the smallest transport-neutral message contract needed for initial telemetry.
- Implement a mock source that can emit encoder, bump, cliff/safety, battery, and connection events as applicable to the verified interface.
- Keep mock data deterministic/replayable.

**Constraints**
- Contract should reflect verified Roomba capabilities, not imagined future sensors.
- No mapping or navigation logic.

**Acceptance**
- Server can connect to the mock transport.
- A deterministic event sequence can be replayed.
- Disconnect/error state is representable.

**Verify**  
Automated test/replay demonstrates expected normalized events.

**Out of scope**  
Physical serial connection and UI.

---

## SR-004 — Read-only hardware bridge

**Dependency:** SR-002, SR-003

**Goal**  
Read verified Roomba telemetry through the hardware bridge without controlling movement.

**Scope**
- Implement only the verified serial/Open Interface connection.
- Normalize supported telemetry into the SR-003 contract.
- Handle reconnect/invalid packets safely.

**Constraints**
- Read-only robot operation for this ticket.
- No drive/motor commands.
- Bridge contains no mapping/navigation intelligence.

**Acceptance**
- Server receives real telemetry from the stationary/constrained Roomba.
- Bump/safety/encoder/battery events supported by the verified interface are decoded correctly.
- Disconnect does not crash either side.

**Verify**  
Controlled bench test comparing observed physical events with received telemetry.

**Out of scope**  
Autonomous movement, mapping, wireless redesign.

---

## SR-005 — Differential-drive odometry

**Goal**  
Estimate `(x, y, heading)` from recorded wheel movement.

**Scope**
- Implement deterministic differential-drive odometry server-side.
- Consume normalized encoder/wheel events.
- Make robot geometry/calibration explicit configuration.

**Constraints**
- Use established math/library support where it reduces risk without pulling in a large robotics stack unnecessarily.
- No SLAM or sensor fusion.

**Acceptance**
- Straight, rotation, and curved synthetic paths produce expected pose changes within defined tolerance.
- Pose begins at a known origin.
- Invalid/reset encoder data is handled explicitly.

**Verify**  
Focused automated tests using deterministic trajectories.

**Out of scope**  
Correcting wheel slip, map matching, localization AI.

---

## SR-006 — Occupancy map from bumps

**Dependency:** SR-005

**Goal**  
Turn pose + bump events into the first persistent 2D obstacle map.

**Scope**
- Add a simple occupancy-grid representation.
- Project bump observations near the appropriate bumper position.
- Persist/load the grid and basic run metadata.

**Constraints**
- V1 is intentionally approximate.
- Do not introduce full SLAM.
- Keep mapping server-side.

**Acceptance**
- Deterministic replay creates the same map every time.
- Bumps produce obstacle cells in plausible positions relative to pose.
- Map survives server restart.

**Verify**  
Replay a synthetic route with known collisions and assert resulting grid observations.

**Out of scope**  
Room recognition, camera perception, path planning.

---

## SR-007 — Safe controlled drive commands

**Dependency:** SR-002, SR-004

**Goal**  
Allow bounded server-requested movement while preserving a local fail-safe path.

**Scope**
- Add only documented drive/stop commands needed for basic experiments.
- Add command limits and explicit stop behavior.
- Define behavior for server/bridge communication loss.

**Constraints**
- First drive tests occur with robot safely constrained/wheels off the floor as appropriate.
- Never disable cliff/safety behavior to satisfy this ticket.
- No autonomous navigation yet.

**Acceptance**
- Forward/turn/stop commands work within configured limits.
- Explicit stop works reliably.
- Communication loss results in a safe stopped/non-commanded state according to the verified interface design.

**Verify**  
Bench test first; limited floor test only after bench PASS.

**Out of scope**  
Room-scale autonomy and cleaning strategy.

---

## SR-008 — Mapping exploration run

**Dependency:** SR-006, SR-007

**Goal**  
Perform a bounded physical exploration that generates a bump-based map.

**Scope**
- Implement a simple deterministic explore/turn/recover behavior.
- Record telemetry, pose, bump events, and resulting map.
- Add clear start/stop/run boundaries.

**Constraints**
- Keep behavior intentionally simple.
- No ML and no path planner.
- Safety events override exploration commands.

**Acceptance**
- Roomba can complete a bounded test-area run.
- Run produces a persisted map and replayable telemetry.
- User can stop the run immediately.

**Verify**  
Controlled test-area run plus offline replay comparison.

**Out of scope**  
Whole-home autonomy and optimized cleaning.

---

## SR-009 — Deterministic path planner

**Dependency:** SR-008

**Goal**  
Plan traversable routes through the known occupancy map.

**Scope**
- Evaluate a lightweight established A* implementation/library before custom code.
- Convert occupancy grid into planner input.
- Produce paths between known map coordinates.

**Constraints**
- Planning only; do not immediately let planner command the physical robot.
- Unknown/unsafe cells must have explicit treatment.

**Acceptance**
- Planner finds valid paths around known obstacles.
- Reports no-path cleanly.
- Deterministic maps produce deterministic plans.

**Verify**  
Automated map fixtures covering open, blocked, and narrow routes.

**Out of scope**  
Physical path following, ML navigation.

---

## SR-010 — Path following

**Dependency:** SR-007, SR-009

**Goal**  
Follow a short planned path using odometry and existing safety sensors.

**Scope**
- Convert path segments into bounded drive commands.
- Stop/replan or abort on unexpected bump/safety events.
- Record execution error for later calibration.

**Constraints**
- Begin in a small controlled area.
- No AI correction layer.

**Acceptance**
- Robot attempts a short known route and stops at completion or on safety interruption.
- Unexpected obstacle never gets ignored merely to complete the route.
- Run is replayable/debuggable from telemetry.

**Verify**  
Simulation/mock first, then controlled physical test.

**Out of scope**  
Whole-home cleaning optimization.

---

## Later — only after V1 works

Do not implement these until the deterministic pipeline is useful:

- Better localization / SLAM evaluation
- ToF, LiDAR, or camera perception
- Automatic docking experiments
- Room/zone semantics
- Cleaning coverage planning
- Small ML models for a concrete demonstrated need
- Dashboard/mobile controls
- Reusable robotics-engine extraction if SmarterRoomba proves the abstractions are genuinely reusable
