## Executive Summary

<!-- 3–5 sentences. What happened, what you found, what your verdict is, and what you recommend — written so a CISO could read only this section and still know what they need to know. -->

On 24 September 2026 the SOC worked four alerts under the Phishing Unfolding case set. The first was an inbound inheritance / “hat fortune” scam to support@tryhatme.com from eileen@trendymillineryco.me — no attachments and no links, but classic social-engineering language asking for banking details (True Positive). Two Low-severity Sysmon parent-child alerts on win-3459 (TrustedInstaller.exe) and win-3451 (taskhostw.exe KEYROAMING) matched normal Windows process behaviour and are False Positives. The serious finding is High-severity activity on win-3450: powershell.exe spawned nslookup.exe against a suspicious haz4rdw4re.io subdomain from C:\Users\michael.ascot\downloads\exfiltration\, which looks like DNS-based data exfiltration (True Positive). Recommend isolating win-3450 / user michael.ascot, blocking haz4rdw4re.io, deleting the scam email, and tuning the parent-child detections that keep firing on legitimate Windows binaries.

## Incident Details

<!-- Date/time of the alert, alert source, affected user(s)/asset(s), classification of the alert type. -->

| Field | Value |
|---------|-------|
| Alert Source | Email / Sysmon |
| Alert IDs | 1000, 1001, 1002, 1025 |
| Time of Alerts (UTC) | 09/24/2026 16:23:58.148 – 09/24/2026 17:02:41.535 |
| Affected Users/Assets | support@tryhatme.com; win-3459; win-3451; win-3450 (michael.ascot) |
| Alert Type | Phishing / Suspicious Parent Child Relationship |

### Per-alert breakdown

| Alert ID | Time (UTC) | Source | Affected | Subject / Event |
|---|---|---|---|---|
| 1000 | 09/24/2026 16:23:58.148 | Email | support@tryhatme.com | Inheritance Alert: Unknown Billionaire Relative Left You Their Hat Fortunes |
| 1001 | 09/24/2026 16:26:22.148 | Sysmon | win-3459 | services.exe → TrustedInstaller.exe |
| 1002 | 09/24/2026 16:28:46.148 | Sysmon | win-3451 | svchost.exe → taskhostw.exe KEYROAMING |
| 1025 | 09/24/2026 17:02:41.535 | Sysmon | win-3450 / michael.ascot | powershell.exe → nslookup.exe (DNS exfil domain) |

## Investigation Timeline

<!-- A chronological account of your investigation: what you looked at first, what led you to look at the next thing, and why. This should read as a narrative, not a list of screenshots. -->

### Alert 1000 — Inheritance scam email (support@tryhatme.com)

* Started with the assigned phishing alert: suspicious email from an external domain with an unusual TLD (.me). SOC Lead note on the rule says it still needs fine-tuning, severity Low.
* Email has no attachments, there are no embedded URL(s).
* The email content, subject line and sender domain/email address definitely look suspicious. The reasoning behind this claim is derived from the set of keywords used ("Billionaire", "Fortunes", "inheritance", "banking details", "immediately"), these are typical social enginnering terms typically used in an attempt to exploit a persons naivety.
* Sender is eileen@trendymillineryco.me, recipient support@tryhatme.com, subject "Inheritance Alert: Unknown Billionaire Relative Left You Their Hat Fortunes".
* Pivoted in the SIEM on the sender to confirm there was only this one delivery and to pull the full content field for the report.
* Even without a link or malware attachment, asking for banking details in an unexpected “inheritance” mail is enough to treat this as real phishing / social engineering against the support mailbox.

### Alert 1001 — TrustedInstaller parent-child (win-3459)

* Next alert was Sysmon “Suspicious Parent Child Relationship”: services.exe spawning TrustedInstaller.exe on host win-3459.
* Looked up the host + process in logs to confirm path, parent, and working directory before deciding if this was malware or noise.
* Process path is C:\Windows\servicing\TrustedInstaller.exe, parent is services.exe, working directory C:\Windows\system32\ — this lines up with how Windows Component-Based Servicing normally starts TrustedInstaller.
* No odd command-line arguments, no user Downloads path, nothing that ties this back to the phishing email. Closed as False Positive / detection noise (rule still needs tuning, same theme as the SOC Lead note on Alert 1000).

### Alert 1002 — taskhostw KEYROAMING (win-3451)

* Similar Low-severity parent-child alert on win-3451: svchost.exe → taskhostw.exe with command line `taskhostw.exe KEYROAMING`.
* Checked the specific PID on that host to make sure we were looking at the same event the alert fired on.
* taskhostw.exe under system32 with a KEYROAMING argument and svchost as parent is consistent with normal Windows credential / task-host behaviour, not with a post-phish payload.
* No link to support@tryhatme.com or to michael.ascot activity. False Positive.

### Alert 1025 — nslookup DNS exfiltration (win-3450)

* High-severity parent-child alert is the one that actually matters: on win-3450, powershell.exe (PID 3728) spawned nslookup.exe (PID 5520).
* Command line queries a long subdomain under haz4rdw4re.io: `UEsDBBQAAAAIANigLlfVU3cDIgAAAI.haz4rdw4re.io`. The leading `UEsDBB` pattern is typical of base64 that starts like a ZIP/PK header — classic DNS tunnelling / staged exfil style naming.
* Working directory is C:\Users\michael.ascot\downloads\exfiltration\ — that folder name alone is a strong signal this is not a normal DNS lookup.
* Confirmed the event in Sysmon with a host + PID search; single matching Process Create for that nslookup.
* This is treated as confirmed malicious activity (True Positive): living-off-the-land DNS lookup abused for possible data exfiltration from michael.ascot’s workstation, not related to the inheritance email’s delivery method but still in-scope for this unfolding investigation set.

## Evidence & Analysis

<!-- The specific Kibana queries/searches you ran, what fields/indicators you pivoted on, and what each piece of evidence told you. Include relevant screenshots of your Kibana searches/dashboards as supporting evidence (not as a substitute for written analysis). -->

### Alert 1000 — assigned alert + sender search

* Reviewed Alert 1000 card: “Suspicious email from external domain”, phishing category, Low severity. Content asks for banking details immediately; attachment None; no URL in the body.

![Alert 1000 — inheritance phishing email](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2017.28.22.png)

* Query: `datasource : "email" and sender : "eileen@trendymillineryco.me"` — single inbound document to support@tryhatme.com, confirms subject/content and that this was not a mass blast we could see in the same window.

![Email search for eileen@trendymillineryco.me](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2017.30.37.png)

### Alert 1001 — TrustedInstaller on win-3459

* Alert 1001: Suspicious Parent Child Relationship, services.exe → TrustedInstaller.exe, host win-3459.

![Alert 1001 — TrustedInstaller parent-child](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2017.47.40.png)

* Query: `host.name : "win-3459" and process.name : "TrustedInstaller.exe"` — path under C:\Windows\servicing\, parent services.exe, system32 working directory. Looks like legitimate Windows servicing, not attacker tooling.

![Sysmon search TrustedInstaller on win-3459](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2018.10.21.png)

### Alert 1002 — taskhostw on win-3451

* Alert 1002: svchost.exe → taskhostw.exe KEYROAMING on win-3451 (alert shown closed in the UI at the time of capture).

![Alert 1002 — taskhostw KEYROAMING](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2018.11.07.png)

* Query: `host.name : "win-3451" and process.name : "taskhostw.exe" and process.pid : "3585"` — matches the alerted PID; command line and parent are consistent with normal OS behaviour.

![Sysmon search taskhostw PID 3585 on win-3451](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2018.12.12.png)

### Alert 1025 — nslookup exfil on win-3450

* Alert 1025: High severity. powershell.exe parent, nslookup.exe child, working directory under michael.ascot\downloads\exfiltration\, DNS name on haz4rdw4re.io.

![Alert 1025 — nslookup DNS exfiltration](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2018.13.40.png)

* Query: `host.name : "win-3450" and process.pid : "5520"` — confirms the Process Create for nslookup with the exfil-style FQDN and the exfiltration working directory.

![Sysmon search nslookup PID 5520 on win-3450](PhishingUnfolding_Assets/Screenshot%202026-09-24%20at%2018.49.19.png)

## Indicators of Compromise

<!-- A clean, listed set of IOCs identified (sender addresses, URLs, domains, hashes, subject lines, etc. — whatever applies to that scenario). -->

| Indicator Type | Indicator | Context |
|---|---|---|
| Email sender | `eileen@trendymillineryco[.]me` | Inheritance / banking-details scam to support@tryhatme.com |
| Domain | `trendymillineryco[.]me` | External sender domain (unusual TLD) |
| Subject | Inheritance Alert: Unknown Billionaire Relative Left You Their Hat Fortunes | Alert 1000 lure |
| Host | `win-3450` | Host used for nslookup DNS activity |
| User / path | `michael[.]ascot` / `C:\Users\michael[.]ascot\downloads\exfiltration\` | Working directory for exfil-style nslookup |
| Parent process | `powershell[.]exe` (PID 3728) | Spawned nslookup |
| Process / command | `nslookup[.]exe` → `UEsDBBQAAAAIANigLlfVU3cDIgAAAI[.]haz4rdw4re[.]io` | Likely DNS tunnelling / data exfiltration |
| Domain | `haz4rdw4re[.]io` | DNS destination used in nslookup |

## Verdict & Severity

<!-- Your final classification (e.g. True Positive / False Positive / Benign True Positive) and a severity rating, with justification. -->

| Alert | Severity | Verdict (TP/FP) |
|---------|-------|-------|
| 1000 (Inheritance email / support@tryhatme.com) | Low | True Positive |
| 1001 (TrustedInstaller / win-3459) | Low | False Positive |
| 1002 (taskhostw KEYROAMING / win-3451) | Low | False Positive |
| 1025 (nslookup DNS / win-3450) | High | True Positive |

### Justification

* **1000:** Even with no attachments and no URLs, the subject/body are a clear inheritance social-engineering scam asking for banking details from an external .me sender. Detection is noisy (SOC Lead already flagged fine-tuning), but the email itself is still phishing — True Positive.
* **1001:** services.exe → TrustedInstaller.exe from the normal servicing path is expected Windows behaviour. No IOCs tying it to phishing. False Positive.
* **1002:** svchost.exe → taskhostw.exe KEYROAMING under system32 is consistent with legitimate OS activity. False Positive.
* **1025:** PowerShell spawning nslookup to a haz4rdw4re.io subdomain that looks encoded, from a folder literally named exfiltration under michael.ascot’s Downloads, is strong evidence of DNS-based data exfiltration. True Positive.

## Recommendations & Remediation

<!-- What should be done next — user actions, blocking/containment steps, detection improvements, and anything you'd recommend the SOC change going forward. -->

* Quarantine / delete the inheritance scam email from support@tryhatme.com and block sender eileen@trendymillineryco.me / domain trendymillineryco.me at the mail gateway.
* Isolate or closely monitor win-3450 and the michael.ascot account until host forensics is done; assume possible data theft via DNS until proven otherwise.
* Block domain haz4rdw4re.io (and related DNS tunnelling patterns) on DNS / firewall / proxy.
* Collect further Sysmon / PowerShell / DNS logs around 17:02 UTC on win-3450 (parent powershell PID 3728, other children, files under downloads\exfiltration\).
* Tune the “Suspicious Parent Child Relationship” detections so TrustedInstaller and taskhostw KEYROAMING under their normal system paths do not keep generating Low-severity noise — same fine-tuning theme already noted by the SOC Lead on the email rule.
* Remind support staff that unexpected inheritance / fortune emails asking for banking details are phishing even when there is no link to click.

## Lessons Learned

<!-- Anything that would help a fellow analyst investigate this faster next time. -->

* No attachment and no URL does not mean the email is safe — content and ask (banking details, urgency, inheritance) can still make it a True Positive.
* Always pivot parent-child process alerts to full command line + working directory; that is what separated the two FP Windows alerts from the High TP nslookup case.
* Folder names and encoded-looking DNS labels (e.g. UEsDBB… under haz4rdw4re.io) are quick wins when hunting for DNS exfiltration.
* Treat Low-severity parent-child alerts as triage candidates for FP tuning, but still open High ones fully — severity here matched reality.
