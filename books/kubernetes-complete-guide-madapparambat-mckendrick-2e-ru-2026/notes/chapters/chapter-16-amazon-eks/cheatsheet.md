# Cheatsheet — Глава 16. Amazon EKS

**Strict source:** chapter RAG `p0537:c01`–`p0560:c01`, PDF 537–560. No commands run; no external API verification. Historical details are not current AWS advice.

## Symptom / problem framing

Задача: получить учебный управляемый Kubernetes-кластер на AWS, использовать `eksctl` и CloudFormation вместо ручной конфигурации EKS, запустить Guestbook, изучить EKS/EC2/ELB/CloudFormation, затем **проверяемо удалить все платные ресурсы**. EKS интегрируется с IAM, Route 53, EBS, EC2 Auto Scaling и несколькими Availability Zones (pp539–540).

## Baseline / context

- AWS account with payment method; region and billing permissions; macOS/Linux/Windows `aws` + `eksctl`; `kubectl` (pp537, 540–546). Exact account, IAM role, AWS CLI profile, budget, quotas **[Needs confirmation]**.
- Source uses IAM user `ekscluster`, directly attaches **`AdministratorAccess`**, creates an **access key**, downloads credential CSV, then runs `aws configure` with `us-west-2` (pp543–545). These are **high-risk educational steps**; not a secure production IAM baseline.
- `eksctl create cluster` with no args: automatically generated name `hilarious-wardrobe-1717847351`, 2 `m5.large` workers, VPC, managed node group; two CloudFormation stacks (pp545–549). **p547 prose says us-west-1; actual output says us-west-2.** Determine target region before deployment; source cannot resolve contradiction.
- Sample endpoint access `publicAccess=true` and `privateAccess=false`; CloudWatch control-plane logging off (p548). Current settings unconfirmed.
- `eksctl` automatically writes kubeconfig, then `kubectl get nodes` shows two nodes Ready (pp548–549); kubeconfig target MUST be confirmed before any Kubernetes mutations.
- Guestbook: Redis leader + follower, PHP frontend, same 6 remote manifest URLs as GKE chapter 15; source EKS `frontend` Service exposes a public load-balancer **hostname** instead of displayed GKE external IP (p550).
- Historical estimate: $0.10 per EKS hour, ~$73/month control plane + ~$70 per EC2 node, **~$213/month before network/ELB** (pp558–559); no present-day price validation.

## Read-only checks / observation

```bash
aws --version
aws ec2 describe-regions
eksctl version
kubectl get nodes
kubectl get service frontend
```

Book: pp541–542, 545–546, 549–550. These query local CLI version / AWS API / Kubernetes API, but `describe-regions` needs AWS permissions and may reveal account configuration. **Note:** the macOS example p541 renders `aws –version` (single en dash), while Linux/Windows p542 write `aws --version` (two ASCII dashes). Don't copy the malformed command from PDF. `eksctl utils describe-stacks --region=us-west-2 --cluster=hilarious-wardrobe-1717847351` appears in CLI diagnostic output p547–548, **not an executed action**, and may expose stack metadata.

Console inspection (pp551–556): EKS Overview/Resources/Compute/Networking/Add-ons/Access/Observability/Upgrade insights/Update history; EC2 instances; Elastic Load Balancing; two CloudFormation stacks with generated templates. **Only inspect resources of the intended account/region.**

## Interpretation

- A successful `eksctl create cluster` writes kubeconfig and shows ready EC2 workers; **not** proof of application SLO, private API, backup or controlled cost (pp547–549).
- Region contradiction: `aws configure` picks `us-west-2` (p545); p547 lists defaults as `us-west-1`, while CLI output and AWS Console refer to **`us-west-2`** (pp547–551). Current region [Needs confirmation].
- Sample `created 0 nodegroup(s)` during provisioning at p548 is followed by `created 1 managed nodegroup(s)` and 2 Ready nodes p549. Treat the intermediate output as transitional, not final failure.
- EKS cluster created by CLI credentials of `ekscluster` shows an AWS Console *Access denied* to different sign-in principal (p552), although the Console sign-in has account-level access. IAM identity and Kubernetes cluster authorization are not necessarily the same. Book suggests enabling console access for `ekscluster` (p553), a credential and privilege expansion, **not** a least-privilege remediation.
- Reused GKE Guestbook manifests create frontend Service external AWS ELB and internal Redis Services. The full remote files are absent from chapter; current content, data retention and public TLS [Needs confirmation].
- CloudWatch logging default disabled **in sample** (p548). Observability in EKS console is described as less detailed than GKE for this demo (pp554–556), not a current benchmark.

## Next action

Prior to any real work, establish target AWS account and region, cost approval, least-privilege roles/short-lived credentials, private/public endpoint policy, logging, VPC boundaries, working network policies, source review of Guestbook remote YAML, and an explicit resource inventory plus teardown plan. The chapter does not provide those validated production controls — **[Needs confirmation]**.

## Modifying actions (source demonstrations — not executed)

```bash
aws configure
eksctl create cluster
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-service.yaml
```

pp545–550. **Effect:** `aws configure` persists a local secret key/profile; `eksctl create` launches **billable** EKS, EC2/VPC/CloudFormation resources and modifies kubeconfig; six `apply` commands create three Deployment and Services, one public ELB. **Risk:** administrator credentials in local files, wrong AWS region/context, mutable unpinned remote manifests, public app and paid network resources. **Verification:** `kubectl get nodes`, `get service frontend`, Console EKS/EC2/ELB/CloudFormation. **Rollback:** chapter only gives full `eksctl delete cluster --name ...`; not safe for non-disposable clusters, no backup or granular rollback [Needs confirmation].

## Verification / acceptance checks

- `aws --version`, `eksctl version` and `aws ec2 describe-regions` behave as documented by book (p545–546); operational identity requires additional validation not shown.
- Two EC2 worker nodes Ready and one managed node group at end of source `eksctl create` (p549), control plane and node group CloudFormation stacks in AWS Console (p556).
- Guestbook `kubectl get service frontend` returns a public hostname and browser renders sample app (pp550–551). No production HTTP/TLS, data persistence or traffic policy acceptance documented.
- Compare EKS Console Resources/Access and identity; book's Access denied is explicitly linked to differing CLI and Console users (pp552–554).
- On removal, `eksctl` output declares stacks/resources deleted; **inspect EC2, EKS, CloudFormation and ELB** for leftovers and charges (pp557–558).

## Rollback / destructive cleanup

```bash
eksctl delete cluster --name hilarious-wardrobe-1717847351
```

Source p557. **DESTRUCTIVE / potentially irreversible:** drains/deletes workloads, node group and EKS control plane and attempts ELB cleanup, deletes CloudFormation stacks (p558). **Before use verify actual random cluster name, AWS region, identity, resource inventory, backups and cloud billing.** The example name is **not reusable as a default**; it comes from one run. Source lacks recovery of destroyed cluster data and proof that all billable orphan resources vanish — **[Needs confirmation]**.

Source narrative p544 proposes deleting IAM test user `ekscluster` after chapter, but **does not show completed user deletion or key revocation**. Thus cloud teardown and credential cleanup are separate requirements, their execution [Needs confirmation]. No real AWS changes.
