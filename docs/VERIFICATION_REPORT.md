# Verification report

**Build:** Kali UX 0.3.0-alpha.1  
**Environment:** Linux build container; no live Kali XFCE desktop

## Automated checks

- Python source compilation: passed.
- Automated suite: **26 passed, 1 skipped, 3 expected failures**.
- Skipped: libwnck tracker integration (PyGObject/libwnck unavailable in build container).
- Expected failures: gesture reversal step semantics and two legacy state-machine threshold/timeout expectations. These remain visible acceptance items.
- CLI version, feature listing and JSON status smoke tests: passed.
- GUI module import without GTK runtime: passed; launching GUI correctly reports missing GTK3/libwnck dependencies in this container.
- Python wheel build: passed (`kali_ux-0.3.0a1-py3-none-any.whl`).
- No live GTK interface rendering or desktop interaction was possible here.

## Not verified

No live X11/XFCE session, GTK window rendering, real touchpad, multi-monitor layout, xfwm4 geometry, clipboard manager, notification daemon or compositor was available. Do not interpret automated tests as live desktop acceptance.
