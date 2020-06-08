from pprint import pprint

def check(cookies_header):

    print()
    
    cookies = []

    for cookie in cookies_header:

        cookie_metadata = {
            "Name": cookie.name,
            "Value": cookie.value,
            "HTTPOnly": False,
            "Secure": cookie.secure,
            "SameSite": None
        }

        # We have to extract __dict__ because httponly is
        # not a "standard" Cookie object morsel
        if "HttpOnly" in cookie.__dict__['_rest']:
            cookie_metadata["HTTPOnly"] = True
        if "SameSite" in cookie.__dict__['_rest']:
            cookie_metadata["SameSite"] = cookie.__dict__['_rest'].get("SameSite")

        print("[!] Found cookie: {}".format(cookie.name))
        # print("Found cookie: {}={}".format(cookie.name, cookie.value))
        print("[-] > Value: {}".format(cookie.value))
        print("[-] > Has the Secure flag: {}".format(cookie.secure))
        print("[-] > Has the HttpOnly flag: {}".format(cookie_metadata["HTTPOnly"]))
        if cookie_metadata["SameSite"]:
            print("[-] > Has an explicit SameSite value: SameSite={}".format(cookie_metadata["SameSite"]))
            if cookie_metadata["SameSite"] == "None" and not cookie.secure:
                print("[x] > Warning: \"SameSite=None\" requires the Secure flag to be accepted")

        cookies.append(cookie_metadata)
        print()


    return cookies