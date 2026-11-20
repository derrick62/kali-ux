"""Quick actions that delegate to existing XFCE settings applications."""

from kali_ux.platform.commands import start_command

ACTIONS = {
    "display": ["xfce4-display-settings"],
    "sound": ["pavucontrol"],
    "network": ["nm-connection-editor"],
    "power": ["xfce4-power-manager-settings"],
    "keyboard": ["xfce4-keyboard-settings"],
}


def open_action(name: str) -> bool:
    """Launch a settings application without blocking the GTK main loop."""
    argv = ACTIONS.get(name)
    if not argv:
        return False
    result = start_command(argv)
    return result.started
