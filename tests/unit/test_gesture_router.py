from kali_ux.features.gesture_control.router import GestureRouter
from kali_ux.features.window_switcher.engine.events import GestureEvent
from kali_ux.features.window_switcher.engine.gestures import GestureRecognizer


def _router(*, threshold=20, step=40):
    router = GestureRouter(GestureRecognizer(threshold_px=threshold, step_px=step))
    return router


def test_lifecycle_router_requires_explicit_enable():
    router = _router()
    seen = []
    router.register_action_handler("switch_begin", seen.append, owner="window_switcher")

    assert router.handle_event(GestureEvent("begin", 3)) == []
    assert router.handle_event(GestureEvent("update", 3, dx=-50)) == []
    assert seen == []


def test_router_sends_complete_switch_lifecycle_to_one_owner():
    router = _router()
    seen = []
    for name in ("switch_begin", "switch_move", "switch_commit", "switch_cancel"):
        router.register_action_handler(name, seen.append, owner="window_switcher")
    router.enabled = True

    router.handle_event(GestureEvent("begin", 3))
    router.handle_event(GestureEvent("update", 3, dx=-90))
    router.handle_event(GestureEvent("end", 3))

    assert [action.name for action in seen] == [
        "switch_begin",
        "switch_move",
        "switch_commit",
    ]
    assert router.active_owner is None


def test_active_gesture_cannot_be_taken_over_by_another_feature():
    router = _router()
    switcher_actions = []
    other_actions = []
    router.register_action_handler(
        "switch_begin", switcher_actions.append, owner="window_switcher"
    )
    router.register_action_handler("switch_move", other_actions.append, owner="other_feature")
    router.register_action_handler("switch_commit", other_actions.append, owner="other_feature")
    router.enabled = True

    router.handle_event(GestureEvent("begin", 3))
    router.handle_event(GestureEvent("update", 3, dx=-90))
    assert router.active_owner == "window_switcher"
    router.handle_event(GestureEvent("end", 3))

    assert [action.name for action in switcher_actions] == ["switch_begin"]
    assert other_actions == []
    assert router.active_owner is None


def test_timeout_cancellation_reaches_owner_and_releases_it():
    router = _router()
    seen = []
    router.register_action_handler("switch_begin", seen.append, owner="window_switcher")
    router.register_action_handler("switch_cancel", seen.append, owner="window_switcher")
    router.enabled = True

    router.handle_event(GestureEvent("begin", 3))
    router.handle_event(GestureEvent("update", 3, dx=-50))
    router._recognizer.last_activity -= 10
    actions = router.check_timeout(1)

    assert [action.name for action in actions] == ["switch_cancel"]
    assert [action.name for action in seen] == ["switch_begin", "switch_cancel"]
    assert router.active_owner is None


def test_disabling_router_resets_recognizer_and_owner():
    router = _router()
    seen = []
    router.register_action_handler("switch_begin", seen.append, owner="window_switcher")
    router.enabled = True
    router.handle_event(GestureEvent("begin", 3))
    router.handle_event(GestureEvent("update", 3, dx=-50))

    router.enabled = False

    assert router.active_owner is None
    assert router.handle_event(GestureEvent("end", 3)) == []
