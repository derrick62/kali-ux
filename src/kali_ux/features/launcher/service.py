"""XDG desktop-entry discovery and safe application launching."""
from __future__ import annotations
import os, subprocess
from pathlib import Path
from dataclasses import dataclass
@dataclass(frozen=True)
class AppEntry: name:str; command:str; path:str
class ApplicationLauncher:
    def __init__(self): self.entries=self._scan()
    def _scan(self):
        out=[]
        for root in (Path('/usr/share/applications'),Path.home()/'.local/share/applications'):
            if root.exists():
                for p in root.rglob('*.desktop'):
                    try:
                        lines=p.read_text(errors='ignore').splitlines(); name=next((x.split('=',1)[1] for x in lines if x.startswith('Name=')),None); cmd=next((x.split('=',1)[1] for x in lines if x.startswith('Exec=')),None)
                        if name and cmd and 'NoDisplay=true' not in lines: out.append(AppEntry(name,cmd,str(p)))
                    except OSError: pass
        return out
    def search(self,q:str): return sorted((e for e in self.entries if q.casefold() in e.name.casefold()),key=lambda e:e.name.casefold())[:30]
    def launch(self,entry:AppEntry)->bool:
        # Desktop Exec has field codes and quoting semantics; delegate parsing to gio where possible.
        p=subprocess.Popen(['gio','launch',entry.path],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True) if os.path.exists('/usr/bin/gio') else None
        return p is not None
