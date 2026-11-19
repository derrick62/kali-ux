from kali_ux.cli import main


def test_main_reports_foundation_status(capsys):
    assert main([]) == 0
    assert "desktop features are not yet wired" in capsys.readouterr().out
