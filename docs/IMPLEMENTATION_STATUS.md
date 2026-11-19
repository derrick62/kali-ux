# Implementation status — interactive prototype

**Release:** 0.3.0-alpha.1  
**Target:** Kali Linux / XFCE / X11  
**Verification environment:** Linux build container, not a live Kali desktop

## Interactive features now present

- **Kali UX Control Center:** GTK3 desktop dashboard with Overview, Windows, Clipboard, Applications, Productivity and Settings pages.
- **SwipeSwitch:** preserved GTK3/libwnck engine, CLI entry point and explicit Control Center launch. Original SwipeSwitch design and development documents are preserved under `docs/swipeswitch/`.
- **Task View:** interactive window overview, activation and dismissal using the inherited GTK3 implementation.
- **Window list:** enumerates normal, task-list windows and activates a selected window.
- **Snap Assist:** eight explicit geometry presets (halves, top/bottom and corners) requested through `wmctrl`.
- **Clipboard History:** opt-in GTK clipboard-owner monitoring, in-memory bounded history, search, copy-back and clear. No persistence.
- **Application Launcher:** searchable XDG desktop-entry list and launch through `gio launch`.
- **Quick Settings:** opens installed XFCE display, sound, network, power and keyboard configuration tools.
- **Focus Mode:** reversible request to XFCE notification daemon do-not-disturb, retaining the previous value for the current process session.
- **Layout Memory:** named, explicit window geometry capture and best-effort restore through `wmctrl`.
- **Diagnostics and configuration:** read-only status, default config creation, implementation notes and explicit feature status.
- **Shared gesture contract:** normalized gesture model and in-process router. No production shared input provider is enabled.

## Known limitations — do not represent as complete

- SwipeSwitch's three inherited acceptance failures remain documented; tracker integration is skipped in environments without PyGObject/libwnck.
- Gesture listener still uses `libinput debug-events` and is app-local. Input permission, cancellation, coexistence and hardware behaviour need proof on target Kali. It is never auto-started.
- Task View focus/dismissal and window activation need live desktop validation.
- Snap presets currently use the selected monitor's full geometry, not XFCE panel-adjusted work areas; monitor selection and edge cases need refinement.
- Clipboard monitoring is session-only and depends on GTK clipboard ownership notifications. It cannot identify every sensitive value or observe every clipboard-manager implementation. Pause capture before copying secrets.
- Layout restoration is best-effort and does not guarantee application identity, workspace or monitor restoration.
- Focus-mode property semantics vary with XFCE notification daemon versions and need validation.
- Window Peek screenshot capture and compositor-aware thumbnails are not implemented; no fake preview is shown.
- Gesture provider arbitration, custom Quick Settings shell, Wayland and other desktop environments are future work.
- No privileged installer, autostart, systemd service, or system configuration mutation is enabled by default.

## Verification

See `docs/VERIFICATION_REPORT.md`. Automated Python tests and packaging checks do not prove desktop behaviour. The application requires distribution-provided PyGObject, GTK3 and libwnck, plus X11 desktop utilities.
