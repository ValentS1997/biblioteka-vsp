# Source findings — Глава 17. Azure Kubernetes Service

**Policy:** RAG-only pp561–586, chunks p0561:c01–p0586:c01. No external checking or silent corrections. Source gaps are marked **[Needs confirmation]**.

## F-01 — [Source code mismatch] — AKS cluster spelling in CLI vs portal
- **p0570–p0571:** `az aks create` and `az aks get-credentials` specify **`aksmyfirstakscluster-eus`**.
- **p0573:** source prose refers to portal cluster **`aks-myfirstakscluster-eus`**, with additional hyphen after `aks`.
- **Boundary:** these are different identifiers; the RAG does not show a rename/alias. Do not silently repair or claim both targets exist. Actual resource name **[Needs confirmation]**.

## F-02 — [Needs confirmation] — historical Azure free credits
- **p0564:** source describes 12-month service access and **$200 credit**, with card required p0565.
- **Boundary:** figures apply to source writing period. Current eligibility, billing rules and whether AKS node pools/addons are covered **[Needs confirmation]**.

## F-03 — [Needs confirmation] — remote Azure CLI installer
- **p0566:** Linux command directly executes downloaded content: `curl -L https://aka.ms/InstallAzureCli | bash`; Windows alternative downloads/runs MSI with PowerShell.
- **Boundary:** chapter does not validate exact binary/script checksum, publisher/signatures or secure rollback. It is not an independently audited production installer.

## F-04 — [Needs confirmation] — Cloud Shell creates Azure storage
- **p0567–p0568:** source chooses Mount storage account and the option to **create a storage account** for persistence.
- **p0569:** Cloud Shell starts authenticated; `az login` not required.
- **Boundary:** persistent configuration, subscription selection, storage billing, exposure of kubeconfig and actual access rights are not tested. Storage creation isn't a no-side-effect convenience.

## F-05 — [Needs confirmation] — Azure CLI login identity
- **p0567:** `az login`, `az login --use-device-code` and `az account show` supplied.
- **p0569:** group create proceeds without an explicit displayed selection of an intended subscription.
- **Boundary:** target subscription and RBAC beyond current login **[Needs confirmation]**; a successful login is not proof that the right subscription has been selected.

## F-06 — [Needs confirmation] — generated SSH key files
- **p0570:** cluster creation uses `--generate-sshkeys` and explains that public/private SSH keys are produced.
- **Boundary:** file storage, protection, key lifecycle and impact on node access are not detailed. Current CLI behavior and credentials **[Needs confirmation]**.

## F-07 — [Needs confirmation] — default worker VM size
- **p0570:** source describes default VM as `Standard_DS2_v2` with 2 vCPU/7 GiB.
- **p0583:** alternate `--node-vm-size standard_ds3_v2` described as 4 vCPU/16 GiB and cheaper.
- **Boundary:** current region SKU availability, VM sizing defaults and relative cost **[Needs confirmation]**.

## F-08 — [Needs confirmation] — unpinned Guestbook manifests
- **p0572:** six remote URL manifests are applied from mutable `GoogleCloudPlatform/kubernetes-engine-samples/main`.
- **Boundary:** full YAML is not printed in chapter; images, RBAC, selectors, service settings, version/digest and current URL contents are not verifiable within RAG. Do not call these files fully audited.

## F-09 — [Source wording/code mismatch] — public workload with no SSL
- **p0573:** Guestbook is accessed through an **external public IP over HTTP**, and text explicitly states **SSL certificate not configured**.
- **Boundary:** a functional guestbook display is not proof of TLS, login security, protection of user content or enterprise internet exposure controls. No HTTPS configuration/source command is given. **[Needs confirmation]**.

## F-10 — [Needs confirmation] — monitoring enabled vs monitored SLO
- **p0570, p0581–p0582:** creation includes `--enable-addons monitoring` and Insights displays resource metrics via Azure Log Analytics.
- **Boundary:** data collection is described, but log retention, billable ingestion, Alert rule delivery, SLO and sustained functioning under faults are not demonstrated. **[Needs confirmation]**.

## F-11 — [Source wording/code mismatch] — no persistent data vs full application portability
- **p0578:** sample explicitly says persistent Storage not used; configured ConfigMaps/Secrets not used beyond system objects.
- **p0585:** source broadens the conclusion toward seamless cloud portability of workloads.
- **Boundary:** one simple stateless-ish Guestbook with unexamined Redis durability does not establish seamless migration of IAM, PV, VNet, load balancers, database state or production security. **[Needs confirmation]**.

## F-12 — [Needs confirmation] — portal Run command rights
- **p0578:** Azure Portal `Run command` described as executing kubectl without local shell or Cloud Shell.
- **Boundary:** no live command, identity permissions, audit effect or rollback demonstration. Viewing portal data and running cluster-mutating commands must not be treated as equivalent.

## F-13 — [Needs confirmation] — control-plane/node-pool compatibility claim
- **p0579–p0580:** book says upgrade control plane first, then node pools, and claims backward compatibility within three releases.
- **Boundary:** no actual staged version-upgrade test; current AKS/Kubernetes version policy, release skew and safe rollback **[Needs confirmation]**.

## F-14 — [Needs confirmation] — KEDA portal event list
- **p0580:** source lists Service Bus, Cron, Memory, CPU as portal-supported event sources **at writing time**.
- **Boundary:** contemporary AKS add-on capabilities and available scalers unverified; chapter does not configure KEDA workload or run autoscaling benchmark.

## F-15 — [Source wording/code mismatch] — cluster deletion does not delete group
- **p0582:** `az aks delete` first removes the cluster only; `az group delete` then removes resource group.
- **Boundary:** cannot describe `az aks delete` as full resource group teardown. Conversely, `az group delete` can remove **every** resource in a shared group. No verified recovery/complete billing audit **[Needs confirmation]**.

## F-16 — [Needs confirmation] — historic monthly costs
- **p0583:** ~$213/month two `Standard_DS2_v2`, ~$286/month paid management, ~$140/month alternative two `standard_ds3_v2`.
- **Boundary:** no current Azure pricing or account bills, and quoted figures do not prove free control plane or the specific current cost of monitoring, storage, public IP and traffic. **[Needs confirmation]**.

## F-17 — [Needs confirmation] — provider capability comparison
- **p0583–p0584:** table 17.1 broadly claims GKE automatic control plane/node upgrades, EKS manual node upgrades, free control plane for GKE and AKS, platform quality, secure architecture, serverless options.
- **Boundary:** table contains source-era comparisons, not reproducible tests or current public-cloud specifications; provider tiers/settings are omitted. Cross-chapter GKE estimated costs vs its table 17.1 free-control-plane shorthand need scoping, not silent reconciliation. **[Needs confirmation]**.

## F-18 — [Source wording/code mismatch] — subjective ranking presented after general comparison
- **p0585:** author ranks AKS first, GKE second, EKS third and characterizes EKS as less polished.
- **p0584:** table includes qualitative ease/security/scalability ratings without controlled test results.
- **Boundary:** this is an **author viewpoint**, not a verified universal ranking or requirement to choose Azure. User workload, cloud integrations and current offers [Needs confirmation].

## F-19 — [Needs confirmation] — backup discussed but not restored
- **p0580:** Backup menu claims Kubernetes workload/data backup support.
- **p0582:** deletion is demonstrated without backup setup, restore verification, retention or data migration.
- **Boundary:** the presence of a portal feature does not prove the tutorial created reliable backups; cluster/group deletion may be irreversible. **[Needs confirmation]**.

**Safety:** no local/cloud execution, canonical source modifications or reading-status updates. Evidence limitations belong to the book as extracted, not corrected from outside knowledge.
