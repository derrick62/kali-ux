# SwipeSwitch integration

The v0.2.0 preview engine has been carried into `engine/` with its original module boundaries retained. Run `kali-ux swipeswitch` or `kali-ux-swipeswitch` in an X11 session after installing the system GTK3/libwnck bindings and libinput tooling.

This is an integration baseline, not a declaration that the upstream preview has passed the complete desktop audit. Known audit findings remain in `docs/SWIPESWITCH_AUDIT_PRELIMINARY.md`. In particular, the thumbnail module is a stub, multi-monitor support is primary-monitor-only, the libinput debug-events text interface needs target-version validation, and the legacy state machine/tests contain unresolved semantics. The feature is disabled by default and no gesture listener starts from the suite's default CLI.
