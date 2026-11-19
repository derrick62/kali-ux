from kali_ux.features.clipboard_history.service import ClipboardHistory
from kali_ux.features.gesture_control.router import Gesture, GestureRouter
from kali_ux.features.snap_assist.service import PRESETS

def test_clipboard_history_deduplicates_and_bounds():
    h=ClipboardHistory(max_items=2)
    assert h.add('one') and h.add('two') and h.add('three')
    assert [x.text for x in h.search()] == ['three','two']
    assert not h.add('three')
    assert not h.add('secret',sensitive=True)
    h.clear(); assert h.search()==[]

def test_gesture_router_requires_explicit_enable():
    r=GestureRouter(); seen=[]; r.register(3,'left',seen.append)
    assert not r.dispatch(Gesture(3,'left')) and not seen
    r.enabled=True
    assert r.dispatch(Gesture(3,'left')) and len(seen)==1

def test_snap_presets_are_normalized():
    assert len(PRESETS)==8
    assert all(0 <= x <= 1 for p in PRESETS.values() for x in p)
