"""Quick actions that delegate to existing XFCE settings tools."""
from kali_ux.platform.commands import run_command
ACTIONS={'display':['xfce4-display-settings'],'sound':['pavucontrol'],'network':['nm-connection-editor'],'power':['xfce4-power-manager-settings'],'keyboard':['xfce4-keyboard-settings']}
def open_action(name:str)->bool:
    argv=ACTIONS.get(name)
    if not argv:return False
    r=run_command(argv,timeout=2)
    return r.available and r.returncode==0
