# Shared gesture runtime increment

**Base:** Kali UX `0.3.0-alpha.4` public `main` source  
**Status:** automated checks passed in the build container; live Kali acceptance pending

## What changed

- `GestureRouter` can now own an injected recognizer and route its recognised actions. It does not import SwipeSwitch implementation classes; the recognizer is supplied through a small interface.
- The first recognised action claims the gesture for one feature owner. Updates and terminal actions from that same gesture cannot be delivered to a different owner.
- The original end-only `Gesture` registration/dispatch API remains available for compatibility with existing callers.
- `SwipeSwitchController` registers as the `window_switcher` owner and sends normalized input events and timeout checks through the shared router. The recognizer is no longer driven directly by the controller.
- Disabling the router resets the recognizer and clears ownership. Configuration reload replaces the recognizer and closes a visible switcher before doing so.
- Four-finger horizontal gestures now consume distance incrementally, including reversals. A short flick still produces one workspace step when it crosses the gesture threshold but not a full repeat interval.
- The existing `use_unaccelerated` setting is now passed through the listener and parser, including on configuration reload.

## What deliberately did not change

- Input startup remains explicit. The Control Center does not start a listener or change system state merely because a preference is enabled.
- The listener still uses `libinput debug-events`. This is not yet accepted as a production input API; device access, permissions, coexistence and event stability still need a proof of concept on the target Kali machine.
- No other gesture tool, service, autostart entry, input group or device permission is modified.
- The GTK/X11 feature remains the first router consumer. Other gesture features must use the same router rather than adding independent listeners or recognizers.

## Automated verification

- `PYTHONPATH=src pytest -q`: **55 passed, 1 skipped**.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `python -m pip wheel --no-deps --no-build-isolation -w <wheel-dir> .`: passed.
- The one skipped test requires system PyGObject/libwnck integration.
- Ruff was not run because it was unavailable in the build container.

## Live acceptance on Kali XFCE/X11

Run as the normal desktop user, never with `sudo`:

- Start with `kali-ux-swipeswitch --check` and confirm X11, touchpad discovery and GTK/libwnck imports.
- Run `kali-ux-swipeswitch --debug` from a terminal and test three-finger left/right selection, release-to-activate, and cancellation.
- Test four-finger left/right navigation while moving, then reverse direction during the same swipe. Confirm that each crossed distance step moves one workspace and that navigation stops at the available workspace boundary.
- Test a short four-finger flick that crosses the classification threshold but not a full `step_px` interval; it should still move one workspace.
- Repeat with `use_unaccelerated = true` only if the default movement calibration feels unsuitable.
- Close the application and confirm it exits cleanly. Confirm normal pointer/touchpad movement remains unaffected.

A passing automated suite does not replace this live acceptance. Do not enable autostart or change other gesture-provider settings as part of this test.
