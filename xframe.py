acceptable_values = [
    "deny",
    "sameorigin"
]

def check(headers):

    payload = {
        "present": False,
        "value": None,
        "acceptable": False
    }

    if "X-Frame-Options" in headers:
        payload["present"] = True

        xframe_value = headers.get("X-Frame-Options")
        payload["value"] = xframe_value

        if xframe_value.lower() in acceptable_values:
            payload["acceptable"] = True

    return payload