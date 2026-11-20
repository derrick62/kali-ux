# SwipeSwitch integration

The GTK3/libwnck SwipeSwitch engine is integrated under `engine/`. Run `kali-ux swipeswitch` or `kali-ux-swipeswitch` in an X11 session after installing the system GTK3/libwnck bindings and libinput tooling.

The live gesture recognizer is in `gestures.py`; its immutable input event contract is in `events.py`. The unused legacy state machine has been removed. Automated tests cover routing, reversal, interruption, cancellation and timeout behaviour.

This remains an integration prototype, not a declaration of complete desktop acceptance. The listener currently reads `libinput debug-events`, which still needs a target-version and permission proof of concept. The thumbnail module is a stub, and multi-monitor overlay behaviour needs live testing. The feature is not automatically started and does not modify other gesture services.
