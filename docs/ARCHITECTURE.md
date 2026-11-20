# Kali UX — Architecture Specification

**Status:** Architecture baseline for the 0.3.0-alpha.3 prototype. Some planned adapter boundaries remain future work and must be validated against the target desktop.

## 1. Architectural approach

Use a modular Python application with a shared core and feature modules. Begin as a single user-session process unless measured requirements justify a separate process. Do not begin with microservices, a plugin marketplace or a daemon per feature.

The architecture should make platform-specific code replaceable without pretending that every desktop environment exposes identical capabilities.

## 2. Logical layers

```text
User interface (GTK)
        |
Feature modules
        |
Shared application core
        |
Platform adapters
        |
XFCE / xfwm4 / X11 / input services
```

### User interface
Owns GTK windows, overlays, input focus, presentation and accessibility. GTK objects and mutations stay on the GTK main thread. Long-running or blocking operations must not block it.

### Feature modules
Own user-visible use cases: switcher, overview, snapping, clipboard, quick panel, focus tools, launcher and layout memory. A feature should depend on documented core/platform interfaces, not another feature's private implementation.

### Shared core
Only shared responsibilities belong here:
- Application lifecycle and shutdown.
- Configuration discovery, parsing, validation and change notification.
- Logging and diagnostics.
- Feature registration and enablement.
- Capability reporting.
- Optional event dispatch where asynchronous fan-out is genuinely required.

Avoid a generic event bus until actual producers/consumers and ordering/error semantics are known. Direct interfaces are preferable for simple request/response operations.

### Platform adapters
Provide explicit interfaces for capabilities such as window enumeration, window activation, workspace navigation, desktop visibility, input events and clipboard access. The initial implementation targets X11/XFCE. Adapters must report unsupported capabilities rather than silently pretending they work.

## 3. Initial package map

```text
src/kali_ux/
  __init__.py / __main__.py / cli.py
  core/
    config.py
    paths.py
    registry.py
  platform/
    capabilities.py
    commands.py
    gtk.py
  ui/
    app.py
  features/
    window_switcher/engine/
      events.py, listener.py, gestures.py, controller.py
      tracker.py, activator.py, workspaces.py, desktop.py
      overlay.py, task_view.py, config.py, thumbs.py
    gesture_control/router.py
    snap_assist/service.py
    window_overview/service.py
    clipboard_history/service.py
    quick_panel/actions.py
    focus_tools/service.py
    launcher/service.py
    window_peek/service.py
    layout_memory/service.py
  control_center/model.py
  diagnostics/report.py

tests/
docs/
packaging/
scripts/
```

Create implementation packages only when code exists. Feature folders may initially contain concise README files defining scope and status. Do not fill the repository with empty Python modules or speculative abstractions.

## 4. Window-management boundary

`xfwm4` remains authoritative for placement, stacking, focus, workspaces and decorations. Kali UX observes desktop state and requests supported operations through established X11/EWMH mechanisms or a suitable library.

The application must not independently maintain a competing model of window geometry or focus. It may maintain derived state such as MRU ordering or a restoration snapshot, but must reconcile that state with actual window-manager events.

Use EWMH where applicable and verify the exact operation against `xfwm4`. `libwnck` is a candidate abstraction for window/workspace discovery and activation, not a guaranteed answer for every operation.

## 5. Gesture architecture

The suite must avoid multiple independent components competing for the same physical gesture.

Intended flow:

```text
Touchpad / supported input source
              |
      Input acquisition adapter
              |
      Normalized gesture events
              |
      Gesture lifecycle + recognizer
              |
       Gesture ownership/router
              |
       Feature action interface
              |
       Window/workspace service
```

Separate:
- **Acquisition:** how events are obtained.
- **Normalization:** convert raw lines/events into a stable internal model.
- **Recognition:** classify finger count, direction, movement and lifecycle.
- **Arbitration:** determine which feature owns a gesture.
- **Action:** request the desktop operation.
- **Presentation:** update GTK UI.

The six SwipeSwitch gestures are specified in `PRODUCT_SPECIFICATION.md`. Do not treat `libinput debug-events` as a production API merely because it is useful for diagnostics. It is a command-line diagnostic tool; event acquisition, permissions, stability and compatibility require a proof of concept. The actual event format must be captured on the target machine and represented by fixtures.

Gesture lifecycle must account for begin/update/end/cancel, sequence changes, finger-count changes, timeouts, device removal and rapid successive gestures. A cancelled gesture must not commit an action.

Existing tools such as `libinput-gestures` or Touchégg may already own gestures. Detect and explain conflicts. Never silently edit their configuration or stop their services.

## 6. SwipeSwitch integration boundary

SwipeSwitch originated as a separate project and is now integrated under `features/window_switcher/engine/`. Its original design and development notes remain under `docs/swipeswitch/`, and its source boundaries remain explicit. The integration was audit-first rather than a blind rewrite.

The remaining long-term packaging decision is whether to retain the current integrated feature module, extract reusable domain logic into a separately reusable package while preserving the standalone project, or keep the runtime separately packaged if isolation proves necessary. Review the source license and release workflow before changing the current arrangement. Preserve the ability to release SwipeSwitch independently unless there is a clear reason to change that.

## 7. Threading and process model

- GTK UI operations run on the GTK main thread.
- Input acquisition may run in a worker thread or subprocess if the selected mechanism requires it.
- Cross-thread UI updates use GLib main-context dispatch.
- Subprocesses must have bounded output handling, explicit shutdown, timeouts and restart/backoff policy where appropriate.
- Avoid shell interpolation for commands; pass argument arrays.
- Ensure child processes terminate on logout and application shutdown.
- A single-instance mechanism should be chosen only after the runtime/process design is clear.

## 8. Configuration and filesystem

Follow the XDG Base Directory Specification and honor environment overrides:
- Config: `$XDG_CONFIG_HOME/kali-ux` (default `~/.config/kali-ux`).
- Data: `$XDG_DATA_HOME/kali-ux` (default `~/.local/share/kali-ux`).
- Cache: `$XDG_CACHE_HOME/kali-ux` (default `~/.cache/kali-ux`).
- Runtime: `$XDG_RUNTIME_DIR/kali-ux` when available.

Configuration should be validated, have safe defaults and tolerate unknown keys where compatibility permits. Never store secrets or clipboard payloads in logs. User settings must not be overwritten during upgrades.

## 9. Security and privacy boundaries

Run as the logged-in user. No setuid, no root GUI process and no blanket privileged helper. Any required device permission must be narrowly justified and documented. Do not read keyboard input for a touchpad gesture feature. Do not log raw input streams by default. No telemetry or network dependency is planned.

Clipboard history requires a separate data-handling design before implementation. It must define persistence, retention, exclusions, pause and clear semantics.

## 10. Failure isolation

A feature failure should not bring down unrelated features. Configuration errors should identify the affected setting and use a safe fallback only when safe. Platform adapters should return explicit unsupported/error outcomes. Overlays must always have a dismissal/recovery path. No operation should leave the desktop in an unrecoverable state.

## 11. Architecture decisions still open

- Production gesture event source and permission model.
- Whether input routing is in-process or a separate user process.
- Exact window/workspace library and fallback strategy.
- GTK3 long-term scope versus GTK4 migration.
- Event bus versus direct service interfaces.
- Configuration serialization format.
- Clipboard backend and persistence defaults.
- Single-instance and startup lifecycle mechanism.
- Native versus custom snapping boundary.
- Multi-monitor semantics for overlays and layouts.
- Packaging split between suite and standalone SwipeSwitch.

See `docs/decisions/`.
