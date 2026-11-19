"""Reversible XFCE focus-mode helper; does not kill notifications or processes."""
from kali_ux.platform.commands import run_command
class FocusMode:
    def __init__(self): self._previous=None; self.active=False
    def enable(self)->bool:
        r=run_command(['xfconf-query','-c','xfce4-notifyd','-p','/do-not-disturb'])
        if not r.available or r.returncode!=0:return False
        self._previous=r.stdout.strip(); w=run_command(['xfconf-query','-c','xfce4-notifyd','-p','/do-not-disturb','-n','-t','bool','-s','true'])
        self.active=w.available and w.returncode==0;return self.active
    def disable(self)->bool:
        if self._previous is None:return False
        val=self._previous.lower() in ('true','1','yes')
        r=run_command(['xfconf-query','-c','xfce4-notifyd','-p','/do-not-disturb','-n','-t','bool','-s',str(val).lower()])
        self.active=False;self._previous=None;return r.available and r.returncode==0
