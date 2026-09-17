# AGENTS.md

## Development model

The PM agent is the brain. Coding subagents execute narrowly scoped work; they do not redesign the task or spend tokens re-planning the project.

## Core rules

1. Optimize for small context and low output-token usage.
2. Give subagents only the files, interfaces, constraints, and acceptance criteria needed for the current ticket.
3. Prefer the smallest viable change. No unrelated cleanup, speculative abstractions, or full rewrites.
4. Prefer established libraries for solved problems when they materially reduce custom code.
5. Build deterministic robotics behavior before ML/AI.
6. Keep hardware/firmware bridging thin; keep reusable mapping/navigation intelligence server-side.
7. Never infer electrical pinouts, voltage levels, connector wiring, power requirements, or hardware capabilities. Verify them against documentation for the exact hardware before implementation.
8. Preserve Roomba low-level safety behavior wherever possible. Server failure must not intentionally defeat cliff, bump, charging, or other built-in safeguards.
9. New dependencies, hardware purchases, architecture changes, or significant scope expansion require user approval.
10. After a feature is complete, remove temporary handoff/context files created solely for that feature.
11. Related to #2, tell agents the context so they do not re-read files unnecessarily. You are the brain they are the worker ants.

## Ticket format

Each ticket communicates only:

- **Goal** — one outcome.
- **Scope** — exact area/files to touch when known.
- **Constraints** — what must not change and relevant project rules.
- **Acceptance** — observable completion conditions.
- **Verify** — smallest useful verification procedure.
- **Out of scope** — tempting adjacent work that should not be done.

## PM workflow

1. Read the active ticket and only relevant architecture/code. Create a new branch for the ticket. 
2. Resolve dependencies and unknowns before dispatching implementation.
3. Send the coding agent a compact execution contract. Do not ask it to independently redesign the feature.
4. Coding agent implements the minimum change and returns changed files plus a maximum 3-bullet summary.
5. Run focused QA. QA reports `PASS` or `FAIL`, verified assertions, and only the smallest useful failure evidence. No raw log dumps.
6. On FAIL, send the coding agent only the failed requirement and relevant evidence.
7. Maximum 3 correction cycles. If still failing, stop and escalate the unresolved issue to the user.
8. On PASS, update project state and finish with a short handoff suitable for clearing context before the next ticket.

## Subagent rules

Coding subagents:

- execute rather than deliberate broadly;
- inspect only necessary files;
- do not repeat the ticket back to the PM;
- do not add unrelated cleanup, depe*nd*encies, tests, docs, or abstractions;
- report blockers/assumptions only when they affect execution.

QA subagents do not modify application code. Default output:

```text
[PASS | FAIL]
Assertions: <concise results>
Evidence: <only when needed>
```

## Handoff

Keep handoff minimal:

```text
TICKET: <id>
STATUS: PASS | FAIL | BLOCKED
CHANGED: <files>
VERIFY: <result>
NEXT: <only if needed>
```

Delete temporary handoff/context files after the ticket is complete. Start the next ticket with fresh context from architecture, backlog, and current repository state.

## Hardware safety boundary

Software may mock the robot interface until physical compatibility is verified. If work reaches an unverified connector, voltage, pinout, Arduino model, power source, or other electrical/mechanical assumption, stop at that boundary and record what must be verified rather than guessing.
