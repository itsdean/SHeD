acceptable_values = [
    "1",
    "1; mode=block",
    "1; report="
]

def check(headers):

    payload = {
        "present": False,
        "value": None,
        "acceptable": False
    }

    if "X-XSS-Protection" in headers:
        payload["present"] = True

        xss_value = headers.get("X-XSS-Protection")
        payload["value"] = xss_value

        if xss_value.lower() in acceptable_values:
            payload["acceptable"] = True

    return payload