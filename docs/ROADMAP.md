# Kali UX — Development Roadmap

**Status:** Active engineering plan. A feature is not complete merely because its interface exists.

## Delivery philosophy

Build a reliable vertical slice before expanding breadth. Every phase has a user-visible outcome and exit criteria. Preserve the working baseline, make changes in small reviewable increments, and distinguish implemented, tested and live-verified behaviour.

## Phase 0 — Product and engineering foundation

**Status:** Baseline established in 0.3.0-alpha.3.

- Product specification, architecture, feature inventory and design principles.
- Python package, CLI, test setup and developer workflow.
- XDG configuration, diagnostics, GTK3 namespace loader and platform capability checks.
- Security, privacy and packaging constraints.

## Phase 1 — Control Center foundation (current)

**Purpose:** make the Control Center the coherent management surface for the suite without making it responsible for feature implementation.

Work:
- Use `ControlCenterModel` as the single UI-facing owner of feature preferences.
- Persist settings atomically with owner-only permissions.
- Separate implementation maturity, runtime availability and enabled preference.
- Detect requirements without changing system state.
- Provide sidebar navigation, Overview, Features, Appearance, Gestures, Privacy, Diagnostics and About sections.
- Gate feature controls according to saved preferences and detected availability.
- Keep feature activation explicit; toggles must not start daemons, take input ownership or alter system settings.
- Split the growing GTK application into focused page/components after the model and interaction contracts settle.

Exit criteria:
- Settings survive restart and malformed values are rejected safely.
- Planned or unavailable features cannot be enabled; users can always disable a previously enabled feature.
- Feature controls accurately reflect enabled/available state.
- Diagnostics explain missing requirements without collecting private data.
- GTK UI is manually validated on Kali XFCE/X11 for scaling, keyboard navigation and interaction.

## Phase 2 — SwipeSwitch integration and acceptance

**Purpose:** make SwipeSwitch a reliable feature inside the shared architecture.

Inspect and validate:
- Input listener, device detection, event parser and real event fixtures.
- Gesture recognizer lifecycle, reversal, cancellation and finger-count changes.
- Window tracking, MRU ordering, workspace filtering and activation.
- Show Desktop snapshot/restoration and workspace navigation.
- Switcher overlay, Task View, thumbnails, keyboard navigation and dismissal.
- Configuration, startup, logging and error recovery.

Critical proof of concept:
- Establish a supported input provider on the actual Kali machine.
- Confirm device ownership, permissions and coexistence with existing gesture tools.
- Do not assume `libinput debug-events` is a production API.
- Do not disable services or modify input permissions automatically.

Exit criteria:
- No interference with normal touchpad operation.
- Gesture transitions are predictable and cancellable.
- Window activation and workspace behaviour pass real XFCE/X11 tests.
- The feature can be enabled/disabled without orphaned processes.

## Phase 3 — Window backend and Snap Assist

- Keep `xfwm4` authoritative.
- Introduce a small X11/EWMH window-management adapter.
- Calibrate usable monitor work areas, panels, scaling and window constraints.
- Add snapping interactions and multi-monitor tests.

## Phase 4 — Desktop overview and navigation

- Refine Task View and window overview.
- Improve focus, dismissal, keyboard navigation and performance.
- Add desktop/workspace navigation only where the backend supports it reliably.

## Phase 5 — Gesture and shortcut management

- Normalize provider events through one dispatcher.
- Add explicit provider selection, conflict reporting and user-controlled mappings.
- Avoid competing listeners and duplicate activation paths.

## Phase 6 — Productivity modules

Deliver one module at a time: Clipboard History, Quick Panel, Focus Tools, Application Launcher, Window Peek and Layout Memory. Each needs a privacy review where relevant, tests, enable/disable behaviour and documentation.

## Phase 7 — Polish and distribution

- Accessibility, keyboard navigation, scaling, performance and visual consistency.
- Debian package metadata and reproducible builds.
- Install/upgrade/remove testing and configuration-preservation rules.
- Release notes, checksums and support matrix.
- Consider a signed APT repository only after the package lifecycle is stable.

## Phase 8 — Compatibility expansion

Evaluate other X11 desktops and Wayland as separate efforts. Wayland requires compositor-specific APIs and cannot be assumed to work through X11/EWMH abstractions.

## Milestone discipline

For every increment: define behaviour and acceptance criteria; inspect constraints; design interfaces; implement the smallest useful change; run automated tests; perform target-desktop tests; document limitations; update the changelog; and commit a checkpoint.

## Current position

The 0.3.0-alpha.3 baseline is retained. The first Control Center foundation increment is implemented in 0.3.0-alpha.4: model-backed feature preferences, capability-aware availability, atomic configuration writes, sidebar navigation and feature-control gating. Automated tests pass in the build container. Live GTK interaction, accessibility, scaling and desktop-specific capability detection still require validation on the user's Kali XFCE/X11 system. SwipeSwitch integration/acceptance follows after this Control Center milestone is verified.
