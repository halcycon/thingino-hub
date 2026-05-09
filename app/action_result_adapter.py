from typing import Any


def pairing_outcome(camera_id: str, result: dict[str, Any]) -> dict[str, Any]:
    status = str(result.get("status") or "success").strip().lower()
    if status == "warning":
        return {
            "message": f"Pairing install was published for {camera_id}, but the camera did not confirm before the timeout.",
            "category": "warning",
            "reload": False,
            "http_status": 200,
            "ok": True,
            "result": "warning",
        }
    return {
        "message": f"Pairing installed for {camera_id}; native API should come back after the agent restarts.",
        "category": "success",
        "reload": True,
        "http_status": 200,
        "ok": True,
        "result": "success",
    }


def delete_outcome(camera_id: str, result: dict[str, Any]) -> dict[str, Any]:
    if result["retained_cleared"]:
        if result.get("command_published"):
            return {
                "message": (
                    f"Removed {camera_id} from the roster, asked the camera to revoke registration, "
                    "and cleared its retained registration."
                ),
                "category": "success",
                "http_status": 200,
                "ok": True,
                "result": "success",
            }
        return {
            "message": f"Removed {camera_id} from the roster and cleared its retained registration.",
            "category": "success",
            "http_status": 200,
            "ok": True,
            "result": "success",
        }

    detail = result["retained_error"] or "camera may reappear if it republishes registration"
    if result["config_removed"]:
        return {
            "message": (
                f"Removed {camera_id} from saved config and current roster; retained unregister did not complete: {detail}"
            ),
            "category": "error",
            "http_status": 500,
            "ok": False,
            "result": "error",
        }

    return {
        "message": f"Removed {camera_id} from the current roster only; retained unregister did not complete: {detail}",
        "category": "error",
        "http_status": 500,
        "ok": False,
        "result": "error",
    }
