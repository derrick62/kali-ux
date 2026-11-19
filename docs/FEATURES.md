# Kali UX — Feature inventory

| Feature | Baseline included | Remaining work |
|---|---|---|
| SwipeSwitch | Existing GTK3/libwnck engine integrated | Resolve acceptance tests, thumbnails, multi-monitor, provider and live QA |
| Shared Gesture Control | Normalized event model and static router | Production provider, arbitration lifecycle, cancellation and conflict UX |
| Task View / Window Overview | Reuses SwipeSwitch Task View | Keyboard/focus/dismissal QA and UI refinement |
| Snap Assist | Eight geometry presets through wmctrl | Work-area detection, preview UI, monitor selection and robust error recovery |
| Clipboard History | Bounded in-memory model, search, deduplication, exclusions hook | X11 clipboard backend, UI, sensitive-app detection and explicit persistence controls |
| Quick Panel | XFCE settings action adapters | GTK panel, capability-aware controls and graceful missing-app states |
| Focus Tools | Reversible notification DND helper | Verify property semantics and build session UI/timer |
| Application Launcher | Desktop-entry discovery and basic search/launch | Complete Exec parsing, icons, categories, keyboard navigation and GTK UI |
| Window Peek | Capability reporting and honest unsupported response | Secure compositor-aware capture backend |
| Layout Memory | Explicit named geometry snapshots and best-effort restore | Workspace/monitor identity, validation, UI and undo |
| Control Center | Configuration model | GTK interface, validation, per-feature status and reset UX |
| Diagnostics | Read-only platform report | Input/GTK/WM probes, redaction, support bundle and UI |

Feature services are intentionally implemented before all their visual interfaces. The table distinguishes included code from complete user-facing functionality.
