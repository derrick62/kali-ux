# Kali UX interactive prototype guide

This release adds an interactive GTK3 Control Center. It is a desktop prototype, not a claim of production readiness.

## Working interactions

- **Overview:** navigation to major features and read-only diagnostics.
- **Windows:** libwnck window list, activation, Task View, and eight `wmctrl` geometry presets.
- **Clipboard:** opt-in session-only text capture, search, copy-back and clear. Data is not persisted. This is not a password-manager detector; pause capture before copying secrets.
- **Applications:** search XDG desktop entries and launch using `gio launch`.
- **Productivity:** optional XFCE notification do-not-disturb toggle, shortcuts to installed XFCE settings tools, and named window geometry snapshots.
- **Settings:** explicit SwipeSwitch launch, config initialization, implementation notes and privacy explanation.

## Known prototype boundaries

- Gesture input remains explicitly launched through SwipeSwitch; Kali UX does not silently take ownership of libinput or disable other gesture tools.
- Gesture arbitration is an in-process contract only. A shared provider and production multi-feature routing are not yet integrated.
- Snap Assist selects the active window's monitor work area when GDK exposes it. Window-manager constraints, panel interactions and multi-monitor edge cases still need live validation.
- Clipboard capture is memory-only and depends on GTK clipboard ownership notifications. It may not observe every clipboard manager/provider behaviour.
- Layout restoration uses X11 window IDs and geometry. It is best-effort; application identity, monitor and workspace restoration are not guaranteed.
- Window Peek screenshot capture, Wayland support, and a custom quick-settings shell are not implemented.
- The GTK application requires distribution-provided PyGObject, GTK3 and libwnck. A generic Python virtual environment may not see system GI bindings; see README.

## Safety

No automatic startup, privileged helper, system-wide input permission change, XFCE configuration rewrite, clipboard persistence or telemetry is installed/enabled by this prototype.
