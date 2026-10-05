# Команды и verification artifacts Chapter 9

Только source-supported examples.

## Listing 35 — Apache log evidence

Source reviews repeated requests to:

```text
/wp-includes/FkhDUPZ.php
```

with unusually large HTTP response sizes.

Purpose:
- correlate recurring system instability with suspicious web activity.

## Listing 36 — inspect suspicious PHP

```bash
cat /var/www/html/wp-includes/FkhDUPZ.php
```

Result:
- obfuscated PHP.

Important source interpretation:
- obfuscation alone does not prove malware;
- corroboration required.

## Listing 37 — domain creation date

```bash
date -u
whois -i rhodeislandturnpike.com | grep -i 'creation date'
```

Purpose:
- compare current time with domain registration age.

## Listing 38 — TLS certificate age

```bash
date -u
curl -svX HEAD https://rhodeislandturnpike.com/ 2>&1 | grep -A6 "Server certificate"
```

Purpose:
- inspect certificate start date and compare with domain age.

## Listing 39 — AWS S3 bucket policy

```bash
aws s3api get-bucket-policy --bucket ssptmsdata | jq '.Policy | fromjson'
```

Purpose:
- verify actual bucket access policy.

Source finding:
- any AWS principal allowed list/get actions.

## Listing 40 — AWS S3 contents

```bash
aws s3 ls s3://ssptmsdata
aws s3 ls s3://ssptmsdata/uat/
```

Purpose:
- determine whether public policy matches business intent/content.

Interpretation:
- public access alone did not prove incident;
- asset owner/business context required;
- verification deferred.

## CTI queries

Chapter names platforms such as:
- VirusTotal
- AlienVault OTX
- Shodan

but does not provide a universal CLI workflow for them.

## Risk notes

Commands above are read-only in the examples shown.

Exception:
- source mentions adding indicators to a threat-intelligence platform, but no platform-specific write command is provided.

## Verification discipline

Do not treat a single artifact as definitive when source itself requires corroboration.

Examples:
- obfuscated PHP ≠ automatically malicious;
- fresh domain ≠ automatically incident;
- public bucket ≠ automatically misconfiguration.
