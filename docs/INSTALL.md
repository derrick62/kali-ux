# Install and run the Kali UX prototype

These commands target Kali Linux with XFCE on X11. Run them from a terminal in the extracted `kali-ux` project directory. Do not run the Python application with `sudo`.

## Install system dependencies

```bash
sudo apt update
sudo apt install -y \
  python3 python3-venv python3-pip python3-gi \
  gir1.2-gtk-3.0 gir1.2-wnck-3.0 libwnck-3-0 \
  libinput-tools wmctrl xclip xfconf libglib2.0-bin \
  pavucontrol network-manager-gnome xfce4-power-manager
```

Some packages may already be installed. The optional XFCE settings applications are used by Quick Settings; if a package is unavailable in your Kali release, omit it and that shortcut will report that the application is missing.

## Create the Python environment

Use system-site-packages so the virtual environment can see the GTK bindings installed by apt:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Do not use `sudo pip`. Keep the Control Center running as your normal desktop user.

## Initialize and launch

```bash
kali-ux init
kali-ux status
kali-ux features
kali-ux gui
```

To start the existing gesture-driven SwipeSwitch listener explicitly:

```bash
kali-ux swipeswitch
```

SwipeSwitch requires an X11 session and access to its selected `/dev/input/eventX` device. If it reports a permission problem, do not blindly change device permissions or add broad input-group access. First inspect `libinput list-devices`, confirm the correct touchpad, and review the security implications. Gesture input is not started by the Control Center or at login automatically.

## Verify the checkout

```bash
./scripts/check.sh
```

The alpha.3 build-container report records 41 passed and 1 skipped, with no expected failures. The skipped libwnck integration and all desktop behaviours still need validation on the target Kali XFCE session. A passing unit suite does not replace manual desktop testing.
