#  SHeD

Security Header and Cookie Detector.

##  Usage


```
$ python3 SHeD.py -u https://dean.dev

SHeD.py - github.com/itsdean

URL: https://dean.dev
[-] Sending request
[✔] > Request successful

HTTP Strict Transport Security
[x] Strict-Transport-Security header: missing

X-Frame-Options
[x] X-Frame-Options header: missing

X-XSS-Protection
[x] X-XSS-Protection header: missing
[!] Please make your own judgment call separate from this finding - the X-XSS-Protection header is no longer
actively supported by modern browsers. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
for more information.

Curious Headers
[?] Server: cloudflare

Cookies
[!] Cookie: __cfduid
[-] > Value: d986453e86efb5cb4a3536050cd6342381592375675
[-] > HTTPOnly: true
[-] > Secure: true
[-] > SameSite: "Lax"

---
All done!
---
```
