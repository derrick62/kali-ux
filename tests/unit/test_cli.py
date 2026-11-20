from kali_ux.cli import main


def test_main_reports_platform_status(capsys):
    assert main(["status"]) == 0
    assert "platform" in capsys.readouterr().out


def test_features_command(capsys):
    assert main(["features"]) == 0
    assert "SwipeSwitch" in capsys.readouterr().out
