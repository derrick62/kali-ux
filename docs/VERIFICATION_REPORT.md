# Verification report

**Build:** Kali UX 0.3.0-alpha.3
**Environment:** Linux build container (Python 3.13.5); no live Kali XFCE desktop

## Automated checks

- Python source compilation: passed (`python3 -m compileall -q src tests`).
- Automated suite: **41 passed, 1 skipped, 0 expected failures**.
- Skipped: libwnck tracker integration because PyGObject/libwnck is unavailable in this build container.
- GTK namespace regression test: passed; the loader requests GTK 3, GDK 3, libwnck 3 and Pango 1.0 before importing GI namespaces.
- Gesture tests cover routing, reversal, cancellation, finger-count changes, interrupted begins and timeout cancellation.
- Service tests cover detached process launching, focus-mode recovery, snap request sequencing, layout snapshot privacy/permissions and window-ID validation.
- CLI version, feature listing and JSON status smoke tests: passed.
- GUI module import without GTK runtime: passed; actual GUI launch requires distribution-provided GTK3/PyGObject/libwnck.
- Ruff lint and formatting: run separately when Ruff is available; this environment did not have the Ruff executable at review time.
- Python wheel build and isolated target install: passed; installed CLI version smoke test passed. Wheel: `kali_ux-0.3.0a3-py3-none-any.whl`, SHA-256 `1c15d69757251c77679e0f83f5f217ac0d36835b0953f9609f06afd6306d8d29`.

## Not verified

No live X11/XFCE session, GTK interface rendering, real touchpad, multi-monitor layout, xfwm4 geometry, clipboard manager, notification daemon or compositor was available. No Debian package install/upgrade/remove cycle or signed APT repository was tested. Do not interpret automated checks as live desktop acceptance.
