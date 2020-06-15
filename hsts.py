import re

hsts_pattern = r"max-age=(?P<age>\d+)(?:;\W(?:(?P<subdomains>includeSubDomains)|(?P<preload>preload))+)*"

def check(headers):

    payload = {
        "present": False,
        "age": 0,
        "days": 0,
        "preload": False,
        "subdomains": False
    }

    if "Strict-Transport-Security" in headers:
        payload["present"] = True

        hsts_value = headers.get("Strict-Transport-Security")
        hsts_pattern_object = re.compile(hsts_pattern)

        matches = hsts_pattern_object.search(hsts_value)
        matches_dict = matches.groupdict()

        seconds = int(matches_dict["age"])
        payload["age"] = seconds
        days = int(int(seconds) / 60 / 60 / 24)
        payload["days"] = days

        if matches_dict["subdomains"]:
            payload["subdomains"] = True

        if matches_dict["preload"]:
            payload["preload"] = True

    # print()
    return payload