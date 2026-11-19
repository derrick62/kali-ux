"""Explicit, user-triggered window layout snapshots."""
from __future__ import annotations
import json
from pathlib import Path
from kali_ux.core.paths import DATA_HOME
from kali_ux.platform.commands import run_command
class LayoutMemory:
    def __init__(self,path:Path|None=None): self.path=path or DATA_HOME/'layouts.json'
    def capture(self,name:str)->bool:
        if not name.strip(): return False
        r=run_command(['wmctrl','-lG']);
        if not r.available or r.returncode != 0: return False
        rows=[]
        for line in r.stdout.splitlines():
            parts=line.split(None,7)
            if len(parts)>=7:
                try: rows.append({'id':parts[0],'desktop':int(parts[1]),'x':int(parts[2]),'y':int(parts[3]),'width':int(parts[4]),'height':int(parts[5]),'title':parts[7] if len(parts)>7 else ''})
                except ValueError: continue
        data={}
        if self.path.exists():
            try: data=json.loads(self.path.read_text())
            except (OSError,ValueError): data={}
        data[name]=rows; self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps(data,indent=2)); self.path.chmod(0o600); return True
    def names(self)->list[str]:
        try:return sorted(json.loads(self.path.read_text()).keys()) if self.path.exists() else []
        except (OSError,ValueError):return []
    def restore(self,name:str)->int:
        try: rows=json.loads(self.path.read_text()).get(name,[])
        except (OSError,ValueError):return 0
        done=0
        for w in rows:
            r=run_command(['wmctrl','-ir',w['id'],'-e',f"0,{w['x']},{w['y']},{w['width']},{w['height']}"])
            done += int(r.available and r.returncode==0)
        return done
