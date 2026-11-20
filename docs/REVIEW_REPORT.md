# Kali UX baseline review and correction report

**Input archive:** `kali-ux(1).zip`
**Reviewed baseline:** 0.3.0-alpha.2
**Updated version:** 0.3.0-alpha.3
**Review date:** 19 November 2026

## Summary

The baseline follows the agreed direction: Kali XFCE/X11 first, a modular Python application, GTK3 Control Center, integrated SwipeSwitch, feature services, and `xfwm4` retained as the authoritative window manager. It is an engineering prototype, not a finished desktop shell or release-ready package.

The source archive also contained development artifacts (`.venv`, bytecode caches, build output, wheel output and egg metadata). These are excluded from the cleaned handover archive. The cleaned handover ZIP omits `.git` and generated build artifacts. Keep the original repository directory if you need its existing commit history; the source files in this archive are the reviewed alpha.3 baseline.

## Corrections made

### GTK3 startup conflict

The Control Center and SwipeSwitch import paths requested GTK 3 and libwnck 3 but imported GDK without pinning its namespace version. PyGObject could therefore load GDK 4 first, then fail when GTK 3 required GDK 3. A shared `kali_ux.platform.gtk.load_gtk3()` helper now explicitly requests GTK 3, GDK 3, libwnck 3 and Pango 1.0 before importing any of them. Both entry points use the same helper, and a regression test verifies the request order.

### Gesture implementation and tests

The baseline documentation claimed the unused legacy `GestureStateMachine` and its stale tests had been removed, but `engine/state.py` and `tests/swipeswitch/test_state.py` were still present. The latter contained two expected failures. The legacy module and test file have now been removed; the live `GestureRecognizer` in `gestures.py` remains the single gesture lifecycle implementation. The suite now has no expected failures.

### Packaging metadata and documentation

The project metadata used the deprecated TOML license-table form. It now uses the SPDX `MIT` identifier and requires a setuptools version that supports the modern metadata. The version is advanced to `0.3.0a3`. Release notes, implementation status, manifest and verification documentation were updated to match the reviewed source and test results.

## Baseline strengths retained

- `src/` package layout and clear separation between core, platform, UI and feature services.
- XDG-based paths and private layout snapshots.
- Explicit user-triggered desktop actions; no root GUI, automatic startup, privileged helper or silent changes to other gesture services.
- `xfwm4` remains authoritative; snapping issues requests through `wmctrl`.
- Clipboard capture is opt-in, bounded and in-memory only; retention limits now come from validated configuration. Application-specific exclusions remain unimplemented.
- Graphical applications use detached process launching rather than blocking the GTK main loop.
- Product, architecture, security, testing, packaging and SwipeSwitch design documentation are retained.

## Verification

- Python compilation: passed.
- Pytest: **41 passed, 1 skipped, 0 expected failures**.
- Skipped test: libwnck tracker integration, because the build container does not provide PyGObject/libwnck.
- CLI version, status and feature-list smoke tests: passed.
- GUI module import without initializing GTK: passed.
- GTK namespace regression test: passed.
- Ruff was not installed in the review container, so Ruff lint/format checks are not claimed in this report.
- Python wheel build and isolated target install: passed; installed CLI version smoke test passed. Wheel: `kali_ux-0.3.0a3-py3-none-any.whl`, SHA-256 `1c15d69757251c77679e0f83f5f217ac0d36835b0953f9609f06afd6306d8d29`. This does not constitute Debian packaging validation.

## Remaining work — intentionally not claimed as complete

- The input listener still uses `libinput debug-events`, a diagnostic command rather than a production-approved event API. Validate device selection, permissions, stream format, event cancellation and coexistence with existing gesture tools on the actual Kali machine.
- Run the Control Center and SwipeSwitch in the real XFCE/X11 session; verify touchpad feel, Task View focus/dismissal, active-window switching and workspace navigation.
- Validate snapping with xfwm4, panel work areas, fractional scaling and multiple monitors.
- Validate clipboard ownership against the installed clipboard manager and notification focus-mode semantics against the installed XFCE notification daemon.
- Window Peek capture, production shared gesture arbitration, Wayland and other desktop environments remain future work.
- Debian package lifecycle (install, upgrade, reinstall, remove) and a signed APT repository remain future work.

## Recommendation

Use alpha.3 as the corrected source baseline. The next milestone remains the Phase 2 platform and gesture integration proof of concept on the actual Kali XFCE/X11 machine. Do not enable automatic startup, broaden input permissions or disable another gesture service until the proof of concept and its security implications have been reviewed.
