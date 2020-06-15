from pprint import pprint

def check(cookies_header):

    cookies = []

    for cookie in cookies_header:

        cookie_metadata = {
            "name": cookie.name,
            "value": cookie.value,
            "httponly": False,
            "secure": cookie.secure,
            "samesite": None,
            "samesite_acceptable": True
        }

        # We have to extract __dict__ because httponly is
        # not a "standard" Cookie object morsel
        if "HttpOnly" in cookie.__dict__['_rest']:
            cookie_metadata["httponly"] = True
        if "SameSite" in cookie.__dict__['_rest']:
            cookie_metadata["samesite"] = cookie.__dict__['_rest'].get("SameSite")

        # We're checking if SameSite is literally set to none, not whether
        # the object exists
        if cookie_metadata["samesite"] is not None and cookie_metadata["samesite"].lower() == "none" and not cookie.secure:
            cookie_metadata["samesite_acceptable"] = False

        cookies.append(cookie_metadata)

    return cookies