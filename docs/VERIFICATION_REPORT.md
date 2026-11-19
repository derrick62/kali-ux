# Verification report

**Build:** Kali UX 0.2.0-alpha.1  
**Environment:** Linux build container; not a live Kali XFCE desktop

## Automated checks

- Python compilation: passed.
- Core unit/service tests: 7 passed.
- SwipeSwitch parser/recognizer/state tests: 19 passed, 3 expected failures retained as explicit acceptance tests, 1 tracker integration module skipped because PyGObject/libwnck are unavailable in this container.
- CLI version, feature listing and JSON status smoke tests: passed.
- ZIP integrity: verified after archive creation.

The three expected failures are not silently treated as resolved:

- Horizontal reversal currently reports two rightward steps where the test expects one; define whether movement is cumulative net displacement or incremental correction.
- The legacy state-machine test expects a 30px swipe to show the overlay while the configured threshold is 35px.
- Its timeout test consequently expects an overlay hide that was never shown.

These should be resolved through a deliberate product decision and implementation change, not by weakening the acceptance criteria.

## Not verified

No live Kali XFCE/X11 session, GTK3/libwnck runtime, real touchpad, multi-monitor setup, compositor, xfwm4 snapping, clipboard selection monitoring, or notification daemon was available. No production input listener was automatically started. This archive is an integrated alpha baseline, not a production-ready installer or release.
