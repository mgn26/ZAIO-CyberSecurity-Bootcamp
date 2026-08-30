## Metadata

<!-- Alert ID, name, date/time triggered, analyst, severity, verdict
(TP/FP), status. -->

|  Field  | Value |
|---------|-------|
| Operation ID | fake-zoom-ransomware-pipeline |  
| Name | Fake Zoom to Ransomware: The Social Engineering Pipeline |  
| Time (UTC) | 2024-05-01 08:22:04 |  
| Analyst | Mojalefa |  
| Difficulty | Advanced |  
| Severity | Critical|  
| Verdict (TP/FP) | True Positive |  
| Status | Incident Response - Identification, Containment and Eradication Phases |

## Executive Summary

<!-- 3–5 sentences a non-technical manager could read: what
happened, was it real, impact, what you did. -->

Attackers kicked things off with a web compromise, chaining together d3f@ckloader and IDAT loader to drop heavy-hitting C2 frameworks like Cobalt Strike and Brute Ratel. After tunneling in with RDP and proxy tools to move laterally, they used our enterprise management software to mass-deploy BlackSuit ransomware across the network. We validated the breach by pulling SIEM, XDR, and firewall logs to map out the whole kill chain, then moved fast to isolate affected systems, kill the C2 channels, and lock down our software deployment tools.

## Operation Details

<!-- Triggering rule, source/destination, user/host, artefact,
direction, detection product. -->

|  Attribute  | Value |
|---------|-------|
| Triggering Detection | Confluence OGNL Exploitation Chain |  
| Source | 92.51.2[.]27 |  
| Host | adriana.garcia |  
| Artifact | rhddiicoE.README.txt, Zoom_v_2.00.4.exe, Veeam-Get-Creds-New.ps1, PDQDeployService.exe |  
| Direction | Inbound |  
| Tool Surfaces Used | SIEM, Firewall, XDR |  

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
