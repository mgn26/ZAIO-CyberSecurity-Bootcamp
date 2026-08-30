## Metadata

<!-- Alert ID, name, date/time triggered, analyst, severity, verdict
(TP/FP), status. -->

|  Field  | Value |
|---------|-------|
| Operation ID | vpn-credential-bruteforce |  
| Name | VPN Brute Force: Credential Attack on the Remote-Access Portal |  
| Time (UTC) | 2026-03-18 06:15:00 |  
| Analyst | Mojalefa |  
| Difficulty | Low |  
| Severity | Critical |  
| Verdict (TP/FP) | True Positive |  
| Status | Incident Response - Identification and Containment Phases |

## Executive Summary

<!-- 3–5 sentences a non-technical manager could read: what
happened, was it real, impact, what you did. -->

Attackers ran a low-and-slow credential spray against our non-MFA (Multi-Factor Authenticated) remote portals by rotating IPs to bypass lockout rules, resulting in a confirmed incident when they matched a valid credential pair and opened a live VPN session. Once inside, the attacker began probing internal systems over the encrypted tunnel, but we contained the breach by killing the active session, resetting the compromised credentials and blocking the attacker's IP range.

## Operation Details

<!-- Triggering rule, source/destination, user/host, artefact,
direction, detection product. -->

|  Attribute  | Value |
|---------|-------|
| Triggering Detection | First VPN session for account from new IP block |  
| Source | 185.159.0[.]209 |  
| Host | 185.159.0[.]112 (d.volkov) |  
| Artifacts | d.volkov, HALCYON-WKS-14 |  
| Direction | Inbound |  
| Tool Surfaces Used | SIEM, Firewall |  

## Investigation & Triage

<!-- Step-by-step analysis; what you checked, what you found,
playbook decisions and why. The longest section. -->



## Threat Intelligence

<!-- Enrichment: VirusTotal/AbuseIPDB/OTX findings, reputation,
known campaign/malware family, attribution. -->

## Timeline

<!-- Time-ordered table of key events (UTC). -->

## Indicators of Compromise

<!-- All IoCs in a table and STIX 2.1 Defanged in prose. -->

|  Type  | Indicator (defanged) | Context |
|---------|-------|-----------|
| | |  

## MITRE ATT&CK Mapping

<!-- Tactics and techniques observed. -->

## Impact & Containment

<!-- What was affected; action taken/recommended (isolate, block,
reset, none). -->

## Conclusion & Recommendations

<!-- Final verdict restated with justification + concrete next steps /
tuning. -->

## Evidence

<!-- Annotated, captioned screenshots referenced from the body. -->
