# Commands — Глава 16: Amazon EKS on AWS

**Provenance:** only RAG PDF pp537–560, `p0537:c01`–`p0560:c01`. Ниже исторические команды из источника, **не исполнялись**. Для мутирующих действий фиксируются effect, risk, verification, rollback. Отсутствующие процедуры обозначены **[Needs confirmation]**.

## Install and version: local operations

| Command | Class; effect, risk | Page |
|---|---|---:|
| `brew install awscli` | local state-changing: installs AWS CLI on macOS; package trust not independently verified | 541 |
| `aws --version` | read-only: CLI version (p541 uses typographic `aws –version`, p542 ASCII `--version`) | 541–542 |
| `sudo apt-get install unzip curl` | privileged local package installation if dependencies missing | 541 |
| `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"` | downloads current URL content; archive integrity [Needs confirmation] | 542 |
| `unzip awscliv2.zip` | local extraction | 542 |
| `sudo ./aws/install` | privileged installation of previously downloaded executable; review source/checksums | 542 |
| `choco install awscli` | local Windows installation | 542 |
| `brew install eksctl` | local macOS installation | 546 |
| `choco install eksctl` | local Windows installation | 546 |
| `eksctl version` | read-only local version query | 546 |

**Source extraction detail:** `aws –version` with en dash in p541 is **not** the same bytes as `aws --version` on p542. Correctly quoted source variant retained, no assertion of tested execution. No source-supplied uninstall/revert for local packages — **[Needs confirmation]**.

Linux installation eksctl p546, line-wrap normalized:
```bash
PLATFORM=$(uname -s)_$(uname -m)
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"
tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

**Effect:** detects system architecture, downloads unpinned `latest` binary archive, extracts and moves executable into system directory; deletes local archive. **Risk:** supply-chain integrity, unexpected binary update, privileged overwrite, version drift, architecture incompatibility. **Verification:** `eksctl version` is provided by source; signature/checksum verification and uninstall **[Needs confirmation]**. No live download performed.

## IAM identity and secret keys (GUI + CLI)

Book pp540, 542–545: create account with payment method; enable/access IAM Identity Center for one account, create IAM user `ekscluster`, attach **`AdministratorAccess`**, create a programmatic **access key**, download CSV. Book later (p553) enables **Console access** for this same user, generating another credential CSV. **These are security-sensitive, state-changing GUI actions, not read-only checks**.

```bash
aws configure
aws ec2 describe-regions
```

p545. **Effect:** `configure` writes long-term AWS access key, secret and default region to local AWS profile; source inputs default region `us-west-2`. **Risk:** leakage of credential CSV, overly privileged IAM user, wrong region/account, persistence on disk. Never place real keys in notes/CI/CLI history. **Verification:** `aws ec2 describe-regions` confirms a working AWS API request, **not** least-privilege policy, specific EKS permission or verified account. **Rollback:** credential rotation, IAM cleanup and local-profile removal **not specified** in source — [Needs confirmation]. The source says user should be deleted eventually (p544), but no actual deletion command or result is shown.

## eksctl: resource creation (BILLABLE, high-impact)

```bash
eksctl create cluster
kubectl get nodes
```

pp547–549. **Effect:** creates AWS EKS control plane, VPC/subnets, 2 EC2 `m5.large` worker nodes in a managed node group and **two CloudFormation stacks**; writes kubeconfig and may modify current `kubectl` context. **Risks:** immediate cloud charges, incorrect IAM/account/region, default public EKS API endpoint, lack of CloudWatch control-plane logs, orphaned resources and irreversible data effects during later teardown. **Verification:** `kubectl get nodes` has two Ready workers; source's terminal shows one managed node group Ready, AWS Console EKS/EC2/CloudFormation. **Rollback:** source `eksctl delete cluster --name <generated-name>` is destructive and may not remove all resources; recovery [Needs confirmation].

**Critical mismatch:** p547 prose lists `Region: us-west-1`, but p545 `aws configure` selects `us-west-2`, and p547–p549 CLI logs show `using region us-west-2`. Do not presume that same `eksctl create cluster` will target either without explicit context verification. Generated cluster name in source `hilarious-wardrobe-1717847351` belongs only to that run.

Diagnostic-only suggestion printed in eksctl output (p547–548), **not shown as executed**:
```bash
eksctl utils describe-stacks --region=us-west-2 --cluster=hilarious-wardrobe-1717847351
```
**Class:** read-only AWS CloudFormation stack inspection (source suggestion); permissions, content and current applicability [Needs confirmation].

## Guestbook app: six source-supported remote YAML URLs

p550 reuses the GoogleCloudPlatform `kubernetes-engine-samples` repository from GKE chapter, with manifests in **mutable `main`**:
```bash
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-service.yaml
kubectl get service frontend
```

**Class:** first six are workload-generating/cluster-state-changing; last is read-only API inspection. **Effect:** creates Deployment and Services for Redis Leader, Redis Follower and frontend; a public AWS Elastic Load Balancer appears for the frontend, exposing a hostname/URL (pp550–555). **Risk:** remote content is not reproduced in RAG and is not SHA-pinned; potential supply chain drift, wrong kubeconfig context, AWS ELB/network cost and public HTTP exposure. **Verification:** `kubectl get service frontend`, source browser Guestbook demo and console EKS/ELB; full manifest security and current URL resolution [Needs confirmation]. **Rollback:** only full cluster deletion shown, no verified granular Guestbook-only rollback or persistence restoration [Needs confirmation].

## AWS Console evidence (read-only unless granting new access)

- pp551–552: sign in and select **US West (Oregon), us-west-2**; EKS cluster page shows **Access denied** for a principal different from the CLI creator.
- p553: IAM UI `Enable console access` for `ekscluster` generates a password/CSV and **expands account access**, not a harmless observation. Then Console sign-in as that user.
- pp553–554: EKS Overview/Resources/Compute/Networking/Add-ons/Access/Observability/Upgrade insights/Update history/Tags.
- pp555–556: EC2 2 worker instances, Load Balancers public frontend, CloudFormation 2 stacks and visual Application Composer. Sources show **two** stacks: managed node group and EKS control plane. IAM policies can affect what each principal sees.
- Control-plane logging in p548 CLI sample disabled; actual log availability in an unknown cluster [Needs confirmation].

## Destructive teardown and costs

```bash
eksctl delete cluster --name hilarious-wardrobe-1717847351
```

p557. **HIGH-RISK DESTRUCTIVE:** supplied cluster name was randomly generated in this historical example; not a template to execute against other accounts. **Effect:** source p558 shows kubeconfig update, cleanup of Kubernetes Service/Ingress AWS load balancers, deletion of managed node-group and control-plane CloudFormation stacks, EC2 workers and EKS cluster. **Risk:** permanent app/data loss, deletion of the wrong cluster, unrelated resources and continued bills for orphans. **Verification:** book instructs inspecting **EC2, EKS, CloudFormation** after deletion, and ELB resources are shown elsewhere (pp555–558); actual resource and bill state [Needs confirmation]. **Rollback:** none in source; backup/recovery procedure [Needs confirmation].

**Historical pricing, pp558–559:** EKS `$0.10/h`, about `$73/month` plus 2 EC2 workers at around `$70/month` each, **total ~$213/month**, excluding ELB/network. Do not reuse as current quote, price calculation or proof that Free Tier covers EKS. Source p537 warns of charges.

## Summary of unsupported runtime claims

Current pricing, Free Tier, account permissions, source package signatures, AWS profile/region, cluster endpoint protection, network access, actual monitoring/logging and application data durability were not tested. Source demonstrates one lab, not a repeatable production SRE runbook. **[Needs confirmation]**.
