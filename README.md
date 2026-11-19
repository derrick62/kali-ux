# Kali UX

**A modular desktop-experience enhancement suite for Kali Linux, beginning with XFCE/X11.**

Kali UX is a project to make everyday desktop interaction on Kali Linux more fluid, discoverable and cohesive. It takes inspiration from useful desktop interactions found in Windows—window switching, task overview, snapping, quick controls and productivity tools—while respecting Linux desktop conventions and existing system components.

> **Project status:** Foundation and product-definition stage. This repository scaffold does not mean the planned desktop features are implemented. SwipeSwitch is an existing, separately developed project and is the first integration candidate.

## Initial target

| Area | Initial baseline |
|---|---|
| Distribution | Kali Linux |
| Desktop | XFCE |
| Window manager | `xfwm4` |
| Display server | X11 |
| Language | Python 3 |
| UI toolkit | GTK 3 / PyGObject, initially |
| Window integration | X11/EWMH; evaluate `libwnck` for window/workspace operations |
| Packaging direction | Debian packages, eventually an APT repository |

The initial scope is intentionally narrow. Wayland and other desktop environments are future compatibility targets, not current promises. Kali's desktop/display-server choices differ by desktop environment; this project specifically targets the XFCE/X11 session first.

## Product principles

- Work with the desktop environment; do not replace `xfwm4`.
- Prefer existing desktop capabilities and standards over custom reinvention.
- Keep features modular, independently configurable and testable.
- Keep the core small. Do not introduce services, abstractions or dependencies without a concrete need.
- Make system-level effects explicit and reversible.
- Treat privacy and least privilege as product requirements.
- Distinguish implemented, tested, manually verified and merely planned functionality.

## Feature vision

The longer-term suite may include:

- SwipeSwitch: gesture-driven window switching, Show Desktop/restoration and Task View.
- Snap Assist: discoverable window layouts and snapping assistance.
- Window Overview: an overview of eligible open windows.
- Shared Gesture Control: one arbitration point for gesture ownership.
- Clipboard History: searchable, bounded and privacy-aware history.
- Quick Panel: selected desktop controls in one focused surface.
- Focus Tools: distraction-reduction utilities.
- Application Launcher: improved application discovery and launching.
- Window Peek and Layout Memory.
- Control Center and Diagnostics.

See [FEATURES.md](docs/FEATURES.md) for scope and status.

## Repository status

This is the initial foundation scaffold. The first engineering activity after reviewing these documents is the SwipeSwitch audit—not implementing every feature.

The existing SwipeSwitch repository is:
<https://github.com/derrick62/swipeswitch>

The current project archive and prior development notes should be inspected as part of that audit. No claim is made here that the remote repository has been cloned, that the current working tree is identical to an earlier archive, or that all recent gesture changes are verified.

## Quick start for contributors

The foundation package is deliberately lightweight and does not import GTK or connect to X11 merely to display its version.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
ruff check .
python -m kali_ux --version
```

GTK/PyGObject, libwnck and X11 integration dependencies are expected to be installed through Kali/Debian packages when a feature actually needs them. Do not install system GTK bindings into Kali's externally managed Python environment with `sudo pip`.

## Documentation map

- [Product specification](docs/PRODUCT_SPECIFICATION.md) — vision, boundaries and product requirements.
- [Roadmap](docs/ROADMAP.md) — staged delivery and exit criteria.
- [Architecture](docs/ARCHITECTURE.md) — component boundaries and platform strategy.
- [Feature inventory](docs/FEATURES.md) — requirements, priorities and status.
- [Design principles](docs/DESIGN_PRINCIPLES.md) — interaction and visual language.
- [Testing strategy](docs/TESTING.md) — test levels and acceptance evidence.
- [Development guide](docs/DEVELOPMENT.md) — local workflow and contribution practices.
- [Research notes](docs/RESEARCH.md) — evidence, assumptions and open questions.
- [Security and privacy](docs/SECURITY_AND_PRIVACY.md) — permissions, data handling and threat considerations.
- [Packaging guide](docs/PACKAGING.md) — Debian packaging direction.
- [SwipeSwitch preliminary audit](docs/SWIPESWITCH_AUDIT_PRELIMINARY.md) — findings from the available 0.2.0 archive.
- [Architecture decisions](docs/decisions/) — recorded decisions and unresolved choices.

## Important project language

**Planned** means described in the product scope. **Implemented** means code exists. **Automated-tested** means relevant automated tests pass. **Manually verified** means the behaviour was exercised on a real target desktop and the result recorded. These labels are not interchangeable.

## License

The repository scaffold is marked MIT in `LICENSE`. Before public distribution, review the licensing of all reused code, dependencies, icons, artwork and any incorporated SwipeSwitch code. A parent project's license does not automatically relicense third-party assets or dependencies.
