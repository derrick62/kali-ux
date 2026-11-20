from kali_ux.features.focus_tools import service as focus_tools
from kali_ux.features.layout_memory import service as layout_memory
from kali_ux.features.snap_assist import service as snap_assist
from kali_ux.platform.commands import CommandResult


def test_focus_mode_preserves_original_value_on_repeated_enable(monkeypatch):
    calls = []
    responses = [CommandResult(True, 0, "false"), CommandResult(True, 0), CommandResult(True, 0)]

    def fake_run(argv):
        calls.append(argv)
        return responses.pop(0)

    monkeypatch.setattr(focus_tools, "run_command", fake_run)
    focus = focus_tools.FocusMode()
    assert focus.enable()
    assert focus.enable()
    assert len(calls) == 2
    assert focus.disable()
    assert calls[-1][-1] == "false"
    assert not focus.active


def test_focus_mode_keeps_recovery_state_if_restore_fails(monkeypatch):
    responses = [CommandResult(True, 0, "false"), CommandResult(True, 0), CommandResult(True, 1)]
    monkeypatch.setattr(focus_tools, "run_command", lambda _argv: responses.pop(0))
    focus = focus_tools.FocusMode()
    assert focus.enable()
    assert not focus.disable()
    assert focus.active
    assert focus._previous == "false"


def test_snap_requires_successful_unmaximize(monkeypatch):
    calls = []
    monkeypatch.setattr(
        snap_assist,
        "run_command",
        lambda argv: calls.append(argv) or CommandResult(True, 1),
    )
    assert not snap_assist.SnapService().snap_active("left", 1920, 1080)
    assert len(calls) == 1


def test_snap_uses_workarea_origin_and_dimensions(monkeypatch):
    calls = []
    monkeypatch.setattr(
        snap_assist,
        "run_command",
        lambda argv: calls.append(argv) or CommandResult(True, 0),
    )
    assert snap_assist.SnapService().snap_active("right", 1000, 800, -1000, 40)
    assert calls[1][-1] == "0,-500,40,500,800"


def test_layout_capture_omits_private_window_titles_and_writes_private_file(monkeypatch, tmp_path):
    output = (
        "0x01234567 0 10 20 800 600 workstation private-title\n"
        "not-an-xid 0 0 0 100 100 workstation ignored\n"
    )
    monkeypatch.setattr(
        layout_memory,
        "run_command",
        lambda _argv: CommandResult(True, 0, output),
    )
    target = tmp_path / "nested" / "layouts.json"
    layouts = layout_memory.LayoutMemory(target)
    assert layouts.capture("Work")
    content = target.read_text()
    assert "private-title" not in content
    assert layouts.names() == ["Work"]
    assert target.stat().st_mode & 0o777 == 0o600


def test_layout_restore_validates_window_ids_and_geometry(monkeypatch, tmp_path):
    target = tmp_path / "layouts.json"
    target.write_text(
        '{"Desk": ['
        '{"id":"0x1234","x":1,"y":2,"width":300,"height":200},'
        '{"id":"rm -rf /","x":0,"y":0,"width":1,"height":1}]}'
    )
    calls = []
    monkeypatch.setattr(
        layout_memory,
        "run_command",
        lambda argv: calls.append(argv) or CommandResult(True, 0),
    )
    assert layout_memory.LayoutMemory(target).restore("Desk") == 1
    assert len(calls) == 1
    assert calls[0][2] == "0x1234"


def test_layout_rejects_empty_and_path_like_names(tmp_path):
    layouts = layout_memory.LayoutMemory(tmp_path / "layouts.json")
    assert not layouts.capture("../outside")
    assert not layouts.capture("  ")
    assert layouts.restore("../outside") == 0
