acceptable_values = [
    "deny",
    "sameorigin"
]

def check(headers):
    if "X-Frame-Options" not in headers:
        print("[x] Has the X-Frame-Options header: no\n")
        return False

    print("[✔] Has the X-Frame-Options header: yes")

    xframe_value = headers.get("X-Frame-Options")
    if xframe_value.lower() in acceptable_values:
        print("[✔] > Value is acceptable: {}".format(xframe_value))
    else:
        print("[?] > Unknown X-Frame-Options value: {}".format(xframe_value))
        print("[!] > Browsers will not honour this value")

    print()
    return True