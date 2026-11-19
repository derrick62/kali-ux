"""Snap presets using wmctrl geometry requests; xfwm4 remains authoritative."""
from __future__ import annotations
from kali_ux.platform.commands import run_command

PRESETS = {'left':(0,0,0.5,1),'right':(0.5,0,0.5,1),'top':(0,0,1,0.5),'bottom':(0,0.5,1,0.5),
           'top-left':(0,0,0.5,0.5),'top-right':(0.5,0,0.5,0.5),'bottom-left':(0,0.5,0.5,0.5),'bottom-right':(0.5,0.5,0.5,0.5)}
class SnapService:
    def __init__(self): self.available = False
    def snap_active(self, preset: str, screen_width: int, screen_height: int, x: int=0, y: int=0) -> bool:
        if preset not in PRESETS or screen_width <= 0 or screen_height <= 0: return False
        fx,fy,fw,fh = PRESETS[preset]; gx=x+round(fx*screen_width); gy=y+round(fy*screen_height)
        gw=round(fw*screen_width); gh=round(fh*screen_height)
        # Remove maximization before setting geometry; wmctrl targets the active window.
        run_command(['wmctrl','-r',':ACTIVE:','-b','remove,maximized_vert,maximized_horz'])
        result=run_command(['wmctrl','-r',':ACTIVE:','-e',f'0,{gx},{gy},{gw},{gh}'])
        return result.available and result.returncode == 0
