# Changelog

All notable project changes are recorded here. This file begins with the foundation scaffold; it does not imply that the planned features are implemented.

## [0.1.0] - 2026-11-19

### Added
- Initial Kali UX product and engineering foundation.
- Product specification, roadmap, architecture, feature inventory and design principles.
- Testing, development, research, security/privacy and packaging guidance.
- Initial Python package, CLI version command and smoke test.
- Architecture Decision Records for project scope, modular architecture, platform baseline, gesture arbitration, UI toolkit and packaging direction.

### Status
- No desktop enhancement feature is claimed as complete by this scaffold.
- SwipeSwitch integration remains subject to the dedicated audit.

## 0.3.0-alpha.1 — Interactive prototype

- Added GTK3 Control Center with Overview, Windows, Clipboard, Applications, Productivity and Settings pages.
- Added user-triggered window activation, Task View, eight snap presets, session-only clipboard capture/search/copy/clear, application search/launch, XFCE settings shortcuts, focus-mode controls and named layout snapshots.
- Added `kali-ux gui` / `kali-ux-gui` launch commands and a desktop-entry template.
- Preserved the original SwipeSwitch documentation under `docs/swipeswitch/`.
- Added installation and prototype-operation guides.
- Explicitly retained the known SwipeSwitch acceptance failures and platform validation requirements.


## 0.3.0-alpha.2 — Engineering remediation

- Consolidated live gesture events into `events.py` and removed the unused legacy state machine.
- Corrected reversal semantics and added cancellation for finger-count changes and interrupted gesture begins.
- Added detached process launching for graphical applications so Control Center actions do not block or time out their child apps.
- Hardened focus-mode restoration and layout snapshot validation, privacy and atomic writes.
- Improved active-monitor work-area selection for Snap Assist.
- Reformatted the Python codebase, resolved Ruff lint findings and expanded service/gesture tests.
- Updated implementation, verification and development documentation to match the current source.


## 0.3.0-alpha.3 — Baseline review corrections

- Centralized GTK namespace loading and explicitly pinned GDK 3 alongside GTK 3, libwnck 3 and Pango 1.0 to prevent accidental GTK4/GDK4 selection.
- Removed the unused legacy gesture state machine and its stale expected-failure tests; the live recognizer is the only gesture lifecycle implementation.
- Added a regression test for the GTK namespace selection order.
- Corrected release documentation and verification counts to match the source and actual test run.
- Updated package metadata to use the SPDX `MIT` license identifier and a current setuptools build requirement.
- Kept desktop integration limitations explicit; no live touchpad, compositor, multi-monitor or Debian package lifecycle acceptance is claimed.
