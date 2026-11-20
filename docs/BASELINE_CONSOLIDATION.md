# Kali UX — Baseline Consolidation and Handover

**Baseline:** `0.3.0-alpha.4`  
**Target platform:** Kali Linux, XFCE, X11  
**Status:** Accepted working development baseline; not a production release

## Purpose

This document consolidates the product and engineering decisions made through the alpha.4 Control Center milestone. It is the handover point for subsequent work. The source code and existing architecture decision records remain authoritative; this document summarizes their current application.

## What is established

- **Product scope:** a cohesive desktop-experience enhancement suite, initially for Kali XFCE/X11. It is not a replacement desktop environment or window manager.
- **Window management:** `xfwm4` remains authoritative. Kali UX requests actions through supported desktop/X11 interfaces and observes the result.
- **Architecture:** a modular monolith with a shared core, feature modules, platform adapters, diagnostics and a GTK3 presentation layer. Avoid a separate daemon for every feature.
- **UI toolkit:** GTK3/PyGObject for the current target. GTK, GDK, Pango and libwnck namespaces are explicitly version-pinned in the shared loader.
- **Configuration:** XDG locations, validated JSON settings and atomic owner-only writes. Do not use `sudo pip` or run the GUI as root.
- **Feature catalogue:** the registry is a catalogue of bundled features, not a third-party plugin loader.
- **Feature state:** implementation maturity, runtime availability and the user's enabled preference are separate concepts. An enabled preference does not claim that a process is running.
- **Safety and user control:** status and diagnostics are read-only. Feature toggles do not start privileged services, take input ownership, alter system settings or disable existing tools.
- **Gesture ownership:** one authoritative gesture recognition/routing path. The input provider must be validated on the target machine; do not assume `libinput debug-events` is a production event API.
- **Delivery discipline:** implement a narrow vertical slice, test it, document its limitations and checkpoint it before expanding scope.

See `ARCHITECTURE.md`, `DESIGN_PRINCIPLES.md`, `SECURITY_AND_PRIVACY.md` and `decisions/` for the detailed rationale.

## Work consolidated through alpha.4

### Engineering foundation

- Python `src/` package, CLI, test suite and developer documentation.
- XDG path and configuration handling, diagnostics and platform capability detection.
- GTK3/GDK3/libwnck/Pango version selection centralized in `platform/gtk.py`.
- Feature registry and modular feature package boundaries.

### Existing feature work

- SwipeSwitch engine integrated in `features/window_switcher/engine/`, including gesture recognition, window tracking, Task View, desktop actions and workspace navigation.
- Snap Assist prototype, clipboard history prototype, Quick Panel, Focus Tools, application launcher and Layout Memory.
- Window Overview reuses the existing Task View implementation.
- Window Peek remains planned; screenshot capture is not implemented.

### Control Center alpha.4

- Persistent GTK sidebar/Stack navigation and the Overview, Features, Windows, Clipboard, Applications, Productivity, Appearance, Gestures, Privacy, Diagnostics and About sections.
- `ControlCenterModel` connects the feature catalogue, detected capabilities and saved feature preferences.
- Feature enablement is rejected when the implementation is planned or requirements are missing; disabling a saved preference remains possible.
- Feature-specific controls are gated by the saved preference and detected availability.
- Settings are persisted atomically with owner-only permissions.

The user has reported that alpha.4 works as described on their Kali desktop. This is a useful desktop smoke-test result, not proof that every individual feature or edge case has passed acceptance.

## Feature maturity at this baseline

| Area | Baseline classification | Remaining proof |
|---|---|---|
| Control Center | Implemented foundation | Further accessibility, scaling, keyboard and interaction checks |
| SwipeSwitch | Integrated prototype | Input-provider proof, hardware gestures, window lifecycle and overlay acceptance |
| Task View | Integrated prototype | Focus, dismissal, keyboard navigation and multi-window checks |
| Snap Assist | Prototype | `xfwm4` geometry, panel work areas, scaling and multi-monitor checks |
| Gesture Control | Foundation | Supported provider and conflict/ownership strategy |
| Clipboard History | Prototype | Privacy review and clipboard-manager behaviour; history is session-only |
| Quick Panel / Focus Tools | Prototype | Validate actual XFCE tools and notification daemon behaviour |
| Application Launcher | Prototype | Search, launch, icons and keyboard interaction refinements |
| Layout Memory | Prototype | Best-effort restoration and monitor/workspace edge cases |
| Window Peek | Planned | Capture implementation and compositor-aware design do not exist yet |

The feature registry and `IMPLEMENTATION_STATUS.md` remain the source for current requirement-level detail.

## Verification record

Independent review of the alpha.4 source archive:

- Automated suite: **46 passed, 1 skipped** when run with `PYTHONPATH=src`.
- Skipped test: libwnck tracker integration, because the review container did not provide the required PyGObject/libwnck runtime.
- Wheel construction: passed.
- CLI status in the review container: ran, but correctly reported the container's platform capabilities rather than the user's Kali desktop.
- Live GTK rendering and real touchpad behaviour are not established by container tests.

For a clean source checkout, either install the project in the documented development environment or use `PYTHONPATH=src` when running tests directly. The ZIP archive intentionally does not contain a virtual environment or Git metadata.

## Known boundaries — do not silently expand scope

- `libinput debug-events` is currently used by the SwipeSwitch listener. It is a diagnostic interface; production suitability, permissions and device ownership are unresolved.
- Do not automatically disable or reconfigure Touchégg, libinput-gestures, Fusuma, Gebaar or other existing input tools.
- No autostart, systemd service, privileged installer or system-wide configuration mutation is enabled by default.
- GTK/libwnck integration, multi-monitor geometry, compositor behaviour and clipboard-manager interoperability need target-desktop validation.
- Wayland and other desktop environments are separate future compatibility efforts, not implied by the X11 implementation.
- Debian install/upgrade/remove lifecycle and a signed APT repository are later release work.

## Current SwipeSwitch source-review findings

A static review of the alpha.4 engine has now been recorded in `SWIPESWITCH_CURRENT_SOURCE_AUDIT.md`. The main conclusions are:

- Keep the normalized event contract, pure `GestureRecognizer`, controller, libwnck tracker and workspace service as the initial design.
- Prove the input provider and permissions before attempting broader integration. `libinput debug-events` remains unproven as a production event source.
- Make `--check` a genuinely non-mutating diagnostic that can report individual capabilities without requiring every runtime dependency.
- Resolve unused/partially implemented SwipeSwitch configuration fields deliberately.
- Add deterministic controller, Show Desktop partial-failure, tracker and Task View interaction tests.
- Improve overlay overflow/monitor handling and acknowledge that thumbnails are currently a stub.
- Decide how standalone TOML settings relate to Kali UX preferences before merging configuration ownership.

This is a source-level assessment only. It does not claim the listener, gestures, overlay or window operations have passed live hardware acceptance.

## Next milestone: SwipeSwitch audit and acceptance

The next phase is **audit first, integration second**. Do not begin by rewriting or extracting the engine.

1. Treat the alpha.4 engine and the preserved SwipeSwitch specifications as the source material. Confirm that the available archive is the latest working source before making changes.
2. Establish a clean test baseline and map the actual entry points, modules, dependencies, configuration and process lifecycle.
3. Trace every gesture in `docs/PRODUCT_SPECIFICATION.md` through event parsing, recognition, controller action and tests. Record the direction/sign convention and cancellation behaviour.
4. Audit device discovery, `libinput debug-events`, permissions and coexistence with existing gesture tools on the actual Kali machine. This is a proof of concept, not permission to change the system.
5. Audit libwnck tracking, MRU ordering, activation, workspace filtering, minimized/sticky windows and window destruction.
6. Audit Show Desktop snapshot/restoration and workspace navigation, including partial failures and user changes while a snapshot is active.
7. Audit switcher overlay, Task View, keyboard/mouse navigation, dismissal, thumbnails, theme, scaling, fullscreen windows and multiple monitors.
8. Record findings as **Keep / Improve / Replace / Missing**, each with source evidence, test evidence and a clear reason.
9. Only after the audit, agree on the boundary between the engine and Kali UX. Prefer a small feature adapter/service interface while preserving SwipeSwitch's standalone identity unless the evidence supports a different decision.
10. Implement one focused change at a time; run automated tests and then repeat target XFCE/X11 acceptance checks.

### SwipeSwitch exit criteria

- The supported input source is proven on the target Kali system and does not interfere with normal touchpad operation.
- All specified gestures have deterministic direction, thresholds, reversal and cancellation behaviour.
- Window tracking and activation behave correctly for real XFCE/X11 windows and workspace changes.
- Overlay and Task View behaviour are predictable, keyboard-accessible and do not strand focus.
- Startup, shutdown, disable and failure paths leave no orphaned listener or overlay process.
- Existing gesture tools are not silently modified or disabled.
- The integration boundary and standalone packaging decision are documented.

## Work after SwipeSwitch

Once SwipeSwitch meets its acceptance criteria, proceed in the agreed order:

- Window backend and Snap Assist, retaining `xfwm4` as the authority.
- Desktop overview and navigation.
- Gesture and shortcut management, using the validated input provider and one dispatcher.
- Productivity modules, one at a time.
- Accessibility, performance, Debian packaging and release engineering.
- Other desktop environments and Wayland only as separately designed compatibility work.

## Checkpoint policy

Keep alpha.4 unchanged as the known-good baseline. Use a version-control branch for the next phase in the user's working repository. Make a commit after the audit, after the provider proof of concept, and after each accepted implementation increment. A source ZIP is a portable snapshot; it does not preserve Git history.
