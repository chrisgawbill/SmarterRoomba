# AGENTS.md

## Mission

Build SmarterRoomba incrementally. Favor simple, observable, safe solutions over clever ones.

## AI-driven development rules

- Work on one backlog ticket at a time.
- Read `docs/architecture.md` and the active ticket before coding.
- Keep context small: inspect only files relevant to the ticket.
- PM/reasoning agent owns scope, decisions, acceptance criteria, and review.
- Coding agents execute targeted changes; do not spend tokens redesigning the project unless blocked.
- Prefer targeted edits over broad rewrites.
- Prefer established, maintained libraries when they eliminate non-differentiating infrastructure.
- Do not add dependencies speculatively.
- Do not add ML where deterministic logic solves the ticket.
- Do not invent hardware facts. Mark unknown hardware details as requiring verification.
- Never weaken robot safety behavior merely to make a test pass.

## Handoff protocol

For each ticket, keep handoff minimal:

```text
TICKET: <id>
STATUS: PASS | FAIL | BLOCKED
CHANGED: <files>
VERIFY: <command/result>
NEXT: <only if needed>
```

Do not dump logs or restate the ticket. Include only the relevant failure and a short trace when blocked.

After a ticket is complete and committed, temporary handoff/context files should be deleted. Start the next ticket with fresh context from the architecture, backlog, and current repository state.

## Hardware rule

Software work may mock the robot interface until physical compatibility is verified. No agent should provide or implement a wiring assumption for an unverified connector, voltage, pinout, or Arduino model.
