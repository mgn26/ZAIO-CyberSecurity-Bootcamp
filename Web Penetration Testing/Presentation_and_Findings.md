# Title

| Field | Detail |
| --- | --- |
| Client name | |
| Engagement type | |
| Your name | |
| Date | |
| Classification | |

# Executive summary

<!-- Three to five bullets in plain English. What was tested, how many findings, the highest severity, the single biggest business risk. No jargon. If your grandmother could not follow it, rewrite it. -->

# Scope and methodology

<!-- What was in scope, what was not, dates, the standard you followed (OWASP WSTG), tools used. -->

# Findings summary

| # | Finding name | Severity | OWASP Top 10 category |
| --- | --- | --- | --- |
| 1 | Cross Site Scripting | | |
| 2 | Open Redirect | | |
| 3 | Cross Site Request Forgery | | |
| 4 | Insecure Direct Object Reference | | |
| 5 | Local File Inclusion | | |
| 6 | Server Side Request Forgery | | |
| 7 | XML External Entity | | |
| 8 | Recon | | |
| 9 | Remote Code Execution | | |
| 10 | SQL Injection, including the blind variant | | |

# Risk overview

<!-- A simple visual, for example a count of findings by severity, or a heat map. One graphic, not five. -->

# Findings

<!-- See the required layout below. -->

## 1. Cross Site Scripting

<!-- Multiple XSS instances across different contexts, including a header based stored XSS and hidden parameters -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 2. Open Redirect

<!-- Two URL parameters that redirect off site -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 3. Cross Site Request Forgery

<!-- An unprotected URL, a removable protection field, and a weakly encoded token -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 4. Insecure Direct Object Reference

<!-- Two IDORs exposing another user's address and order details -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 5. Local File Inclusion

<!-- An endpoint that reads local files, flag at /lfi/flag.txt -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 6. Server Side Request Forgery

<!-- Reach an internal API that should not be exposed -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 7. XML External Entity

<!-- A standard XXE and a blind XXE, flag at /flag.txt -->

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 8. Recon

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 9. Remote Code Execution

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

## 10. SQL Injection, including the blind variant

### Finding title and severity

<!-- For example "Stored XSS via User-Agent header, High". -->

### OWASP Top 10 (2021) mapping

<!-- Use the table in section 6.4. -->

### Affected endpoint

<!-- Full URL, method, parameter. -->

### Screenshot evidence

<!-- Cropped tight to what matters, with a box or arrow on the important part. Do not paste a full desktop screenshot. -->

### Steps to reproduce

<!-- Numbered, short enough that a developer can follow them without asking you a question. -->

### Business impact

<!-- One or two sentences, no jargon. Not "an attacker can execute JavaScript" but "an attacker can take over a shopper's account and place orders using their saved card". -->

### Remediation

<!-- Specific and actionable. Not "sanitise input" but "HTML encode the User-Agent value before rendering it in the admin panel, and set a Content Security Policy that blocks inline scripts". -->

# Attack chain

<!-- How two or more findings combine into something worse than either alone. For example XSS into session theft, or SSRF into internal API exposure. Draw the chain. -->

# Remediation roadmap

<!-- Split into Immediate (0 to 7 days), Short term (30 days), Strategic (90 days). Assign each finding to a bucket. -->

# Conclusion

<!-- Overall security posture in two or three sentences, plus what you recommend for retesting. -->

# References and appendix

<!-- OWASP links, tool versions, anything that did not fit. -->
