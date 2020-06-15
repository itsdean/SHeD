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

from parser import Parser


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
            response = requests.get(
                url,
                headers = converted_headers
            )
            return response, None

    except requests.exceptions.ConnectionError as err:
        return None, err
    except Exception as err:
        return None, err


if __name__ == "__main__":
    json = False

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

    parser.add_argument(
        "--json",
        action="store_true",
        help="Return output in JSON format to stdout"
    )

    args = parser.parse_args()
    url = args.url
    headers = args.header
    json = args.json

    if not json:
        print()
        print("\033[1m\033[4mSHeD.py\033[0m - \033[1mgithub.com/itsdean\033[0m\n")
        print("\033[1m\033[4m" + "URL: {}".format(url) + "\033[0m")
        print("[-] Sending request")
    response, err = request(url, headers=headers)

    if not err:
        if not json:
            print("[✔] > Request successful\n")
        parser = Parser(response)
        results = parser.check()
        parser.output(json)
    else:
        if "Connection refused" in str(err):
            print("[request] shed can't hit the endpoint.")
        print("[main] exception thrown, error below:\n")
        print(str(err))
        # raise err

    if not json:
        print("\n---\nAll done!\n---\n")
