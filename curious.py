CURIOUS_HEADERS = [
    "X-Powered-By",
    "Server"
]

def check(headers):
    for header in CURIOUS_HEADERS:
        if header.lower() in headers:
            print("[?] Found peculiar header: {}={}".format(header, headers.get(header)))