import re

hsts_pattern = r"max-age=(?P<age>\d+)(?:;\W(?:(?P<subdomains>includeSubDomains)|(?P<preload>preload))+)*"

def check(headers):
    if "Strict-Transport-Security" not in headers:
        print("[x] Has the Strict-Transport-Security header: no\n")
        return False

    print("[✔] Has the Strict-Transport-Security header: yes")

    hsts_value = headers.get("Strict-Transport-Security")
    hsts_pattern_object = re.compile(hsts_pattern)

    matches = hsts_pattern_object.search(hsts_value)
    matches_dict = matches.groupdict()

    seconds = matches_dict["age"]
    days = int(int(seconds) / 60 / 60 / 24)
    print("[-] > Age: {} seconds ({} days)".format(seconds, days))

    if matches_dict["subdomains"]:
        print("[-] > includeSubDomains: yes")

    if matches_dict["preload"]:
        print("[-] > Preload: yes")


    # if xframe_value.lower() in acceptable_values:
    #     print("[✔] Value is acceptable: {}".format(xframe_value))
    # else:
    #     print("[?] Unknown X-Frame-Options value: {}".format(xframe_value))
    #     print("[!] > Browsers will not honour this value")

    print()
    return True