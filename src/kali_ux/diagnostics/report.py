"""Read-only diagnostic report; excludes environment values and user data."""
from kali_ux.platform.capabilities import detect
from kali_ux.core.registry import FEATURES

def build_report()->dict:
    return {'platform':detect(),'features':[{'key':f.key,'title':f.title,'status':f.status,'requirements':list(f.requires)} for f in FEATURES],
            'notes':['No system settings were changed.','Gesture input is not started automatically.','Window capture backend is not implemented.']}
