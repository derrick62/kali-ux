# Kali UX — Feature inventory

| Feature | Baseline included | Remaining work |
|---|---|---|
| SwipeSwitch | GTK3/libwnck engine with current gesture recognizer, switcher and Task View | Validate input ownership, permissions, cancellation, thumbnails and live QA |
| Shared Gesture Control | Normalized event model and static router | Production provider, arbitration lifecycle, cancellation and conflict UX |
| Task View / Window Overview | Reuses SwipeSwitch Task View | Keyboard/focus/dismissal QA and UI refinement |
| Snap Assist | Eight geometry presets through wmctrl, using active-window monitor work area | Preview UI, geometry/monitor edge-case testing and robust user feedback |
| Clipboard History | Opt-in GTK clipboard monitoring, bounded in-memory model, search, deduplication and UI | Sensitive-app detection, clipboard-manager coverage and explicit persistence controls |
| Quick Panel | XFCE settings action adapters launched asynchronously from the GTK UI | Capability-aware controls and graceful missing-app states |
| Focus Tools | Reversible notification DND helper | Verify property semantics and build session UI/timer |
| Application Launcher | Desktop-entry discovery, search and launch through Gio from the GTK UI | Icons, categories, keyboard navigation and richer desktop-entry handling |
| Window Peek | Capability reporting and honest unsupported response | Secure compositor-aware capture backend |
| Layout Memory | Explicit named geometry snapshots and best-effort restore | Workspace/monitor identity, validation, UI and undo |
| Control Center | GTK3 dashboard and configuration-facing model | Settings validation, per-feature status and reset UX |
| Diagnostics | Read-only platform report | Input/GTK/WM probes, redaction, support bundle and UI |

The dashboard provides a prototype interface for several services, but their desktop integration and edge cases are not yet fully verified. The table distinguishes included code from complete user-facing functionality.
