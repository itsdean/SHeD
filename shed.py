#!/usr/bin/env python3

# Security HEaDer and cookie checker.
# - developed (but more like wrapped) by itsdean
# - contact: hey@dean.dev

import argparse
import datetime
import requests
import sys

import cookies
import curious
import hsts
import xframe
import xss

from parser import Parser


def request(
        url,
        # port=80,
        headers,
        method="GET"
    ):

    converted_headers = {}

    # get headers passed via cli and save them in a dict
    if headers is not None:
        all_headers = headers.pop()
        # get each individual header from the command line argument, separated by pipes
        for header in all_headers.split("|"):
            # print(header)
            options = header.split(":", 1)
            converted_headers[options[0].strip()] = options[1].strip()

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
    report = pretty = json =  False
    start_time = datetime.datetime.now().isoformat()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="The URL to be checked"
    )

    parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="Headers to add to the request"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Return output in JSON format to stdout"
    )

    parser.add_argument(
        "--output",
        help="File to save output to (in JSON format)"
    )

    if "--pretty" in sys.argv:
        parser.add_argument(
            "--pretty",
            action="store_true",
            help="Prettifies the JSON output"
        )

    args = parser.parse_args()
    url = args.url
    headers = args.header
    json = args.json
    if args.output:
        output_filename = args.output
        report = True
    if "--pretty" in sys.argv:
        pretty = True

    if not json:
        print()
        print("\033[1m\033[4mSHeD.py\033[0m - \033[1mgithub.com/itsdean\033[0m\n")
        print("\033[1m\033[4m" + "URL: {}".format(url) + "\033[0m")
        print("[-] Sending request")
    response, err = request(url, headers=headers)

    if not err:
        if not json:
            print("[✔] > Request successful\n")
        parser = Parser(response, start_time)
        results = parser.check()
        parser.output(json, pretty)
        if report:
            parser.report(output_filename)
    else:
        if "Connection refused" in str(err):
            print("[request] shed can't hit the endpoint.")
        print("[main] exception thrown, error below:\n")
        print(str(err))
        # raise err

    if not json:
        print("\n---\nAll done!\n---\n")
