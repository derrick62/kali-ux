"""Kali UX command-line interface."""
from __future__ import annotations
import argparse, json
from kali_ux import __version__
from kali_ux.core.config import write_default_config
from kali_ux.core.paths import CONFIG_HOME
from kali_ux.diagnostics.report import build_report
from kali_ux.core.registry import FEATURES

def build_parser():
 p=argparse.ArgumentParser(prog='kali-ux',description='Kali UX desktop enhancement suite')
 p.add_argument('--version',action='version',version=f'%(prog)s {__version__}')
 sub=p.add_subparsers(dest='command')
 sub.add_parser('status',help='Show platform and feature capability report')
 sub.add_parser('init',help='Create a private default configuration')
 sub.add_parser('features',help='List bundled features')
 sub.add_parser('swipeswitch',help='Start the SwipeSwitch X11/GTK3 interface')
 sub.add_parser('gui',help='Open the Kali UX GTK3 Control Center')
 return p

def main(argv:list[str]|None=None)->int:
 a=build_parser().parse_args(argv)
 if a.command=='init': print(write_default_config()); return 0
 if a.command=='features':
  for f in FEATURES: print(f'{f.key:20} {f.status:12} {f.title}')
  return 0
 if a.command=='swipeswitch':
  from kali_ux.features.window_switcher.engine.__main__ import main as run_switcher
  return run_switcher([])
 if a.command=='gui':
  from kali_ux.ui.app import main as run_gui
  try: return run_gui()
  except RuntimeError as exc: print(exc); return 1
 if a.command=='status' or a.command is None: print(json.dumps(build_report(),indent=2)); return 0
 return 2
