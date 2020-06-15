#  SHeD

Security Header and Cookie Detector.

##  Usage


```
$ python3 shed.py -u https://dean.dev

SHeD.py
---

[!] URL: https://dean.dev
[-] > Sending request
[✔] > Request successful

[x] Has the Strict-Transport-Security header: no

[!] Has the X-Frame-Options header: no

[!] Has the X-XSS-Protection header: No

[?] Found peculiar header: Server=cloudflare

[!] Found cookie: __cfduid
[-] > Value: d8570039f8e891e7f28c13045654bba161591622381
[-] > Has the Secure flag: True
[-] > Has the HttpOnly flag: True
[-] > Has an explicit SameSite value: SameSite=Lax

---
All done!
---
```
