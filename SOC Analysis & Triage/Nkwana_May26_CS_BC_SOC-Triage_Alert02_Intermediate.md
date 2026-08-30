## Metadata

<!-- Alert ID, name, date/time triggered, analyst, severity, verdict
(TP/FP), status. -->

|  Field  | Value |
|---------|-------|
| Operation ID | cisco-ios-xe-webui-implant |  
| Name | Cisco IOS XE Web UI: Implant and Rogue Admin (CVE-2023-20198) |  
| Time (UTC) | 2026-05-19 07:09:00 |  
| Analyst | Mojalefa |  
| Difficulty | Intermediate|  
| Severity | Critical |  
| Verdict (TP/FP) | True Positive |  
| Status | Incident Response - Identification, Containment, Eradication and Recovery Phases |

## Executive Summary

<!-- 3–5 sentences a non-technical manager could read: what
happened, was it real, impact, what you did. -->

An attacker gained unauthenticated privilege-15 access on router AXFORD-RTR-01 by exploiting CVE-2023-20198 on its inadvertently internet-exposed Cisco IOS XE Web UI, then chained CVE-2023-20273 to drop a persistent Lua implant that hooked the HTTP server and beaconed to an external command-and-control (C2) address. In response, we isolated the affected router, removed the rogue local account and Lua implant, patched the vulnerable Web UI software.

## Operation Details

<!-- Triggering rule, source/destination, user/host, artefact,
direction, detection product. -->

|  Attribute  | Value |
|---------|-------|
| Triggering Detection | Network device Web UI accessed from non-management IP |  
| Source | 185.123.0[.]118 |  
| Host | 185.123.0[.]91 |  
| Artifact | cisco_admin, cisco_service.lua,  |  
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
