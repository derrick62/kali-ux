# Kali UX — Security and Privacy

## Principles

Kali UX is a local desktop utility. Its default design should require no network access, no telemetry and no privileged background process.

## Execution and permissions

- Run as the logged-in user.
- Do not use setuid binaries.
- Do not run GTK interfaces as root.
- Do not request broad device access without a demonstrated need.
- Explain any permission/group change before asking the user to make it.
- Never silently change another gesture service's configuration.
- Avoid shell command construction; use argument arrays and validate inputs.

## Input data

A gesture feature should consume only the minimum input needed to recognize gestures. It must not capture keyboard content. Raw event streams must not be logged by default. Diagnostic mode must be explicit and should still avoid unnecessary personal data.

## Clipboard data

Clipboard history is potentially sensitive. Before implementing persistence, define:
- Whether persistence is off by default.
- Maximum item count and age.
- Exclusion rules for password managers and sensitive applications.
- Pause/resume and clear-all behaviour.
- Whether clipboard payloads are stored on disk.
- File/image handling and size limits.
- Data deletion behaviour on uninstall.

Clipboard contents must never appear in ordinary logs or diagnostic bundles.

## Window metadata

Window titles can contain private information. Diagnostics should not upload or expose titles by default. A support bundle should redact or omit them unless the user explicitly chooses otherwise.

## Network

No network access is required for the initial suite. If a future feature introduces network communication, document its purpose, destination, data types, consent model and failure behaviour before implementation.

## Diagnostics

Diagnostics should include versions, capability checks, sanitized error messages and relevant configuration keys. Exclude credentials, clipboard payloads, raw input, private window titles and personal file paths where possible.

## Safe system changes

Installation must not overwrite user settings. Any optional system integration must be reversible and explained. Prefer user-level XDG autostart over privileged system services for a user-session application.
