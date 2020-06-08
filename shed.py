#!/usr/bin/env python3

# Security HEaDer and cookie checker.
# - developed (but more like wrapped) by itsdean
# - contact: hey@dean.dev

import argparse
import requests

import cookies
import curious
import hsts
import xframe
import xss

from pprint import pprint


def request(
        url,
        # port=80,
        headers=[],
        method="GET"
    ):

    converted_headers = {}

    # convert the header arguments from x=y to {x: "y"}
    for header in headers:
        options = header.split("=", 1)
        converted_headers[options[0]] = options[1]

    try:
        if method == "GET":
            response = requests.head(
                url,
                headers = converted_headers
            )
            return response, None

    except requests.exceptions.ConnectionError as err:
        return None, err
    except Exception as err:
        return None, err    


def check_headers(response_headers):

    # for header in response_headers:

    #     pprint(header + ": " + response_headers.get(header))

    hsts_result = hsts.check(response_headers)
    xframe_result = xframe.check(response_headers)
    xss_result = xss.check(response_headers)

    curious.check(response_headers)


def check_cookies(response_cookies):
    cookies.check(response_cookies)


def check(response):
    check_headers(response.headers)
    check_cookies(response.cookies)


if __name__ == "__main__":
    print()
    print("SHeD.py\n---\n")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="The URL to be checked"
    )

    parser.add_argument(
        "--header",
        default="",
        action="append",
        help="Headers to add to the request"
    )

    args = parser.parse_args()
    url = args.url
    headers = args.header

    print("[!] URL: {}".format(url))
    print("[-] > Sending request")
    response, err = request(url, headers=headers)

    if not err:
        print("[✔] > Request successful\n")
        check(response)
        # report()
    else:
        if "Connection refused" in str(err):
            print("[request] shed can't hit the endpoint.")
        print("[main] exception thrown, error below:\n")
        print(str(err) + "\n")
        # raise err
    
    # print("[main] exiting\n---\n")
    print("---\nAll done!\n---\n")
