# Kali UX

**Kali UX** is a modular desktop-experience suite for Kali Linux. The first target is XFCE on X11. It aims to bring useful, deliberate desktop interactions together while preserving Linux user control and leaving `xfwm4` as the window manager.

> **Implementation status:** 0.3.0-alpha.3 engineering prototype. The repository includes a GTK3 Control Center, the integrated SwipeSwitch engine, and several working desktop-service prototypes. It is not yet a release-ready or live-verified desktop product. See `docs/IMPLEMENTATION_STATUS.md` for the exact boundary between implemented, tested and unverified behaviour.

## Included features

| Feature | Included baseline | Current limitation |
|---|---|---|
| SwipeSwitch | GTK3/libwnck switcher, Task View, gesture recognizer, desktop/workspace actions | Uses `libinput debug-events`; input ownership, permissions and real-device behaviour need target validation |
| Shared Gesture Control | Normalized event contract and in-process router | No production input provider/arbitration daemon; disabled by default |
| Window Overview | Reuses the GTK3 SwipeSwitch Task View | Needs real desktop focus, dismissal and keyboard testing |
| Snap Assist | Eight geometry presets via `wmctrl`, using the active window monitor work area | No preview UI; `xfwm4` geometry acceptance and multi-monitor behaviour need live testing |
| Clipboard History | Opt-in GTK clipboard watcher, bounded in-memory history, search, copy-back and clear | Session-only; app exclusions are not implemented and sensitive values cannot be reliably detected |
| Quick Panel | Launches existing XFCE settings applications asynchronously | Optional tools may be absent; no custom settings shell |
| Focus Tools | Reversible XFCE notification do-not-disturb helper | Requires target XFCE notification daemon behaviour validation |
| Application Launcher | XDG desktop-entry discovery/search and launch through `gio` | No full custom launcher shell, icons or keyboard navigation yet |
| Window Peek | Capability reporting | Screenshot capture deliberately not implemented |
| Layout Memory | User-triggered geometry snapshots/restoration via `wmctrl` | Best-effort; does not guarantee workspace/monitor fidelity |
| Control Center | GTK3 dashboard with Overview, Windows, Clipboard, Applications, Productivity and Settings pages | Prototype UI; accessibility, scaling and interaction polish remain |
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
- Runtime: `$XDG_RUNTIME_DIR/kali-ux` (only when the session provides `XDG_RUNTIME_DIR`)

Clipboard history is in-memory only in this baseline. No clipboard text is written to logs or disk. Layout snapshots are only written after an explicit capture call and are stored with user-only permissions.

## Project map

```text
src/kali_ux/
  core/                  configuration, paths, feature registry
  platform/              capability, command and GTK namespace adapters
  features/              independently bounded feature modules
  control_center/        configuration-facing model
  diagnostics/           read-only health reporting
  ui/                    GTK3 Control Center and presentation
docs/                    product, architecture, decisions, testing, packaging
packaging/               Debian packaging notes and templates
scripts/                 safe developer/release helpers
```

## Engineering approach

Build a reliable vertical slice, then implement and verify additional features one at a time. Do not confuse a service prototype with a finished user-facing feature. Every desktop capability must be tested on real XFCE/X11, including multiple monitors, scaling, panels, fullscreen windows, workspaces, minimized windows, and input-device changes.

See `docs/REVIEW_REPORT.md` for the latest source review, plus `docs/IMPLEMENTATION_STATUS.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`, `docs/SECURITY_AND_PRIVACY.md`, and `docs/DEVELOPMENT.md`.

## Interactive Control Center prototype

After installing the project and the GTK/X11 system dependencies, launch the desktop UI with:

```bash
kali-ux gui
```

The UI provides working prototype interactions for window listing/activation, Task View, eight snap presets, opt-in in-memory clipboard history, application search/launch, XFCE quick settings, focus mode, layout snapshots and diagnostics. See `docs/PROTOTYPE_GUIDE.md` for behaviour and limitations. The application menu entry template is in `packaging/kali-ux.desktop`.

The original SwipeSwitch design, gesture, architecture, testing and development notes are preserved under `docs/swipeswitch/` alongside the integrated project documentation.

For a copy-paste installation procedure, see [`docs/INSTALL.md`](docs/INSTALL.md).
