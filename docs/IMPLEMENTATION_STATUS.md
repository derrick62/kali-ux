# Implementation status — interactive prototype

**Release:** 0.3.0-alpha.4
**Target:** Kali Linux / XFCE / X11
**Verification environment:** Linux build container, not a live Kali desktop

## Interactive features now present

- **Kali UX Control Center:** GTK3 desktop dashboard with sidebar navigation for Overview, Features, Windows, Clipboard, Applications, Productivity, Appearance, Gestures, Privacy, Diagnostics and About. Feature preferences are managed through `ControlCenterModel`; controls are gated by saved preferences and detected availability.
- **SwipeSwitch:** integrated GTK3/libwnck engine, command-line entry point, gesture recognizer, MRU window tracking, Task View, Show Desktop/restoration and workspace navigation.
- **Window list:** enumerates normal task-list windows and requests activation.
- **Snap Assist:** eight geometry presets requested through `wmctrl`; the Control Center targets the active window's monitor work area when GDK exposes it.
- **Clipboard History:** opt-in GTK clipboard-owner monitoring, asynchronous text retrieval, bounded in-memory history, search, copy-back and clear. Retention limits are configurable; no persistence or application-specific exclusions are implemented.
- **Application Launcher:** searchable XDG desktop-entry discovery and launch through `gio launch`.
- **Quick Settings:** starts installed XFCE display, sound, network, power and keyboard configuration tools without blocking the Control Center.
- **Focus Mode:** reversible request to XFCE notification do-not-disturb, retaining the previous value and preserving it if restoration fails.
- **Layout Memory:** named, explicit window geometry capture and best-effort restore; snapshots omit window titles and are written atomically with user-only permissions.
- **Diagnostics and configuration:** read-only platform capability report, model-backed feature status, validated settings and atomic owner-only configuration writes.
- **Shared gesture contract:** the in-process router now owns the recognizer lifecycle and routes recognised actions to one explicit feature owner. SwipeSwitch is the first consumer; the router remains disabled until the opt-in input listener starts.

## Engineering corrections in alpha.2, alpha.3 and alpha.4

- Removed the unused legacy `state.py` implementation and moved the shared immutable event contract into `events.py`. The live `GestureRecognizer` is now the single source of gesture lifecycle behaviour.
- Corrected the reversal acceptance test: cumulative movement can cross back over the original step and then move one further step, which correctly emits two reverse steps.
- A finger-count change or unexpected new gesture begin now cancels an active switcher immediately rather than leaving its overlay open until timeout.
- Added a detached command launcher for graphical applications. Quick Settings, Gio application launches and opening the config folder no longer use a blocking command runner.
- Focus Mode no longer overwrites the original notification setting on repeated enable requests, and it retains the recovery value if restoration fails.
- Snap requests stop if the active window cannot be unmaximized; the UI selects the active window's monitor work area where supported.
- Layout snapshots are atomically written, have private permissions, validate window IDs and omit potentially private window titles.
- Reformatted Python source and tests and resolved the configured Ruff lint rules.
- Alpha.3 centralizes PyGObject namespace loading and explicitly pins GTK 3, GDK 3, libwnck 3 and Pango 1.0 before importing them. This fixes the GTK3/GDK4 namespace collision found during target-machine startup.
- Removed the stale legacy state-machine module and its two expected-failure tests; the live `GestureRecognizer` remains the single implementation under test.
- Alpha.4 connects the GTK interface to `ControlCenterModel`, adds runtime capability-aware availability and separates maturity from enabled preference.
- Feature preference writes now use same-directory temporary files, owner-only permissions and atomic replacement. Invalid non-boolean `enabled` settings are rejected.
- Replaced the tabbed notebook with GTK stack/sidebar navigation and added dedicated Features, Appearance, Gestures, Privacy, Diagnostics and About sections.
- Feature controls are enabled only when the feature is both enabled in configuration and available on the current platform. Feature toggles never start services or change system settings.

## Known limitations — do not represent as complete

- The SwipeSwitch input listener still uses `libinput debug-events`. It is a diagnostic command, not a proven stable production event API. Device ownership, permissions, coexistence with other gesture services and hardware behaviour require a proof of concept on target Kali.
- The shared router currently has one consumer (SwipeSwitch). Additional gesture features must register through this router rather than start independent recognizers or listeners.
- The libwnck tracker integration test is skipped in the build container because PyGObject/libwnck is unavailable there.
- Task View focus/dismissal, window activation, gesture direction/feel and overlay behaviour need live XFCE/X11 validation.
- Snap geometry uses monitor work areas when available, but window-manager constraints, fractional scaling, panels and unusual monitor layouts still need live testing.
- Clipboard monitoring is session-only and depends on GTK clipboard-owner notifications. It cannot identify every sensitive value or observe every clipboard-manager implementation. Application-specific exclusions are not implemented; pause capture before copying secrets.
- Layout restoration is best-effort and does not guarantee application identity, workspace or monitor restoration. Window IDs can become stale between capture and restore.
- Focus-mode property semantics vary with XFCE notification daemon versions and need validation.
- Window Peek screenshot capture and compositor-aware thumbnails are not implemented; no fake preview is shown.
- Gesture provider arbitration, custom Quick Settings shell, Wayland and other desktop environments are future work.
- No privileged installer, autostart, systemd service or system configuration mutation is enabled by default.

## Automated verification

The current build-container run records **46 passed, 1 skipped, 0 expected failures**. Python bytecode compilation and wheel construction succeeded. Ruff checks are part of `scripts/check.sh` but were not run in this review container because Ruff is unavailable. The GTK UI has not been launched in a live desktop session from this build container; this does not constitute live desktop acceptance. See `docs/VERIFICATION_REPORT.md`.
