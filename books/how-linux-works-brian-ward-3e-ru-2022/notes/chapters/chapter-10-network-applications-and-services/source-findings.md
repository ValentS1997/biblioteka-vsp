# Source findings — глава 10 «Сетевые приложения и службы»

**Scope:** `p0320:c01`–`p0343:c01`, PDF/печатные страницы 320–343. Политика **rag_only**: source variants are preserved; external documentation/model memory are not used to silently repair them.

## F-01 — [Source wording issue]: `QUICK` in HTTP protocol note

- **Locator:** `p0321:c01`, §10.1.
- Source says HTTP/1.1 is old and names newer protocols as **HTTP/2, QUICK and developing HTTP/3**.
- The token `QUICK` is preserved as the literal source wording.
- **Decision:** do not normalize it to another protocol name without external verification. Intended term: **[Needs confirmation]**.

## F-02 — [Source inconsistency / edition context]: SSH host-key algorithms

- **Locator A:** `p0326:c01`, `sshd_config` example includes:
  - `ssh_host_rsa_key`;
  - `ssh_host_ecdsa_key`;
  - `ssh_host_ed25519_key`.
- **Locator B:** `p0327:c01` states that SSH version 2 has RSA and DSA keys, gives a table only for RSA/DSA, and shows `ssh-keygen` examples for those two types.
- **Issue:** the chapter itself presents different algorithm sets in adjacent discussion.
- **Decision:** artifacts preserve both source forms and do not promote the RSA/DSA generation examples as universal/current best practice. Actual host-key policy: **[Needs confirmation]**.

## F-03 — [Source extraction issue]: malformed dash in tar/SSH pipeline

- **Locator:** `p0329:c01`, §10.3.4.
- Extracted command contains `tar zcvf – dir | ssh remote_host tar zxvf -`.
- The character between `zcvf` and `dir` is rendered as a long dash rather than an unambiguous ASCII hyphen.
- **Impact:** this line is not safe to treat as a copy-paste executable command.
- **Decision:** `commands.md` records the pipeline concept but does not silently normalize the ambiguous token.

## F-04 — [Source extraction/wording issue]: malformed lsof service filter example

- **Locator:** `p0333:c01`, §10.5.1.
- Source text says service names from `/etc/services` can be used “как в `-tcp:ssh`”.
- Nearby explicit valid-looking forms are `lsof -iTCP:443`, `lsof -iTCP -sTCP:LISTEN`, `-i4`, `-i6`.
- **Decision:** `-tcp:ssh` is preserved here but omitted from executable examples. Exact intended syntax: **[Needs confirmation]**.

## F-05 — [Source extraction issue]: original socket figure unavailable

- **Locator:** `p0342:c01`, fig. 10.1 — one method of accepting and handling incoming connections.
- `rag/manifest.yaml` states that images/diagrams are not independently encoded as multimodal RAG objects.
- **Decision:** Mermaid/SVG artifacts reconstruct only the text-confirmed listener → `accept()` → connected socket → worker/fork relationship. Exact original geometry/labels remain **[Needs confirmation]**.

## F-06 — [Source chronology / applicability boundary]: historical networking tools

The chapter discusses `inetd`, `xinetd`, TCP wrappers, `netstat`, DSA host keys, older SSH/FTP/telnet-era tooling and several dated security resources.

- These are legitimate source contents for the 2022 Russian edition.
- **Decision:** artifacts distinguish “source-described mechanism” from “current target-system recommendation”. Current package availability, algorithm policy and service framework remain **[Needs confirmation]**.

## Current-system applicability

Hostnames, ports, usernames, SSH key files, listener addresses, service names, rpcbind exposure, firewall behavior and Unix-socket paths in examples are source context, not live-host facts. Values for a real system remain **[Needs confirmation]**.
