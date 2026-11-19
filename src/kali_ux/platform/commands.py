"""Safe wrappers for optional desktop commands; never invoke a shell."""
from __future__ import annotations
import shutil, subprocess
from dataclasses import dataclass

@dataclass(frozen=True)
class CommandResult:
    available: bool
    returncode: int | None = None
    stdout: str = ''
    stderr: str = ''

def run_command(argv: list[str], timeout: float = 3.0) -> CommandResult:
    if not argv or not shutil.which(argv[0]): return CommandResult(False, stderr=f'{argv[0] if argv else "command"} not found')
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
        return CommandResult(True, p.returncode, p.stdout, p.stderr)
    except (OSError, subprocess.TimeoutExpired) as exc: return CommandResult(True, None, stderr=str(exc))
