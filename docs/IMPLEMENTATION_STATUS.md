# Implementation status — integrated baseline

**Release:** 0.2.0-alpha.1 (working baseline)  
**Target:** Kali Linux / XFCE / X11  
**Verification environment:** build container, not a live Kali desktop

## Implemented in this archive

- Preserved the existing SwipeSwitch v0.2.0 preview engine under `features/window_switcher/engine/` and connected a dedicated CLI entry point.
- Added XDG path handling, JSON configuration defaults, a static feature registry, read-only platform capability detection, and safe subprocess wrappers (argument arrays, no shell).
- Added a normalized gesture event/router contract. It does not capture input or start automatically.
- Added snap geometry service, bounded in-memory clipboard model, layout snapshot service, XDG desktop-entry discovery, XFCE focus-mode helper, quick-action launcher, Task View reuse, Control Center model and diagnostic report.
- Added unit tests for the newly implemented service contracts.

## Not complete / must not be represented as complete

- No unified polished GTK Control Center, Quick Panel, Clipboard History UI, Snap Assist UI, Focus UI or Launcher UI.
- No production shared gesture provider. The existing SwipeSwitch listener remains app-local and uses `libinput debug-events`; provider reliability, permission handling and coexistence need proof on the target Kali release.
- SwipeSwitch thumbnails remain unimplemented; multi-monitor overlay support remains limited; inherited tests/state semantics require resolution.
- Window Peek does not capture pixels. A compositor-aware capture backend and privacy model are required.
- Snap Assist uses direct geometry requests and does not yet calculate usable monitor work areas or offer a visual zone overlay.
- Clipboard service is not wired to X11 selection monitoring; persistence is deliberately disabled.
- Layout restoration is best-effort and does not promise cross-monitor or workspace fidelity.
- The focus helper must be tested against the installed XFCE notification daemon version and preserve exact prior setting semantics.
- Launcher uses a deliberately basic desktop-file reader; full freedesktop Exec field-code handling and terminal/startup-notify semantics remain.
- No installer, autostart, systemd user service, or system configuration mutation is enabled by default.

## Verification performed for this archive

The archive build should be checked with Python compilation, the GTK-independent pytest suite, CLI smoke tests, and ZIP integrity. These checks do not validate GTK/libwnck, input-device access, window-manager behaviour, or real touchpad gestures. Results are recorded in `docs/VERIFICATION_REPORT.md` after the build.

## Next engineering pass

1. Resolve SwipeSwitch's three previously observed test failures by defining reversal and threshold semantics; do not weaken tests blindly.
2. Add an adapter around libwnck so core tracker tests can run without importing GI at module import time.
3. Validate the six agreed gestures on target Kali and decide whether the current input source is safe for production.
4. Consolidate gesture ownership through the shared router only after the input-provider proof of concept.
5. Implement GTK interfaces for the remaining features using the common design system.
6. Add multi-monitor/work-area-aware geometry, capture backend, privacy controls and end-to-end desktop tests.
