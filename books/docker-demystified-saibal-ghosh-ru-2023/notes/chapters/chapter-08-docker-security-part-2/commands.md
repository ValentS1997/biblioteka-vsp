# Команды главы 8

Команды основаны только на RAG главы 8. Это source-era Docker Enterprise workflow. Не использовать как current production runbook без отдельной verification branch.

## Read-only / low-impact checks

| Команда | Назначение | Risk |
|---|---|---|
| `docker version` | Engine/client versions | read-only |
| `ifconfig -a eth0` | Node address in source lab | read-only |
| `docker version --format '{{ .Server.Version }}'` | Server version through configured endpoint | read-only |
| `echo "$DOCKER_HOST"` | Client Bundle endpoint | may reveal internal endpoint |
| `echo "$DOCKER_CERT_PATH"` | Certificate directory | path disclosure only |
| `echo "$DOCKER_TLS_VERIFY"` | TLS verification flag | read-only |
| `apt-cache madison docker-ee` | Available package versions in source-era repo | read-only if repo exists |

## Package removal / Docker EE installation

Source begins by removing previous Docker packages:

```bash
apt-get remove docker docker-engine docker-ce docker-ce-cli docker.io
apt-get update
```

Risk: HIGH — removes runtime packages and may stop workloads.

Rollback: `[Needs confirmation]`. Source does not give a full rollback plan.

Source installs APT HTTPS support packages:

```bash
apt-get install apt-transport-https ca-certificates curl software-properties-common -y
```

Then configures a licensed Docker EE repository, imports a GPG key, adds repository, updates APT and installs `docker-ee`, `docker-ee-cli` and `containerd.io`.

Subscription URL from source is deliberately not reproduced. It is license/account-specific and sensitive.

## Verify Engine

```bash
docker run hello-world
docker version
```

Effect of first command: pulls image and creates a test container if image is absent.

## UCP installation

Read node IP:

```bash
ifconfig -a eth0
```

Pull:

```bash
docker image pull docker/ucp:latest
```

Install pattern from source:

```bash
docker container run --rm -it --name ucp   -v /var/run/docker.sock:/var/run/docker.sock   docker/ucp:latest install   --host-address <manager-ip>   --interactive
```

Risk: HIGH — installs enterprise control plane and modifies Swarm/cluster state.

Acceptance in source:
- installation completes all steps;
- UCP UI becomes reachable;
- manager node shows Ready.

Rollback: `[Needs confirmation]`.

## Worker join

UCP generates a command equivalent to:

```bash
docker swarm join --token <worker-token> <manager-ip>:2377
```

Risk: changes cluster membership.

Security:
- `<worker-token>` is secret material;
- never commit the real token.

Verification: UCP shows worker joined / Ready.

Rollback command is not shown as part of this chapter workflow: `[Needs confirmation]`.

## DTR installation

Source uses a UCP-generated installer based on:

```bash
docker run -it --rm docker/dtr install   --dtr-external-url <dtr-host>   --ucp-node <dtr-node>   --ucp-username <admin-user>   --ucp-url https://<ucp-host>   <source-lab-tls-option>
```

The source lab disables TLS verification. The literal insecure flag is intentionally not promoted as a reusable command.

Risk: HIGH — registry/control-plane installation and trust configuration.

Credentials/admin password are interactive/sensitive.

## Client Bundle

Source downloads a UCP-generated client bundle, copies it to a node and unpacks it.

```bash
unzip <ucp-client-bundle>.zip
```

Then source runs the bundle's environment script before using Docker CLI.

The exact shell invocation is not reconstructed because the retrieved chunk says to run `env.sh` but does not expose a clean complete command line.

Verification:

```bash
docker version --format '{{ .Server.Version }}'
echo "$DOCKER_HOST"
echo "$DOCKER_CERT_PATH"
echo "$DOCKER_TLS_VERIFY"
```

Security:
- private key inside bundle is credential material;
- protect file permissions and storage.

## Push image to DTR

```bash
docker pull busybox:latest
docker tag busybox:latest <dtr>/<user>/<repo>:busybox
docker login --username <user> <dtr>
docker push <dtr>/<user>/<repo>:busybox
```

Effects:
- pulls image;
- creates local tag;
- authenticates to registry;
- pushes image.

Avoid passing password directly on command line unless source explicitly requires it; source shows username only and interactive authentication.

## Old-image scan experiment

```bash
docker pull busybox:1.25.1
docker tag busybox:1.25.1 <dtr>/<user>/<repo>:busybox_old
docker push <dtr>/<user>/<repo>:busybox_old
```

Source-era result: DTR scan reports multiple critical/major vulnerabilities.

Important: exact vulnerability counts are source-era scan output, not a current assertion.

## CVE database

Source UI actions:
- enable scanning;
- enable online synchronization;
- trigger manual scan;
- optionally enable scan-on-push.

Offline update mechanism: upload/install a tar-file containing CVE database updates.

No clean CLI command for CVE database update is present in chapter RAG.

## RBAC

RBAC setup is shown primarily through UCP UI, not CLI.

Source workflow:

```text
Create user
→ create organization
→ create team
→ add user to team
→ create collection
→ create custom role
→ create grant:
   subject + resource set + role
```

No equivalent complete CLI sequence is present in retrieved chapter text: `[Needs confirmation]`.

## Safety boundary

- Historical Docker EE repository/install steps may no longer be valid.
- Do not reuse source subscription URLs, public IPs, join tokens, admin credentials or client keys.
- Disabling TLS verification weakens trust validation.
- Mounting `/var/run/docker.sock` grants installer deep control of the Docker host.
- Package removal, UCP/DTR install and Swarm membership changes are disruptive.
- A current implementation requires separate official-documentation verification.
