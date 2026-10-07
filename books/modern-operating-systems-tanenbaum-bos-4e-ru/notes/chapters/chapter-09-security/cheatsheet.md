# Chapter 9 cheatsheet — Безопасность

## Symptom / problem framing

| Observation | First security question |
|---|---|
| unauthorized read | confidentiality / access-control failure |
| unauthorized modification | integrity / privilege failure |
| service unusable | availability / resource exhaustion |
| valid credentials, wrong privilege | authorization/domain error |
| privilege obtained through input | memory safety / injection / TOCTOU |
| secret leaks despite ACLs | covert channel or trusted-component compromise |
| malware keeps returning after reboot | persistence/rootkit/firmware boundary |
| signed code rejected/accepted incorrectly | key/certificate trust chain |
| revocation seems ineffective | cached/open handle or capability semantics |

## Baseline / context

### CIA

- Confidentiality: unauthorized parties cannot read.
- Integrity: unauthorized parties cannot alter/delete/inject.
- Availability: authorized users can obtain service.

### Trust hierarchy

```text
security policy
  ↓
TCB / reference monitor
  ↓
authentication
  ↓
authorization model
  ↓
implementation / APIs
  ↓
defense-in-depth controls
```

A larger TCB contains more code that must be correct.

## Read-only checks

1. Identify the asset and required CIA properties.
2. Identify attacker class/capability.
3. Define the authorization domain currently executing.
4. Enumerate the minimum required rights (POLA).
5. Inspect ACL/capability state for the exact object.
6. Determine whether access was already opened before revocation.
7. Separate pathname checks from descriptor/object checks.
8. For secret leakage, inspect ordinary channels and shared-state/covert channels.
9. For credentials, determine whether stored material is plaintext, unsalted derived data, salted derived data or one-time/challenge-response state.
10. For memory corruption, identify whether bounds/type/lifetime/integer validation failed.
11. Check whether independent mitigations are present: canary, non-executable data, ASLR.
12. For malware, identify persistence layer: user files, executable image, boot path, kernel/rootkit, firmware.
13. For recovered hosts, verify trust from known-good media rather than relying only on the compromised OS.
14. For mobile code, identify interpreter/VM permissions and code-signing policy.

## Interpretation

### ACL vs capabilities

| Representation | Indexed by | Strong operation |
|---|---|---|
| ACL | object | “who can access this object?”; global revocation from one object |
| Capability list | subject/domain | “what can this domain access?”; delegation/least-authority workflows |

### Bell–LaPadula vs Biba

| Model | Read | Write | Goal |
|---|---|---|---|
| Bell–LaPadula | same or lower | same or higher | confidentiality |
| Biba | same or higher | same or lower | integrity |

They intentionally point information flow in opposite directions.

### Covert channel

A covert channel exists when two parties can influence/observe shared state even though the normal policy forbids direct communication. Examples in the chapter use locks, resource availability, file existence and timing.

### Password storage

`password + salt → one-way derivation → stored verifier`

The salt is public; its purpose is to destroy the usefulness of one precomputed dictionary across many accounts.

### Lamport chain

```text
secret s → f(s) → f²(s) → ... → fⁿ(s)

server starts with fⁿ⁺¹(s)
client reveals values in reverse order
```

An intercepted current value only lets the attacker compute already-used values.

### Memory-safety defenses

- Canary: detect overwrite before return.
- DEP/NX: data pages are not executable.
- ASLR: make useful addresses unpredictable.
- Type/bounds/lifetime safety: prevent corruption before mitigations are needed.

No single layer is sufficient.

### TOCTOU

Unsafe shape:

`check(path) → attacker changes path target → privileged open(path)`

Safer source idea:

`open object → inspect same descriptor/object with fstat → operate on same descriptor`

### Malware recovery

Rootkit compromise weakens trust in local observations. A rollback/checkpoint can also restore the rootkit if the persistence existed at checkpoint time or outside that software layer.

## Next action

For a suspected compromise:

`identify violated property → freeze evidence/read-only state → determine trust boundary → contain → recover from known-good source → rotate affected credentials/keys → verify controls`.

## Modifying action

State-changing operations in the chapter include:

- changing ACL/capability rights;
- switching protection domains;
- changing authentication secrets;
- enabling/disabling services through firewall policy;
- revoking or replacing keys/certificates;
- restoring/reinstalling a system;
- applying sandbox/jail/mobile-code permissions.

For real systems, exact platform commands are outside this RAG-only chapter and remain `[Needs confirmation]`.

## Verification / acceptance checks

- unauthorized principal can no longer read/modify the object;
- legitimate principal retains required access;
- revoked access does not persist through an already-open handle unless explicitly intended;
- authentication replay no longer succeeds;
- trusted verifier/certificate chain anchors in a known local root;
- recovered host is validated independently of the formerly compromised runtime;
- defense layers fail independently rather than sharing one bypass;
- logs/IDS do not substitute for preventive access control.

## Rollback

- ACL/policy changes: restore previous documented policy if access is over-restricted.
- Credential/key rotation: previous secrets should not normally be re-enabled after suspected compromise.
- Firewall changes: restore prior rule set only after validating the old rule was not part of the incident.
- Reinstallation/recovery: rollback is backup/image dependent — `[Needs confirmation]`.
