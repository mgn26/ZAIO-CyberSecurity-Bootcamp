## Executive Summary

<!-- 3–5 sentences. What happened, what you found, what your verdict is, and what you recommend — written so a CISO could read only this section and still know what they need to know. -->

On 23–24 September 2026 the SOC received four related phishing-category alerts against TheTryDaily users. One inbound “HR onboarding” email to j.garcia@thetrydaily.thm looked suspicious at first glance, but there was no firewall evidence that the recipient clicked the link, so that case was closed as a False Positive. A separate Amazon delivery lure to h.harris@thetrydaily.thm was confirmed phishing (True Positive): the user did attempt the shortened bit.ly link, and the firewall blocked it under the “Blocked Websites” rule. A later Microsoft account “unusual sign-in” email to c.allen@thetrydaily.thm used a clear typosquat domain (m1crosoftsupport.co) and is a True Positive, with no evidence the user reached the phishing URL. Recommend deleting/quarantining the malicious messages, coaching the affected users, and keeping URL/domain blocks for the confirmed phishing infrastructure.

## Incident Details

<!-- Date/time of the alert, alert source, affected user(s)/asset(s), classification of the alert type. -->

| Field | Value |
|---------|-------|
| Alert Source | Email / Firewall |
| Alert IDs | 8814, 8815, 8816, 8817 |
| Time of Alerts (UTC) | 09/23/2026 21:21:20.616 – 09/24/2026 00:51:54.978 |
| Affected Users/Assets | j.garcia@thetrydaily.thm; h.harris@thetrydaily.thm; c.allen@thetrydaily.thm; host 10.20.2.17 |
| Alert Type | Phishing / Access to Blacklisted External URL |

### Per-alert breakdown

| Alert ID | Time (UTC) | Source | Affected | Subject / Event |
|---|---|---|---|---|
| 8814 | 09/23/2026 21:21:20.616 | Email | j.garcia@thetrydaily.thm | Action Required: Finalize Your Onboarding Profile |
| 8815 | 09/23/2026 21:24:33.616 | Email | h.harris@thetrydaily.thm | Your Amazon Package Couldn’t Be Delivered – Action Required |
| 8816 | 09/23/2026 21:25:47.616 | Firewall | 10.20.2.17 | Access to Blacklisted External URL Blocked by Firewall |
| 8817 | 09/24/2026 00:51:54.978 | Email | c.allen@thetrydaily.thm | Unusual Sign-In Activity on Your Microsoft Account |

## Investigation Timeline

<!-- A chronological account of your investigation: what you looked at first, what led you to look at the next thing, and why. This should read as a narrative, not a list of screenshots. -->

### Alert 8814 — HR onboarding email (j.garcia)

* The user received an email, without any attachments, with the subject "Action Required: Finalize Your Onboarding Profile" and was required to click on a given link.
* The email structure looks like a typical reminder email, which corresponds with the subject matter. Sender is onboarding@hrconnex.thm and the link points to https://hrconnex.thm/onboarding/15400654060/j.garcia.
* Searched email logs for the recipient (`datasource : "email" and recipient : "j.garcia@thetrydaily.thm"`) to see related mailbox activity around the same window. The onboarding message appears more than once; the rest of the traffic is normal internal mail from the user.
* URL does not seem to lead to a clearly malicious endpoint from the face of the email alone, however this is unconfirmed without external reputation tooling.
* If the recipient never clicked on the link, then this email would pose no active threat to the network, otherwise this could still be a potential phishing attempt.
* To confirm the user's interaction with the URL given in the email we check the logs from the firewall. Attempts to query the exact URL / domain against the firewall datasource did not return usable hits in this investigation (query syntax issues / no matching traffic).
* Even in the case that the URL somehow led to a malicious endpoint we were not aware of, there isn't any evidence or trace that the recipient of the email actually clicked on the link or interacted with the endpoint from within the organization's network.
* Case closed as False Positive on the platform with rationale: no evidence of interaction with the email.

### Alert 8815 / 8816 — Amazon package lure and firewall block (h.harris / 10.20.2.17)

* Next assigned alert was another inbound email with a suspicious external link: subject "Your Amazon Package Couldn’t Be Delivered – Action Required", sender urgents@amazon.biz, recipient h.harris@thetrydaily.thm, no attachments.
* Email content is a classic delivery / incomplete-address lure, with urgency (48 hours) and a shortened link http://bit.ly/3sHkX3da12340. The sender domain amazon.biz does not look like legitimate Amazon mail.
* Confirmed the email event in SIEM with `datasource : email and sender : "urgents@amazon.biz"` (single hit at 21:24:33.616 UTC).
* As the playbook says, we then pivoted to firewall / proxy logs for that URL. Query `datasource : "firewall" AND URL : "http://bit.ly/3sHkX3da12340"` returned one hit.
* About a minute later (21:25:47.616 UTC), internal host 10.20.2.17 attempted web-browsing to that same bit.ly URL (dest IP 67.199.248.11:80). Action was **blocked** by rule "Blocked Websites".
* Broader pivots on the destination IP (`DestinationIP : 67.199.248.11`) and combined URL/IP queries still only show that one blocked attempt — so the click happened, but the control worked and there is no sign of a successful browse-through.
* Alert 8816 is the firewall-side detection of that same click, severity High, confirming the blacklist / threat feed already knew this URL as bad.

### Alert 8817 — Microsoft unusual sign-in lure (c.allen)

* Later alert for inbound email to c.allen@thetrydaily.thm from no-reply@m1crosoftsupport.co, subject "Unusual Sign-In Activity on Your Microsoft Account", no attachments.
* Content claims a sign-in from Lagos, Nigeria (IP 102.89.222.143) and pushes the user to "Review Activity" via https://m1crosoftsupport.co/login. The domain uses a "1" instead of an "i" (m1crosoft) — this is a clear typosquat / impersonation of Microsoft.
* The date inside the email body (2025-01-24) also does not line up with when the message was actually received, which is another weak/fake detail.
* Searched email history for the recipient (`datasource : "email" AND recipient : "c.allen@thetrydaily.thm"`) — the phishing message is present alongside other unrelated inbound mail.
* Checked firewall for interaction: no results for SourceIP 102.89.222.143, and no clean firewall hit showing a browse to the m1crosoftsupport.co login URL. So the lure landed, but we do not have evidence the user completed the click from the corporate network.

## Evidence & Analysis

<!-- The specific Kibana queries/searches you ran, what fields/indicators you pivoted on, and what each piece of evidence told you. Include relevant screenshots of your Kibana searches/dashboards as supporting evidence (not as a substitute for written analysis). -->

### Alert 8814 — assigned alert + mailbox search

* Reviewed the assigned alert card for "Inbound Email Containing Suspicious External Link" (Alert 8814): sender onboarding@hrconnex.thm, recipient j.garcia@thetrydaily.thm, link in body to the hrconnex.thm onboarding path.

![Alert 8814 — HR onboarding phishing alert](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2022.44.22.png)

* Kibana query: `datasource : "email" and recipient : "j.garcia@thetrydaily.thm"` — shows the onboarding message(s) plus normal internal mail activity from the user in the same window. No attachment-based delivery.

![Email search for j.garcia@thetrydaily.thm](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2022.51.58.png)

* Firewall pivots on the onboarding URL / hrconnex.thm domain did not return matching browse events (search errors on the attempted queries). That absence, together with the benign-looking HR wording, supports closing with no confirmed user interaction.

![Failed firewall URL query (syntax)](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2022.55.51.png)

![Failed firewall domain query (syntax)](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2022.56.39.png)

* Platform incident report closed as **False positive**, reason: no evidence of interaction with email.

![Incident report — False positive closure](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2023.15.29.png)

### Alert 8815 / 8816 — Amazon email + blocked click

* Alert 8815 card: inbound Amazon-themed lure, urgents@amazon.biz → h.harris@thetrydaily.thm, shortened URL in plain text.

![Alert 8815 — Amazon package phishing email](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2023.26.35.png)

* Query: `datasource : email and sender : "urgents@amazon.biz"` — single matching document, confirms content and recipient.

![Email search for urgents@amazon.biz](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2023.29.11.png)

* Query: `datasource : "firewall" AND URL : "http://bit.ly/3sHkX3da12340"` — one blocked web-browsing event from 10.20.2.17 to 67.199.248.11:80 at 21:25:47.616 UTC. This is the key pivot: the user (or that workstation) did click, and the firewall stopped it.

![Firewall block of bit.ly URL](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2023.31.11.png)

* Follow-up: `datasource : "firewall" AND URL : "http://bit.ly/3sHkX3da12340" OR DestinationIP : 67.199.248.11` and `datasource : "firewall" AND DestinationIP : 67.199.248.11` — still only that one blocked hit, so no repeated successful access observed.

![Firewall pivot on URL or DestinationIP](IntroToPhishing_Assets/Screenshot%202026-09-23%20at%2023.34.39.png)

![Firewall search on DestinationIP 67.199.248.11](IntroToPhishing_Assets/Screenshot%202026-09-24%20at%2000.32.22.png)

* Alert 8816 is the High-severity firewall alert for the same blocked blacklist URL access.

![Alert 8816 — blacklisted URL blocked](IntroToPhishing_Assets/Screenshot%202026-09-24%20at%2000.20.32.png)

### Alert 8817 — Microsoft typosquat email + no click evidence

* Alert 8817 card: no-reply@m1crosoftsupport.co → c.allen@thetrydaily.thm, link https://m1crosoftsupport.co/login. Typosquat is obvious from the sender and URL alone.

![Alert 8817 — Microsoft unusual sign-in lure](IntroToPhishing_Assets/Screenshot%202026-09-24%20at%2002.18.18.png)

* Query: `datasource : "email" AND recipient : "c.allen@thetrydaily.thm"` — phishing message present in the mailbox logs.

![Email search for c.allen@thetrydaily.thm](IntroToPhishing_Assets/Screenshot%202026-09-24%20at%2002.29.40.png)

* Firewall checks for the claimed sign-in IP and for browse activity to the phishing URL did not show matching allowed (or even blocked) traffic we could use as a click confirmation.

![No firewall results for SourceIP 102.89.222.143](IntroToPhishing_Assets/Screenshot%202026-09-24%20at%2002.28.55.png)

![Attempted firewall query involving m1crosoftsupport.co URL](IntroToPhishing_Assets/Screenshot%202026-09-24%20at%2002.28.04.png)

## Indicators of Compromise

<!-- A clean, listed set of IOCs identified (sender addresses, URLs, domains, hashes, subject lines, etc. — whatever applies to that scenario). -->

| Indicator Type | Indicator | Related alert |
|---|---|---|
| Email sender | `onboarding@hrconnex[.]thm` | 8814 |
| URL | `https://hrconnex[.]thm/onboarding/15400654060/j[.]garcia` | 8814 |
| Subject | Action Required: Finalize Your Onboarding Profile | 8814 |
| Email sender | `urgents@amazon[.]biz` | 8815 |
| URL | `http://bit[.]ly/3sHkX3da12340` | 8815 / 8816 |
| Domain | `amazon[.]biz` | 8815 |
| Subject | Your Amazon Package Couldn’t Be Delivered – Action Required | 8815 |
| Destination IP | `67[.]199[.]248[.]11` | 8816 |
| Source IP (internal) | `10[.]20[.]2[.]17` | 8816 |
| Email sender | `no-reply@m1crosoftsupport[.]co` | 8817 |
| Domain / URL | `m1crosoftsupport[.]co` / `https://m1crosoftsupport[.]co/login` | 8817 |
| Subject | Unusual Sign-In Activity on Your Microsoft Account | 8817 |
| Claimed sign-in IP (in lure) | `102[.]89[.]222[.]143` | 8817 |

## Verdict & Severity

<!-- Your final classification (e.g. True Positive / False Positive / Benign True Positive) and a severity rating, with justification. -->

| Alert | Severity | Verdict (TP/FP) |
|---------|-------|-------|
| 8814 (HR onboarding / j.garcia) | Medium | False Positive |
| 8815 (Amazon package / h.harris) | Medium | True Positive |
| 8816 (Firewall block / 10.20.2.17) | High | True Positive |
| 8817 (Microsoft lure / c.allen) | Medium | True Positive |

### Justification

* **8814:** The email does not seem to come from a clearly malicious source on its face (HR-style onboarding language and hrconnex.thm path). More importantly, there is no evidence that the recipient interacted with the URL in the email from the organisation’s network, so this was closed as a False Positive.
* **8815:** Sender domain, urgency language, and bit.ly link are typical phishing. This is a real phishing delivery to a corporate mailbox.
* **8816:** Firewall logs prove an internal host tried to open the same malicious URL and was blocked by "Blocked Websites". True Positive — the blacklist hit was real; the click was contained and no successful outbound browse was observed beyond the block.
* **8817:** Typosquat domain (m1crosoftsupport.co) and fake Microsoft security scare tactics make this a clear phishing True Positive. No firewall evidence of a completed click was found during this investigation.

## Recommendations & Remediation

<!-- What should be done next — user actions, blocking/containment steps, detection improvements, and anything you'd recommend the SOC change going forward. -->

* Quarantine / delete the confirmed phishing messages (Amazon and Microsoft lures) from the affected mailboxes and any other copies if they were forwarded.
* Keep (or add) blocks for `bit.ly/3sHkX3da12340`, `67.199.248.11`, `amazon.biz` (sender), and `m1crosoftsupport.co` at mail gateway and web filter where not already covered.
* Speak to h.harris (and the owner of 10.20.2.17) about the click — confirm whether credentials or personal data were entered anywhere before/despite the block, and reset passwords if there is any doubt.
* Notify c.allen not to use the Microsoft “Review Activity” link; remind them of the official account-security path only.
* The organization's security policies should be updated / enforced so staff understand that unexpected delivery notices and account-security emails with external links are high risk, especially when the domain is slightly off.
* The organization should conduct workshops or training for staff in order to educate them about potential security risks that could arise due to their actions (shortened links, typosquat domains, urgency language).

## Lessons Learned

<!-- Anything that would help a fellow analyst investigate this faster next time. -->

* This kind of alert is only fully understood once you check whether anyone from inside the organisation’s network interacted with the URL — so check the firewall or proxy logs that lead to the gateway early, using the exact URL from the email body.
* Shortened links (bit.ly) and typosquat domains (m1 / i swaps) are strong phishing signals on their own; do not wait for enrichment before pivoting to firewall.
* A blocked firewall hit still means the user clicked — treat that as confirmed interaction even when containment worked.
* Absence of firewall hits (as with the HR onboarding and Microsoft cases here) is useful negative evidence, but watch query syntax carefully so a bad search is not mistaken for “no traffic”.
