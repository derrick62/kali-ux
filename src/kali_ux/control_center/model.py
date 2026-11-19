"""Control Center data model. UI front-end is optional GTK3 integration."""
from kali_ux.core.config import load_config,write_default_config
from kali_ux.core.registry import FEATURES
class ControlCenterModel:
    def __init__(self): self.config=load_config()
    def rows(self):
        return [{'key':f.key,'title':f.title,'description':f.description,'status':f.status,'enabled':bool(self.config['features'].get(f.key,{}).get('enabled',False))} for f in FEATURES]
    def set_enabled(self,key:str,enabled:bool):
        if key not in {f.key for f in FEATURES}: raise KeyError(key)
        self.config['features'].setdefault(key,{})['enabled']=bool(enabled)
        path=write_default_config()
        import json
        path.write_text(json.dumps(self.config,indent=2)+'\n');path.chmod(0o600)
