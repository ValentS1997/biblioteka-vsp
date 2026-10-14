# Source findings — Глава 16: Amazon EKS

**Evidence:** strict RAG-only `p0537:c01`–`p0560:c01`, PDF 537–560. Source problems are retained; no outside adjudication or memory-based fixes. Allowed classes: [Source contradiction], [Source code mismatch], [Source wording/code mismatch], [Source extraction issue], [Needs confirmation].

## F-01 — [Source contradiction] — AWS region us-west-1 vs us-west-2
- **p0545:** `aws configure` instructs default region **`us-west-2`**.
- **p0547:** prose claims the default `eksctl create cluster` cluster has **`Region: us-west-1`**.
- **p0547–p0549:** actual output says `using region us-west-2`, AZs `us-west-2d/b/c`, cluster is ready in `us-west-2`; p0551 instructs selecting AWS Console Oregon `us-west-2`.
- **Boundary:** source has two incompatible region variants. Do not silently rewrite `us-west-1` or promise what a fresh no-arg `eksctl` will select; real profile/region **[Needs confirmation]**.

## F-02 — [Source extraction issue] — `aws –version` en dash
- **p0541:** macOS line rendered `aws –version` with typographical en dash.
- **p0542:** Linux/Windows explicitly use `aws --version` with two ASCII hyphens.
- **Boundary:** the PDF extraction variant is not an equivalent command byte sequence. The catalog uses source's unequivocal p0542 variant and records both.

## F-03 — [Needs confirmation] — overly privileged IAM user in lab
- **p0543:** user `ekscluster` is attached directly to the policy **`AdministratorAccess`** instead of a tailored group/role.
- **p0544:** author says these elevated rights are acceptable *for disposable test environment*, while recommending vendor documentation for near-production policies.
- **Boundary:** no least-privilege IAM policy, IAM Roles/SSO workflow or temporary credentials established in the chapter. Production access **[Needs confirmation]**.

## F-04 — [Needs confirmation] — long-term access key and CSV
- **p0544:** IAM access key created and CSV downloaded with key material.
- **p0545:** `aws configure` accepts access key ID and secret key into local profile.
- **p0553:** when Console login is later enabled for that user, another CSV containing login credentials is downloaded.
- **Boundary:** secrets must not enter Git, logs, copied commands or study artifacts. Credential rotation, storage hardening, audit and deletion **[Needs confirmation]**.

## F-05 — [Source wording/code mismatch] — IAM Identity Center vs IAM Users
- **p0542:** guide first routes to `IAM Identity Center`.
- **p0543–p0544:** user is then created via ordinary IAM `Users`, with attached `AdministratorAccess` and IAM access key.
- **Boundary:** source traverses two identity interfaces without explaining their relationship or a unified role model. Do not equate IAM Identity Center identities with IAM users automatically; real IAM architecture **[Needs confirmation]**.

## F-06 — [Source wording/code mismatch] — programmatic-only user vs Console access
- **p0543:** user `ekscluster` created with console-login checkbox **unchecked**.
- **p0552–p0553:** same user is later granted Console access to work around `Access denied` with another principal.
- **Boundary:** later action changes identity's threat surface and is not read-only troubleshooting; no permission-minimizing alternative or rollback supplied **[Needs confirmation]**.

## F-07 — [Source wording/code mismatch] — transitional nodegroup count
- **p0548:** logs say `created 0 nodegroup(s) in cluster` while waiting for nodes.
- **p0549:** later output says `created 1 managed nodegroup(s)` and two nodes Ready.
- **Boundary:** early `0` is a transitional log, not the end-state; cannot conclude a cluster without nodes from the intermediate line.

## F-08 — [Needs confirmation] — default public EKS API endpoint
- **p0548:** source logs `publicAccess=true`, `privateAccess=false`.
- **Boundary:** this is an example output, not a security recommendation or proof of current EKS defaults. API access controls, IP restrictions, network boundaries **[Needs confirmation]**.

## F-09 — [Needs confirmation] — disabled CloudWatch logging
- **p0548:** `CloudWatch logging will not be enabled for cluster`; a suggested enable command appears in program output.
- **p0554:** Console `Observability` described conceptually, but no evidence of source control-plane logs.
- **Boundary:** source does not demonstrate audit/control-plane logging or a current production monitoring configuration. **[Needs confirmation]**.

## F-10 — [Needs confirmation] — random cluster name in deletion
- **p0547–p0549:** `eksctl create cluster` has no `--name`, generating `hilarious-wardrobe-1717847351`.
- **p0557:** `eksctl delete cluster --name hilarious-wardrobe-1717847351` uses that instance-specific identifier.
- **Boundary:** copying the deletion command verbatim cannot target arbitrary future clusters correctly. Real identity, region/account and backup must be established **[Needs confirmation]**.

## F-11 — [Needs confirmation] — mutable remote Guestbook manifests
- **p0550:** six `kubectl apply -f` URL source files from GoogleCloudPlatform `kubernetes-engine-samples/main/quickstarts/guestbook`.
- **Boundary:** external YAML contents not included in chapter RAG, mutable `main` not pinned, source integrity/permissions/images/current compatibility **[Needs confirmation]**. Cross-cloud reuse is shown for the demo but is not a production security review.

## F-12 — [Needs confirmation] — AWS hostname vs GKE IP
- **p0550–p0551:** frontend Service on AWS returns a URL/hostname rather than the displayed GKE IP of chapter 15.
- **p0555:** ELB is created automatically by AWS when frontend is deployed.
- **Boundary:** the particular load-balancer DNS address and availability are environment-specific. A DNS name in sample does not prove private access, TLS or zero downtime; **[Needs confirmation]**.

## F-13 — [Needs confirmation] — AWS Console access denied
- **p0552:** Console principal cannot inspect resources although the cluster is visible.
- **p0553:** the source grants IAM `ekscluster` Console credentials and then access succeeds.
- **Boundary:** this is one demonstrated identity mismatch; not evidence that granting another powerful login is the correct general remedy. IAM/RBAC access mappings and safe repair require review **[Needs confirmation]**.

## F-14 — [Needs confirmation] — host-level and app-level monitoring conflated
- **p0554:** EKS Console Resources shows basic Deployment/Pod information.
- **p0555:** EC2 charts show CPU/memory/network of EC2 **instances**, not Guestbook container/application metrics; p0556 criticizes limited Console observability.
- **Boundary:** comparisons of GKE and EKS are author observations at a specific historical UI state, not a tested benchmark of all available monitoring products or current Console features. **[Needs confirmation]**.

## F-15 — [Needs confirmation] — deletion and residual billable assets
- **p0557–p0558:** `eksctl delete cluster` outputs cleanup of AWS ELB and deletion of two CloudFormation stacks, `all cluster resources were deleted`.
- **p0558:** immediately advises checking EC2, EKS and CloudFormation for orphan/inactive resources still accruing charges.
- **Boundary:** automation success does not guarantee zero billable leftovers or recovery of data. Full inventory, backup, CloudFormation failures, ELB and EBS state **[Needs confirmation]**.

## F-16 — [Needs confirmation] — EKS Free Tier and historical prices
- **p0540:** AWS Free Tier described as 12 months for certain services.
- **p0558–p0559:** `$0.10/hour` EKS, ~$73/month cluster, ~$70/month per EC2 and ~$213/month before networking/ELB.
- **Boundary:** not a current AWS price quote or evidence that these resources are free. Cost assumptions, billing zone, EC2 class and current rates **[Needs confirmation]**.

## F-17 — [Source wording/code mismatch] — eksctl managed service vs exposed infrastructure
- **p0545–p0546:** `eksctl` is described as automating AWS CloudFormation provisioning.
- **p0547–p0549:** example creates VPC/subnets and CloudFormation control plane + node-group stacks, not just a Kubernetes object.
- **Boundary:** cluster lifecycle mutates independently billable AWS resources; `kubectl` workload deletion alone is insufficient to undo `eksctl create cluster`.

## F-18 — [Needs confirmation] — historical AWS facts and defaults
- **p0537–p0539:** AWS market shares and infrastructure counts explicitly refer to mid-2024; `eksctl version`/Kubernetes version 1.29 and AMI on pp547–548 are sample output.
- **Boundary:** no current verification is performed and no statement about live version support, region/AZ default, pricing or AWS market leadership is asserted.

**Scope protection:** source PDF/LFS, RAG, registry, status/dates/progress reading unchanged; no real AWS, IAM or Kubernetes commands executed.
