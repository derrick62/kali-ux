# SwipeSwitch — alpha.4 current-source audit

**Baseline reviewed:** Kali UX `0.3.0-alpha.4`  
**Review type:** static source and automated-test review  
**Not performed:** live touchpad, permissions, XFCE window-manager, compositor or multi-monitor testing

This report reviews the SwipeSwitch engine actually present in the alpha.4 archive. It supplements, rather than replaces, the historical/preliminary review in `SWIPESWITCH_AUDIT_PRELIMINARY.md` and the original specifications under `docs/swipeswitch/`.

## Overall assessment

The engine has useful separations already: normalized input events, a pure gesture recognizer, a controller, a libwnck tracker, desktop/workspace services and separate GTK views. The right next step is a focused reliability and provider proof of concept—not a rewrite and not immediate extraction into another package.

The largest unresolved risk is the event source. `listener.py` launches `libinput debug-events` against a selected `/dev/input/eventX`. The parser and recognizer can be unit-tested, but this does not prove the listener is a supported production input API, that it has the correct permissions, or that it can coexist with other gesture services without competing for the device.

## Component findings

| Component | Decision | Evidence and next action |
|---|---|---|
| `events.py` | Keep | Small immutable event contract. Preserve as the boundary between providers and recognition. |
| `gestures.py` | Keep / improve | Pure recognizer with cumulative deltas, axis dominance, reversal, cancellation and timeout. Add contract tests for every specified gesture, sign convention and edge transition. |
| `controller.py` | Keep / improve | Useful action coordinator. Add deterministic tests with fake tracker/window/view services, especially disappearing windows and empty/single-window states. |
| `listener.py` | Improve first | Parser accepts two event-header variants and has retry/stop logic. Prove the event source, permissions and device selection on target hardware. Test process exit, stop while blocked, repeated start/stop and malformed event output. |
| `__main__.py` | Improve | `--check` currently loads/creates the SwipeSwitch config, detects a touchpad and imports GTK/libwnck before returning. Split diagnostics into independent checks so a config/dependency check does not require every runtime component. Ensure check mode does not create or mutate configuration. |
| `config.py` | Improve | Uses a separate `~/.config/swipeswitch/config.toml`, which is sensible for standalone compatibility. Several declared settings are not used or are only partially used: `flick_min_px`, `invert_direction`, `use_unaccelerated`, thumbnail options and `theme='auto'`; monitor selection is primary-only. Validate types and document/remove unsupported settings only after compatibility review. |
| `tracker.py` | Keep / improve | libwnck MRU tracking and current-workspace filtering are a reasonable base. Add tests for window close, workspace movement, sticky/minimized windows, dialogs, duplicate XIDs and active-window transitions. Avoid title-prefix exclusion as the only long-term self-window identity mechanism. |
| `activator.py` | Keep / verify | Wnck activation with `wmctrl` fallback is small and bounded. Verify minimized-window restoration and focus behaviour on XFCE. |
| `desktop.py` | Improve | Snapshot/restoration avoids overwriting an existing snapshot and skips already-minimized windows. It currently records the intended snapshot before knowing which minimizations succeeded, and clears the snapshot after a restore attempt even if some windows fail. Define and test partial-failure recovery and user changes during the snapshot interval. |
| `workspaces.py` | Keep / verify | Explicit non-wrapping boundaries and documented left=next/right=previous mapping. Verify on the actual XFCE workspace order and touchpad coordinate convention. |
| `overlay.py` | Improve | Non-focusable overlay and selection updates are useful. It centers on the primary monitor, has no scroll container for large window counts, and `auto` theme currently behaves as dark. Test fullscreen, compositor-off, scaling and multiple displays. |
| `task_view.py` | Improve | Separate GTK overview with cards, Escape and focus-out dismissal. Add keyboard navigation and tests for one window, many windows, activation, focus restoration and click-outside behaviour. |
| `thumbs.py` | Missing | Thumbnail capture is a stub returning `None`. Do not expose a thumbnail setting as working until a bounded, privacy-aware capture path exists. |

## Product-contract trace

The authoritative mapping is in `PRODUCT_SPECIFICATION.md`:

- Three-finger horizontal: switcher begin/move/commit, with cancellation on interrupted or cancelled sequences.
- Three-finger down: Show Desktop snapshot.
- Three-finger up: restore a valid snapshot, otherwise open Task View.
- Four-finger horizontal: next/previous workspace without wrapping.

The source recognizer and controller contain paths for these actions. Automated tests cover the pure gesture and parser path, but source presence is not equivalent to live acceptance. The sign convention, physical left/right feel, thresholds, quick-flick behaviour, cancellation and workspace mapping must be confirmed on the user's touchpad.

## Cross-cutting integration issue

Kali UX has a shared feature preference model, but SwipeSwitch currently reads its own TOML configuration and is launched as a separate `kali-ux-swipeswitch` process. This is not necessarily wrong: ADR 0007 explicitly says to preserve the standalone identity unless evidence supports changing it. The integration design should therefore use a small adapter/launch contract and a deliberate configuration-ownership decision. Do not casually merge or duplicate settings.

## Prioritized next work

### First: provider and diagnostic proof of concept

- On target Kali, record the installed libinput version, `libinput list-devices` output for the touchpad, current gesture tools/services and the exact permissions required.
- Observe normal touchpad operation before and after running the listener. Do not change groups, udev rules or other services during initial observation.
- Capture representative BEGIN/UPDATE/END and cancellation lines without recording unrelated user activity; use fixtures with device identifiers removed.
- Test `--check` as a non-mutating diagnostic. Separate checks for X11, config parsing, touchpad detection, GTK3 and libwnck.
- Decide whether the current event source is acceptable or whether a supported provider/adapter is required. If not, stop and redesign this boundary before adding more gesture behaviour.

### Second: deterministic engine tests

- Add fake-based tests for controller routing and desktop snapshot/restore partial failures.
- Add tracker tests that can run without a live X server where practical; retain a clearly marked integration test for real libwnck.
- Add Task View keyboard/focus and overlay overflow tests where the GTK test environment permits.
- Validate all config fields against the actual product contract; do not silently retain settings that do nothing.

### Third: integration boundary

After the provider and engine behaviour are proven, define a narrow Kali UX feature adapter with explicit start, stop, status, error and configuration semantics. Keep normal GUI operation unprivileged. Preserve standalone invocation and configuration compatibility unless a documented decision changes them.

## Decision gate

Do not call SwipeSwitch production-ready or move on to broad gesture management until input ownership/coexistence, all specified gesture behaviours, cancellation, window activation, Task View dismissal and clean process shutdown pass on the target Kali XFCE/X11 machine.
