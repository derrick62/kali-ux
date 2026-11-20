# Kali UX — Development Guide

## 1. Development approach

Work in small, reviewable increments. Understand the requirement before editing code. Explain the responsibility of each component, the reason for its location and its dependencies. Prefer a simple design that solves the current problem over speculative abstractions.

The cycle is:

1. Understand the user-visible requirement.
2. Inspect the existing code and desktop behaviour.
3. Define acceptance criteria and edge cases.
4. Identify platform and security constraints.
5. Design the smallest suitable interface.
6. Implement incrementally.
7. Run focused tests, then the full suite.
8. Perform desktop verification where applicable.
9. Document decisions, results and remaining work.

## 2. Prerequisites

For the foundation package:
- Python 3.10 or newer.
- `venv` and pip.
- Git.
- `pytest` and `ruff` for development.

For future desktop features, install the relevant Kali/Debian system packages (GTK3/PyGObject, libwnck, libinput tools, X11 utilities) through APT. The exact package list must be based on actual imports and platform experiments.

Do not use `sudo pip`. Do not work around Kali's externally managed Python environment by modifying system Python.

## 3. Setup

```bash
git clone https://github.com/derrick62/kali-ux.git
cd kali-ux
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The repository remote in the supplied checkout is `https://github.com/derrick62/kali-ux.git`. If you use a fork, replace the clone URL with your fork's address.

## 4. Useful commands

```bash
pytest
pytest -q
pytest --cov=kali_ux --cov-report=term-missing
ruff check .
ruff format --check .
python -m kali_ux --version
```

## 5. Repository conventions

- Use the `src/` layout.
- Keep tests under `tests/`, mirroring package responsibilities.
- Use descriptive names and small modules with one clear responsibility.
- Keep platform-specific imports inside platform adapters.
- Keep pure domain logic independent of GTK and X11.
- Use dependency injection or small protocols where they make tests easier.
- Avoid circular imports and feature-to-feature private imports.
- Avoid global mutable state.
- Use structured, privacy-safe logging.
- Keep user-facing configuration documented and validated.

## 6. Python conventions

- Add type annotations to public interfaces.
- Use dataclasses/enums for stable domain concepts where appropriate.
- Prefer pathlib and argument arrays for process invocation.
- Catch narrow exceptions and preserve useful diagnostic context.
- Do not swallow errors silently.
- Never block the GTK main loop.
- Avoid shell=True unless there is a reviewed, compelling reason.
- Keep external dependencies minimal and justified.

## 7. Git workflow

Use focused branches and commits. A commit should represent one coherent change. Before committing:
- Run relevant tests.
- Run lint/format checks.
- Review the diff.
- Confirm no secrets, local paths or generated artifacts were added.
- Update docs/changelog when behaviour or decisions change.

Suggested commit format:
- `docs: establish Kali UX foundation`
- `feat(gesture): normalize swipe lifecycle events`
- `fix(window-switcher): preserve selection on window close`
- `test(restore): cover previously minimized windows`

## 8. Configuration and user data

Use XDG paths and honor environment variables. Do not write configuration into the source tree. Do not overwrite user configuration on upgrade. Configuration changes should be validated and should not partially apply if invalid.

## 9. Desktop development safety

- Test in a normal user session.
- Do not run GTK applications as root.
- Do not alter XFCE or gesture-service settings without explicit user approval.
- Back up configuration before any user-approved modification.
- Provide a rollback path.
- Do not assume that `libinput debug-events` is a stable application API.
- Clearly explain any permission requirement before asking the user to change group membership or device access.

## 10. Documentation discipline

When behaviour changes, update the product specification and tests. When architecture changes, add/update an ADR. When implementation status changes, record the revision and verification evidence. Keep historical context separate from current verified status.

## 11. Current next task

The first source audit and a focused remediation pass are complete. The current test baseline is recorded in `docs/VERIFICATION_REPORT.md`. The next task is target-machine verification on Kali XFCE/X11: confirm the selected touchpad and permissions, capture real gesture event fixtures, test all six gestures and cancellation, and verify snap geometry, Task View focus/dismissal, clipboard ownership and XFCE notification restoration. Do not enable automatic startup or change other gesture services during these tests.
