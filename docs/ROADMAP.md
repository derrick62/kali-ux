# Kali UX — Development Roadmap

**Status:** Proposed delivery sequence, not a declaration of completed work.

## Delivery philosophy

Build a reliable vertical slice before expanding breadth. Each phase has an outcome and exit criteria. We do not move forward merely because code has been written; the behaviour must be tested at the appropriate level and its status recorded.

## Phase 0 — Product and engineering foundation

**Purpose:** establish a shared source of truth and a maintainable starting point.

Work:
- Establish product specification, architecture, feature inventory and design principles.
- Record decisions and unresolved questions.
- Create the Python package, test setup and developer workflow.
- Define security, privacy and packaging constraints.

Exit criteria:
- Documentation is internally consistent.
- The initial package installs in an isolated environment.
- CLI smoke test and test suite pass.
- Open decisions are visible rather than silently assumed.

## Phase 1 — SwipeSwitch audit (next)

**Purpose:** understand the actual code before integrating or refactoring it.

Inspect:
- Repository history, tree, packaging and dependencies.
- Input listener and device detection.
- Event parser and real event fixtures.
- Gesture recognizer/state machine.
- Window tracking, MRU ordering and workspace filtering.
- Show Desktop snapshot/restoration.
- Task View and horizontal switcher overlays.
- Window activation and workspace navigation.
- Configuration, startup, logging and error recovery.
- Automated tests and real-desktop verification.

Classify each component as **Keep**, **Improve**, **Replace** or **Missing**. Record evidence, not assumptions.

Deliverables:
- Audit report.
- Verified implementation-status matrix.
- Test baseline and known failures.
- Prioritized backlog and integration recommendation.

Exit criteria:
- Current source and archive differences are understood.
- Every agreed gesture has a requirement-to-code trace.
- Test failures are reproduced or explained.
- No destructive refactor is started before the audit findings are reviewed.

## Phase 2 — Platform and gesture integration proof of concept

**Purpose:** validate the system boundaries on the actual target machine.

Work:
- Identify available gesture tools/services and their ownership.
- Capture and inspect actual touchpad event sequences.
- Validate the least-privilege event acquisition method.
- Test cancellation, finger-count changes, event timing and device reconnect.
- Validate X11/EWMH and libwnck operations against `xfwm4`.
- Establish a shared gesture arbitration contract.

Exit criteria:
- The input source is technically and operationally understood.
- Permission requirements are documented and minimized.
- Existing gesture services are not modified without consent.
- A prototype demonstrates clean ownership and cancellation.

## Phase 3 — Shared core and first integrated vertical slice

**Purpose:** introduce only the common infrastructure that multiple features genuinely need.

Potential components:
- Application lifecycle and single-instance policy.
- Configuration loading/validation.
- Structured logging and diagnostics.
- Feature registration/enablement.
- Platform capability detection.
- Shared event contracts, if justified by real consumers.

Integrate the audited SwipeSwitch functionality behind stable interfaces.

Exit criteria:
- Startup/shutdown are reliable.
- Configuration failures are handled safely.
- Feature failures do not crash unrelated components.
- The integrated SwipeSwitch path passes automated and manual acceptance tests.

## Phase 4 — Snap Assist and window layout foundation

**Purpose:** deliver window arrangement without replacing `xfwm4`.

Work:
- Inventory native `xfwm4` snapping/tiling behaviour.
- Define where a preview/assist UI adds value beyond native behaviour.
- Validate geometry requests and monitor/workspace handling.
- Test maximized, fullscreen, transient, fixed-size and multi-monitor windows.

Exit criteria:
- Feature adds demonstrable value.
- Window manager remains authoritative.
- Unsupported operations fail gracefully.

## Phase 5 — Task View, navigation and visual refinement

**Purpose:** refine window discovery, overview and navigation into a coherent interaction system.

Work:
- Separate quick switching from all-window overview.
- Refine pointer/keyboard navigation and dismissal.
- Evaluate thumbnails only after icons/titles and interaction correctness.
- Test multi-monitor and compositor-on/off behaviour.

Exit criteria:
- Overview and switcher have distinct, understandable purposes.
- Focus and activation behaviour are predictable.
- Performance and accessibility checks pass.

## Phase 6 — Productivity modules

Deliver one module at a time:
- Clipboard History.
- Quick Panel.
- Focus Tools.
- Application Launcher.
- Window Peek.
- Layout Memory.

Each module must have a product requirement, privacy assessment where applicable, tests, enable/disable behaviour and documentation before it is called complete.

## Phase 7 — Control Center and diagnostics

Unify configuration and status without making the Control Center a dependency for basic operation. Diagnostics should report capability, versions, feature health and redacted logs.

## Phase 8 — Packaging and release

Work:
- Debian package metadata and reproducible build.
- Install/upgrade/remove testing.
- User-session startup integration.
- Dependency and compatibility checks.
- Release notes, checksums and documented support matrix.
- Consider signed APT repository only after package/release process is stable.

Exit criteria:
- Fresh install, upgrade and removal are verified.
- User configuration is preserved appropriately.
- No privileged GUI execution.
- Known limitations and troubleshooting are documented.

## Phase 9 — Compatibility expansion

Evaluate other X11 desktops and Wayland as separate engineering efforts. Wayland support requires compositor-specific protocols/APIs and cannot be assumed to work through X11/EWMH abstractions. Add a platform only after a concrete capability matrix and test environment exist.

## Milestone discipline

For every milestone:
1. Define user-visible behaviour and acceptance criteria.
2. Identify platform constraints and risks.
3. Design interfaces and record material decisions.
4. Implement the smallest useful increment.
5. Run automated tests.
6. Run manual target-desktop tests where required.
7. Record what is implemented, tested and verified.
8. Update documentation and changelog.

## Current position

Phase 0 (product and engineering foundation) and Phase 1 (SwipeSwitch source audit) are complete for the supplied 0.3.0-alpha.2 archive. A focused source-remediation pass has consolidated the live gesture recognizer and improved process launching, focus-mode recovery, snapping, layout snapshot handling and automated tests. The next phase is **Phase 2: platform and gesture integration proof of concept** on the actual Kali XFCE/X11 machine. Do not enable automatic startup, change device permissions or modify existing gesture services as part of that proof of concept without explicit review.
