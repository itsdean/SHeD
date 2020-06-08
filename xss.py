acceptable_values = [
    "1",
    "1; mode=block",
    "1; report="
]

def check(headers):
    if "X-XSS-Protection" not in headers:
        print("[!] Has the X-XSS-Protection header: No\n")
        return False

    print("[✔] Has the X-XSS-Protection header: Yes")

    xss_value = headers.get("X-XSS-Protection")
    if xss_value.lower() in acceptable_values:
        print("Value is acceptable: {}".format(xss_value))    

    elif xss_value == "0":
        print("[x] > X-XSS-Protection is set to 0!")

    print("[!] > The X-XSS-Protection header is no longer actively supported by modern browsers. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection for more information.")
     
    print()
    return True