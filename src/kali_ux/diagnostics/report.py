"""Read-only diagnostic report; excludes environment values and user data."""

from kali_ux.control_center.model import ControlCenterModel
from kali_ux.core.registry import FEATURES
from kali_ux.platform.capabilities import detect


def build_report() -> dict:
    platform = detect()
    try:
        model = ControlCenterModel()
        features = model.rows()
        config_error = None
    except (OSError, ValueError) as exc:
        # Keep diagnostics usable when a user's config is malformed. Do not
        # overwrite or silently repair it; report the issue for manual recovery.
        features = [
            {
                "key": feature.key,
                "title": feature.title,
                "implementation": feature.status,
                "requirements": list(feature.requires),
                "state": "configuration unavailable",
            }
            for feature in FEATURES
        ]
        config_error = str(exc)

    report = {
        "platform": platform,
        "features": features,
        "notes": [
            "No system settings were changed.",
            "Feature preferences do not start background services.",
            "Gesture input is not started automatically.",
            "Window capture backend is not implemented.",
        ],
    }
    if config_error:
        report["configuration_error"] = config_error
    return report
