# Kali UX

**Kali UX** is a modular desktop-experience suite for Kali Linux. The first target is XFCE on X11. It aims to bring useful, deliberate desktop interactions together while preserving Linux user control and leaving `xfwm4` as the window manager.

> **Implementation status:** integrated engineering baseline / early alpha. This archive contains the shared core, feature service foundations, and the SwipeSwitch v0.2.0 preview engine. It is not yet a polished, fully verified desktop product. Some features have working domain services but do not yet have complete GTK interfaces or live desktop integration. See `docs/IMPLEMENTATION_STATUS.md`.

## Included features

| Feature | Included baseline | Current limitation |
|---|---|---|
| SwipeSwitch | Existing GTK3/libwnck switcher, Task View, gesture recognizer, desktop/workspace actions | Inherited audit findings; requires Kali X11 live validation |
| Shared Gesture Control | Normalized event contract and in-process router | No production input provider/arbitration daemon; disabled by default |
| Window Overview | Reuses SwipeSwitch Task View | Needs real desktop focus/dismissal testing |
| Snap Assist | Eight geometry presets via `wmctrl` | No polished preview/assist UI; monitor work-area calculation remains to do |
| Clipboard History | Bounded, searchable, deduplicated privacy-first model | No clipboard watcher or GTK history panel; persistence off by default |
| Quick Panel | Delegates to existing XFCE settings applications | No panel UI; optional tools may be absent |
| Focus Tools | Reversible XFCE notification do-not-disturb helper | Requires target XFCE notification daemon behaviour validation |
| Application Launcher | XDG desktop-entry discovery/search/launch | Needs desktop-entry Exec parsing and GTK launcher UI hardening |
| Window Peek | Capability reporting | Screenshot capture deliberately not implemented |
| Layout Memory | User-triggered geometry snapshots/restoration via `wmctrl` | Best-effort; does not guarantee workspace/monitor fidelity |
| Control Center | Feature/configuration model | GTK interface not yet implemented |
| Diagnostics | Read-only platform capability report | More diagnostic probes and redaction review needed |

## Platform contract

- Initial target: Kali Linux, XFCE, X11.
- `xfwm4` remains authoritative for window management.
- No automatic changes to XFCE settings, other gesture services, input permissions, or system files.
- No GUI process should run as root.
- Gesture listener startup is explicit; the default `kali-ux status` command is read-only.
- Wayland and other desktop environments are future targets.

## Install for development

Use a virtual environment for Python packaging, but install GTK bindings from the distribution packages:

Follow [`docs/INSTALL.md`](docs/INSTALL.md) for the full dependency and environment setup. In particular, create the virtual environment with `--system-site-packages` so it can access the distribution-provided PyGObject/GTK bindings. Do not use `sudo pip`.

After installation, initialize and launch the Control Center with `kali-ux init` and `kali-ux gui`. Start the gesture listener separately with `kali-ux swipeswitch` only when you explicitly want it.

The suite does not install itself as an autostart item or enable a gesture provider. That should only be done after the user has validated the device, permissions, and conflicts on their machine.

## Configuration and data

- Config: `$XDG_CONFIG_HOME/kali-ux/config.json` (default `~/.config/kali-ux/config.json`)
- Data: `$XDG_DATA_HOME/kali-ux` (default `~/.local/share/kali-ux`)
- Cache: `$XDG_CACHE_HOME/kali-ux` (default `~/.cache/kali-ux`)
- Runtime: `$XDG_RUNTIME_DIR/kali-ux`

Clipboard history is in-memory only in this baseline. No clipboard text is written to logs or disk. Layout snapshots are only written after an explicit capture call and are stored with user-only permissions.

## Project map

```text
src/kali_ux/
  core/                  configuration, paths, feature registry
  platform/              capability and command adapters
  features/              independently bounded feature modules
  control_center/        configuration-facing model
  diagnostics/           read-only health reporting
  ui/                    shared UI foundations (future GTK integration)
docs/                    product, architecture, decisions, testing, packaging
packaging/               Debian packaging notes and templates
scripts/                 safe developer/release helpers
```

## Engineering approach

Build the whole feature ecosystem as an integrated baseline, then polish feature-by-feature. Do not confuse a module stub with a finished user-facing feature. Every capability must be tested on real XFCE/X11, including multiple monitors, scaling, panels, fullscreen windows, workspaces, minimized windows, and input-device changes.

See `docs/IMPLEMENTATION_STATUS.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`, `docs/SECURITY_AND_PRIVACY.md`, and `docs/DEVELOPMENT.md`.

## Interactive Control Center prototype

After installing the project and the GTK/X11 system dependencies, launch the desktop UI with:

```bash
kali-ux gui
```

The UI provides working prototype interactions for window listing/activation, Task View, eight snap presets, opt-in in-memory clipboard history, application search/launch, XFCE quick settings, focus mode, layout snapshots and diagnostics. See `docs/PROTOTYPE_GUIDE.md` for behaviour and limitations. The application menu entry template is in `packaging/kali-ux.desktop`.

The original SwipeSwitch design, gesture, architecture, testing and development notes are preserved under `docs/swipeswitch/` alongside the integrated project documentation.

For a copy-paste installation procedure, see [`docs/INSTALL.md`](docs/INSTALL.md).
