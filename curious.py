CURIOUS_HEADERS = [
    "X-Hacker",
    "X-Powered-By",
    "Server"
]


def check(headers):
    payload = []

    for header in CURIOUS_HEADERS:
        if header.lower() in headers:
            payload.append(
                {
                    header: headers.get(header)
                }
            )

    return payload