# Kali UX — Feature Inventory

**Status key:** Planned = product scope only; Existing project = separate codebase exists but has not yet been audited for integration; Foundation = this scaffold only.

| Feature | User value | Initial scope | Status | Priority |
|---|---|---|---|---|
| SwipeSwitch | Fast gesture-driven window navigation | Six agreed gestures; MRU switching; Show Desktop/restoration; Task View; workspace navigation | Existing project; audit pending | P0 |
| Shared Gesture Control | Avoid gesture conflicts and centralize ownership | Input adapter, normalized events, recognizer, arbitration | Planned; technical proof of concept required | P0 |
| Window Overview | See and select open windows | Eligible windows, pointer/keyboard selection, dismissal | Partly overlaps SwipeSwitch Task View | P1 |
| Snap Assist | Arrange windows quickly | Layout suggestions and native window-manager integration | Planned | P1 |
| Control Center | Configure the suite in one place | Feature status, settings and diagnostics | Planned | P2 |
| Diagnostics | Understand compatibility and failures | Capability report, redacted logs and support bundle | Planned | P1 |
| Clipboard History | Recover recent copied content | Bounded searchable history and privacy controls | Planned; data policy required | P2 |
| Quick Panel | Access selected controls quickly | Small focused panel, reuse XFCE services | Planned | P2 |
| Focus Tools | Reduce distraction | Optional, reversible focus utilities | Planned | P3 |
| Application Launcher | Find and launch applications | Desktop-entry-aware search and launch | Planned | P3 |
| Window Peek | Preview a window | Preview where capture is supported | Planned | P3 |
| Layout Memory | Restore window arrangements | Best-effort geometry/workspace snapshots | Planned | P3 |

## P0 — First integration slice

### SwipeSwitch
The product contract is in `PRODUCT_SPECIFICATION.md`. Audit the actual repository before determining what is implemented. The recent development history indicates that a v0.2.0 core preview existed and that automated verification had outstanding failures; this is historical context, not a verified result for the current repository.

### Shared Gesture Control
This is a suite-level architectural requirement, not permission to replace SwipeSwitch's input implementation before audit. First establish whether a shared dispatcher is needed immediately or whether an adapter is sufficient for the first integration.

## Cross-feature requirements

Every feature must:
- Have an explicit enabled/disabled state where appropriate.
- Respect platform capability checks.
- Avoid modifying system configuration without explicit user approval.
- Provide clear error and recovery behaviour.
- Avoid blocking the UI thread.
- Have unit tests for its domain logic and integration/manual tests for desktop effects.
- Document privacy, persistence and permissions.
- Be independently disableable without disabling unrelated features.

## Feature overlap and boundaries

SwipeSwitch Task View and a future Window Overview may be the same capability rather than two separate products. The product design should avoid shipping duplicate interfaces. The Control Center is a configuration surface, not the owner of feature logic. Shared Gesture Control routes input but does not own window-management behaviour. Snap Assist requests operations from the platform adapter; it does not become a replacement window manager.

## Status discipline

Do not mark a feature complete based on a class, UI mockup or passing isolated test. Use the status vocabulary in `README.md` and record evidence in the relevant milestone report.
