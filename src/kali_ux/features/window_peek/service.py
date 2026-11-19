"""Window preview capability probe. Pixel capture is deliberately not faked."""
from kali_ux.platform.capabilities import detect
class WindowPeek:
    def capability(self)->tuple[bool,str]:
        c=detect()
        if not c['x11']:return False,'Window capture currently requires an X11 session.'
        return False,'A compositor-aware capture backend has not yet been implemented; showing window metadata is available through Task View.'
