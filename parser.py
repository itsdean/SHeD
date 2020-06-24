import cookies as cookie_checker
import curious
import hsts
import xframe
import xss

import json

class Parser:


    def __init__(self, response, start_time):
        self.response = response
        self.url = response.url

        date = self.response.headers["date"]

        self.results = {
            "shed": {
                "timestamp": str(start_time)
            },
            "request": {
                "url": self.url,
                "method": self.response.request.method,
                "headers": dict(self.response.request.headers)
            },
            "response": {
                "date": date
            }
        }


    def check_headers(self, headers):
        hsts_result = hsts.check(headers)
        xframe_result = xframe.check(headers)
        xss_result = xss.check(headers)
        curious_result = curious.check(headers)

        self.results = {
            **self.results,
            "hsts": hsts_result,
            "xframe": xframe_result,
            "xss": xss_result,
            "curious": curious_result
        }


    def check_cookies(self, cookies):
        cookie_results = cookie_checker.check(cookies)

        self.results = {
            **self.results,
            "cookies": cookie_results
        }


    def check(self):
        self.check_headers(self.response.headers)
        self.check_cookies(self.response.cookies)


    def report(self, filename):
        with open(filename, "w") as report_file:
            json.dump(self.results, report_file)


    def output(self, output_as_json, pretty):
        if output_as_json:
            if pretty:
                print(json.dumps(self.results, indent=4))
            else:
                print(json.dumps(self.results))
        else:
            # hsts
            # print("\u0332".join("HTTP Strict Transport Security"))
            print("\033[4m" + "HTTP Strict Transport Security" + "\033[0m")
            if self.results["hsts"]["present"]:
                print("[✔] Strict-Transport-Security header: present")
                print("[-] > Age: {} seconds ({} days)".format(
                    self.results["hsts"]["age"],
                    self.results["hsts"]["days"]
                ))
                print("[-] > Has includeSubdomains: {}".format(
                    self.results["hsts"]["subdomains"]
                ))
                print("[-] > Has preload: {}".format(
                    self.results["hsts"]["preload"]
                ))
            else:
                print("[x] Strict-Transport-Security header: missing")

            # xframe
            print("\n\033[4m" + "X-Frame-Options" + "\033[0m")
            if self.results["xframe"]["present"]:
                print("[✔] X-Frame-Options header: present")
                print("[-] Value: {}".format(
                    self.results["xframe"]["value"]
                ))
                print("[-] > Acceptable: {}".format(
                    self.results["xframe"]["acceptable"]
                ))
                if not self.results["xframe"]["acceptable"]:
                    print("[!] > Browsers will not honour this header")

            else:
                print("[x] X-Frame-Options header: missing")

            # xss
            print("\n\033[4m" + "X-XSS-Protection" + "\033[0m")
            if self.results["xss"]["present"]:
                print("[✔] X-XSS-Protection header: present")
                print("[-] Value: {}".format(
                    self.results["xss"]["value"]
                ))
                print("[-] > Acceptable: {}".format(
                    self.results["xss"]["acceptable"]
                ))

            else:
                print("[x] X-XSS-Protection header: missing")
            print("[!] Please make your own judgment call separate from this finding - the X-XSS-Protection header is no longer actively supported by modern browsers. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection for more information.")

            # curious
            if len(self.results["curious"]) > 0:
                print("\n\033[4m" + "Curious Headers" + "\033[0m")
                for counter, headers in enumerate(self.results["curious"]):
                    header = headers.popitem()
                    print("[{}] {}: {}".format(
                        "?",
                        header[0],
                        header[1]
                    ))

            # cookies
            print("\n\033[4m" + "Cookies" + "\033[0m")
            if len(self.results["cookies"]) > 0:
                for counter, cookie in enumerate(self.results["cookies"]):
                    print("[!] Cookie: {}".format(cookie["name"].lower()))
                    print("[-] > Value: {}".format(cookie["value"]))
                    print("[-] > HTTPOnly: {}".format(str(cookie["httponly"]).lower()))
                    print("[-] > Secure: {}".format(str(cookie["secure"]).lower()))
                    if cookie["samesite"]:
                        print("[-] > SameSite: \"{}\"".format(cookie["samesite"]))
                        if not cookie["samesite_acceptable"]:
                            print("[x] >>> Warning: \"SameSite=None\" requires the Secure flag to be accepted")
                            print("[x] >>> SameSite will be ignored")
                    else:
                        print("[-] > SameSite: missing")
                    if counter + 1 != len(self.results["cookies"]):
                        print()
            else:
                print("[x] No cookies were returned by the server")