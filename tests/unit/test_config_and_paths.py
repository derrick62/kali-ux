from kali_ux.core.config import DEFAULTS, load_config
from kali_ux.features.launcher.service import ApplicationLauncher

def test_default_config_is_isolated_copy():
    a=load_config(); b=load_config(); a['features']['launcher']['enabled']=True
    assert b['features']['launcher']['enabled'] is False

def test_launcher_search_is_safe_for_empty_query():
    launcher=ApplicationLauncher()
    assert isinstance(launcher.search(''),list)
