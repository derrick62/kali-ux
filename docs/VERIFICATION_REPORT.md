# Verification report

**Build:** Kali UX 0.3.0-alpha.4  
**Environment:** Linux build container (Python 3.13); no live Kali XFCE desktop

## Automated checks

- Python source compilation: passed (`PYTHONPATH=src python -m compileall -q src tests`).
- Automated suite: **46 passed, 1 skipped, 0 expected failures**.
- Skipped: libwnck tracker integration because the build container does not provide the required PyGObject/libwnck integration.
- GTK namespace regression test: passed; the loader requests GTK 3, GDK 3, libwnck 3 and Pango 1.0 before importing GI namespaces.
- Control Center model tests: passed for capability-aware availability, planned/unavailable feature rejection, disable behaviour, atomic persistence and private file permissions.
- Configuration validation tests: passed, including rejection of non-boolean feature enabled values.
- CLI version, feature listing and JSON status smoke tests: passed.
- GUI module import without starting GTK: passed. Actual GTK rendering and interaction were not tested in this build container.
- Wheel build: passed; `kali_ux-0.3.0a4-py3-none-any.whl` (SHA-256 `688cd38981b022d068f2c3e1b36717b8a4379f23d0a081c85357c1538b324c7b`); wheel metadata reports version 0.3.0a4.
- Ruff lint and formatting: not run because Ruff is unavailable in this build container.

## Not verified

No live Kali XFCE/X11 session, GTK interface rendering, real touchpad, multi-monitor layout, xfwm4 geometry, clipboard manager, notification daemon or compositor was available. No Debian package install/upgrade/remove cycle or signed APT repository was tested. Do not interpret automated checks as live desktop acceptance.
