import json

import pytest

from kali_ux.control_center.model import ControlCenterModel


def test_model_reports_implementation_and_runtime_availability_separately(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "kali_ux.control_center.model.detect",
        lambda: {
            "x11": True,
            "gtk3": True,
            "libwnck": True,
            "xfwm4": True,
            "xfce": True,
            "wmctrl": True,
            "gesture_provider": False,
            "compositor": False,
        },
    )
    model = ControlCenterModel(tmp_path / "config.json")
    rows = {row["key"]: row for row in model.rows()}

    assert rows["window_switcher"]["implementation"] == "integrated"
    assert rows["window_switcher"]["available"] is True
    assert rows["gesture_control"]["available"] is False
    assert rows["gesture_control"]["missing_requirements"] == ["gesture provider"]
    assert rows["window_peek"]["state"] == "planned"


def test_model_persists_feature_preferences_atomically(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "kali_ux.control_center.model.detect",
        lambda: {"x11": True, "wmctrl": True},
    )
    config_path = tmp_path / "config.json"
    model = ControlCenterModel(config_path)

    updated = model.set_enabled("layout_memory", True)

    assert updated["enabled"] is True
    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert saved["features"]["layout_memory"]["enabled"] is True
    assert config_path.stat().st_mode & 0o777 == 0o600
    assert not list(tmp_path.glob(".config.json.*"))


def test_model_refuses_to_enable_unavailable_or_planned_features(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "kali_ux.control_center.model.detect",
        lambda: {"x11": True, "gtk3": True, "libwnck": True},
    )
    model = ControlCenterModel(tmp_path / "config.json")

    with pytest.raises(ValueError, match="gesture provider"):
        model.set_enabled("gesture_control", True)
    with pytest.raises(ValueError, match="not implemented"):
        model.set_enabled("window_peek", True)
    with pytest.raises(KeyError):
        model.set_enabled("unknown_feature", True)
    with pytest.raises(TypeError):
        model.set_enabled("window_switcher", 1)


def test_model_always_allows_disabling_a_previously_enabled_feature(tmp_path, monkeypatch):
    monkeypatch.setattr("kali_ux.control_center.model.detect", lambda: {"x11": True})
    model = ControlCenterModel(tmp_path / "config.json")
    model.config["features"]["gesture_control"]["enabled"] = True

    updated = model.set_enabled("gesture_control", False)

    assert updated["enabled"] is False
