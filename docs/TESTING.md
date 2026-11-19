# Kali UX — Testing Strategy

## 1. Purpose

Desktop software crosses several boundaries: Python logic, GTK, X11, window-manager behaviour, input devices, session lifecycle and packaging. A passing unit test is necessary but cannot prove that an overlay behaves correctly on a real XFCE session.

Testing is layered so that failures can be localized and claims remain honest.

## 2. Test levels

### Unit tests
Test pure logic without a desktop session:
- Gesture parsing and normalization.
- Gesture state machine and direction classification.
- Arbitration and ownership rules.
- MRU ordering and window filtering using fakes.
- Show Desktop snapshot creation/reconciliation.
- Configuration parsing, validation and defaults.
- Layout calculation and feature state transitions.

### Component tests
Test a component with controlled dependencies:
- Window tracker with fake window events.
- Gesture router with fake feature handlers.
- Clipboard policy with a fake backend.
- GTK-independent overlay view models.

### Integration tests
Run in a controlled X11/XFCE environment:
- EWMH window enumeration and activation.
- Workspace navigation and boundaries.
- Minimize/restore operations.
- Desktop visibility state.
- GTK overlay stacking, focus and dismissal.
- Input subprocess lifecycle and permissions.
- Configuration and startup integration.

### Manual desktop tests
Required for real user interaction:
- Physical touchpad gesture direction and feel.
- Gesture cancellation and rapid repetition.
- Overlay behaviour above fullscreen windows.
- Compositor on/off.
- Multi-monitor and scaling.
- XFCE panel coexistence.
- Login, logout, suspend/resume and device reconnect.
- Interaction with existing gesture services.

### Packaging tests
- Clean install.
- Upgrade from prior version.
- Reinstall.
- Removal.
- Interrupted install/upgrade.
- Missing dependencies.
- Preservation of user configuration.
- No root-owned user files and no privileged GUI process.

## 3. SwipeSwitch test matrix

### Gesture input
- BEGIN / UPDATE / END normal lifecycle.
- END cancelled.
- Missing or optional sequence identifiers.
- Unexpected whitespace and event-line variations.
- Unsupported finger counts.
- Finger-count changes during gesture.
- Diagonal motion and direction threshold.
- Very short, slow and fast gestures.
- No END event / timeout.
- Input process exits, device disconnects and reconnects.

Capture real event output from the target touchpad and preserve sanitized fixtures. Do not fabricate fixtures from assumptions about the command's output.

### Window switching
- 0, 1, 2, 3 and 10+ eligible windows.
- MRU ordering.
- Sticky and current-workspace windows.
- Minimized window selected.
- Window closes during gesture.
- Workspace changes mid-gesture.
- Excluded panel/dock/desktop/overlay windows.
- Activation failure and focus-stealing constraints.

### Show Desktop and restoration
- Several visible windows.
- One visible window.
- A mix of visible and already minimized windows.
- Repeated down gesture does not replace snapshot.
- A window closes while desktop is shown.
- A new window opens while desktop is shown.
- A window changes workspace.
- Restoration after partial external state change.
- No valid snapshot: three-finger up opens Task View.
- Valid snapshot: three-finger up restores the previous visible set.
- Only one eligible window: Task View still opens and works.

### Workspace navigation
- Zero/one/multiple workspaces where environment permits.
- First and last workspace boundaries.
- Correct left/right mapping.
- Sticky windows.
- Rapid repeated navigation.
- Interaction with workspace changes from keyboard or panel.

### Regression and stress
- At least 50 consecutive gesture cycles without a stuck overlay as an initial smoke criterion.
- Repeated open/dismiss and rapid direction reversal.
- Listener termination and restart.
- GTK shutdown while worker is active.
- Long-running idle session and memory observation.

## 4. Test tooling

Use `pytest` for Python tests. Use `ruff` for linting. Add type checking only when it provides value and can be configured consistently. Desktop integration tests should be explicitly marked and skipped with a clear reason when the required X11/XFCE environment is unavailable.

## 5. Test evidence

For each milestone record:
- Commit or source revision tested.
- OS, desktop, window manager and session type.
- Python and relevant library versions.
- Commands run.
- Pass/fail counts.
- Manual scenarios completed.
- Known failures and limitations.
- Whether the result is unit-tested, integration-tested or manually verified.

## 6. Definition of done

A feature is done only when:
- Requirements and acceptance criteria exist.
- Relevant automated tests pass.
- Desktop integration and manual tests pass where needed.
- No known high-severity regression remains.
- Error handling and recovery are tested.
- Documentation and changelog are updated.
- Installation/removal impact is understood.
- The implementation status is accurately labelled.
