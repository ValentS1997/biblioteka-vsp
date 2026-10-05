# Команды и containment artifacts Chapter 12

Только source-supported examples.

## Listing 48 — Windows RDP session query/termination

```cmd
qwinsta /server:rdp-server01
rwinsta 3 /server:rdp-server01
```

Purpose:
- enumerate active RDP sessions;
- terminate identified attacker session.

Risk:
- state-changing;
- may terminate legitimate user work if session ID is wrong.

Verification:
- rerun `qwinsta`.

## Listing 49 — SSH session query/termination

```bash
who
sudo pkill -9 -t pts/1
who
```

Purpose:
- identify and terminate active SSH session.

Risk:
- destructive to active session;
- wrong TTY selection can disconnect legitimate user.

Verification:
- rerun `who`.

## Listing 50 — Splunk unclosed RDP sessions

```text
index=wineventlog EventCode=4624 LogonType=10
| fields _time, TargetUserName, TargetLogonId, IpAddress, Computer
| join type=left TargetLogonId
    [search index=wineventlog EventCode=4634
     | fields TargetLogonId, EventCode]
| where isnull(EventCode)
| table _time, TargetUserName, IpAddress, Computer
```

Purpose:
- find RDP sessions opened without matching close event.

## Listing 51 — Multi-server RDP enumeration

Source provides a PowerShell-based enumeration example across multiple Windows servers.

Purpose:
- identify active sessions enterprise-wide instead of querying one host at a time.

Exact code is preserved in source translation; no additional code is invented here.

## Listing 52 — NetTCPConnection

Source uses PowerShell network-connection output from compromised host.

Purpose:
- capture volatile network state before/while containment.

## Listing 53 — AWS termination protection

Source uses AWS CLI to enable termination protection on contained EC2 instances.

Purpose:
- prevent accidental deletion of evidence.

## Listing 54 — Entra ID OAuth consent grants

Source uses Microsoft Graph PowerShell to enumerate OAuth consent grants.

Purpose:
- compare current application permissions with authorized baseline;
- identify malicious consent.

## Listing 55 — Azure quarantine NSG

```bash
az vm show --name web-prod-01 -g rg-production-eastus2   --query "networkProfile.networkInterfaces[0].id" -o tsv

az network nsg create   --name IR-Quarantine-2025-042   -g rg-production-eastus2 -o none

az network nsg rule create   --nsg-name IR-Quarantine-2025-042   -g rg-production-eastus2   --name AllowSSH-IR   --priority 100   --direction Inbound   --access Allow   --protocol Tcp   --destination-port-ranges 22   --source-address-prefixes 198.51.100.10/32 -o none

az network nsg rule create   --nsg-name IR-Quarantine-2025-042   -g rg-production-eastus2   --name DenyAllOutbound   --priority 100   --direction Outbound   --access Deny   --protocol '*'   --destination-port-ranges '*'   --source-address-prefixes '*'   --destination-address-prefixes '*' -o none

az network nic update   --name web-prod-01-nic   -g rg-production-eastus2   --network-security-group IR-Quarantine-2025-042 -o none
```

Purpose:
- preserve SSH access from IR jump box;
- deny outbound traffic;
- quarantine VM.

Risk:
- state-changing network controls;
- can cut required application/business connectivity.

Verification:
- validate NIC/NSG association and expected allowed/denied traffic.

Rollback:
- restore previous NSG association [Needs confirmation from environment].

## Listings 56–57 — AWS Lambda deny-and-log

Source replaces compromised Lambda code with a function returning 403 while logging invocations, then deploys it with AWS CLI.

Deployment artifact:

```bash
zip function.zip index.js
aws --profile jwright lambda update-function-code   --function-name lambda-function-to-log-and-disable   --zip-file fileb://function.zip
```

Risk:
- state-changing;
- changes production function behavior.

Verification:
- function returns deny response;
- invocations continue to be logged.

Rollback:
- redeploy known-good function version [Needs confirmation].

## Listing 58 — Disable AWS access key

```bash
aws iam list-access-keys   --user-name k8s-service-account   --profile techflow-prod

aws iam update-access-key   --user-name k8s-service-account   --access-key-id AKIATFSHNUL4J3QFDRFE   --status Inactive   --profile techflow-prod
```

Verification:
- list key again and confirm `Inactive`.

## Listing 59 — Tags, termination protection, snapshot

Source actions include:

```bash
aws ec2 create-tags ...
aws ec2 modify-instance-attribute --disable-api-termination ...
aws ec2 create-snapshot ...
```

Purpose:
- mark evidence resources;
- prevent deletion;
- preserve storage state.

## Listing 60 — AWS quarantine security group

Source:
- creates quarantine SG;
- allows SSH only from IR jump box;
- revokes default egress;
- attaches SG to compromised instances.

Risk:
- state-changing;
- can disrupt required connectivity.

Verification:
- inspect SG and instance association;
- confirm outbound blocking.

## Listing 61 — Kubernetes RBAC containment

```bash
kubectl get clusterrolebinding dashboard-secrets-reader -o yaml
kubectl delete clusterrolebinding dashboard-secrets-reader
kubectl annotate serviceaccount dashboard-viewer   -n kubernetes-dashboard   IR-Case=2025-042   Status=Disabled   ContainedBy=sarah-ir-team
```

Purpose:
- disable effective service-account privilege without deleting account evidence.

Risk:
- breaks workloads relying on the binding.

Verification:
- confirm binding absent;
- review K8s audit logs for denied/no further access.

Rollback:
- recreate known-good RBAC binding [Needs confirmation].

## Command discipline

Many examples in this chapter are state-changing.

Before execution:
- confirm target/account/resource;
- preserve evidence where required;
- record rollback point;
- timestamp action.

After execution:
- validate containment through independent telemetry.
