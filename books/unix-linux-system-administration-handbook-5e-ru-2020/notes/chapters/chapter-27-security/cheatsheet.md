# Шпаргалка: Security

## 1. CIA triad

~~~text
Confidentiality → кто может читать
Integrity       → что можно доверять
Availability    → когда сервис/данные доступны
~~~

Security is a process, not a product.

## 2. Threat surface

Основные sources:
- social engineering/phishing;
- software vulnerabilities;
- DDoS;
- insiders;
- configuration errors.

Human training is a security control.

## 3. Hardening order

~~~text
inventory
→ patch
→ remove unnecessary services
→ least privilege
→ filtering
→ MFA
→ central logging
→ backups
→ monitoring
~~~

## 4. Least privilege

Применять к:
- users;
- file permissions;
- daemons;
- firewall rules;
- service accounts;
- automation.

Less privilege → smaller blast radius.

## 5. Defense in depth

Do not rely only on:
- perimeter firewall;
- antivirus;
- VPN;
- one authentication factor;
- one IDS.

Combine layers.

## 6. Attack-surface reduction

Read-only discovery:
~~~bash
netstat -an | grep LISTEN
sudo lsof -i :22
~~~

Then:
~~~text
port
→ owning process
→ required?
→ disable/remove if not required
→ verify exposure gone
~~~

## 7. Patch discipline

Maintain:
- inventory;
- recurring schedule;
- test plan;
- rollback plan;
- vendor/security advisories.

Avoid ad-hoc patching without change control.

## 8. Remote logging

Central logs:
- aggregate events;
- support alerts/correlation;
- preserve evidence if local host is compromised.

## 9. Backups

Backups are part of availability.

Protect them:
- access control;
- encryption;
- safe/off-network storage.

A backup is itself sensitive data.

## 10. Rootkit response

Detection examples:
- OSSEC;
- AIDE;
- chkrootkit.

If trust in host is lost:
~~~text
preserve data/evidence
→ rebuild from clean baseline
~~~

Do not assume in-place cleanup restores trust.

## 11. Firewall principle

~~~text
default deny
→ open only required services
→ DMZ for Internet-facing systems
→ host-level controls too
~~~

Egress filtering can reduce post-compromise reach.

## 12. MFA

Chapter's minimum target:
- VPN administrative access;
- SSH administrative access;
- administrative web portals.

Password-only authentication is insufficient for high-privilege Internet-facing access.

## 13. Password model

Prefer:
- long unique passphrases;
- no reuse;
- password vault;
- individual accounts;
- strong controls for privileged identities.

Avoid:
- shared accounts;
- no-password accounts;
- reused credentials.

## 14. Password aging

Linux:
~~~bash
sudo chage -m 2 -M 90 -E 2017-07-31 -W 14 ben
~~~

FreeBSD example:
~~~bash
sudo pw user mod trent -p 2017-09-25 -e 90
~~~

These modify policy. Verify intended values before applying.

## 15. Security scans

Authorized network scan:
~~~bash
nmap -sT <authorized-host>
sudo nmap -sV -O <authorized-host>
~~~

Never scan a third-party network without permission.

## 16. Password audit

Authorized only:
~~~bash
sudo ./john /etc/shadow
~~~

Recovered passwords are secrets:
- restrict output;
- remediate weak passwords;
- delete audit output afterward.

## 17. HIDS/NIDS roles

NIDS:
- Bro;
- Snort.

HIDS:
- OSSEC.

OSSEC can:
- detect rootkits;
- monitor file integrity;
- analyze logs;
- alert;
- perform active response.

## 18. Fail2Ban

~~~text
logs
→ repeated suspicious events
→ temporary source blocking / notification
~~~

## 19. Crypto primitives

Symmetric:
- shared secret;
- efficient bulk encryption.

Public-key:
- public/private pair;
- key exchange/signatures.

Hash:
- fixed-length integrity representation.

PKI:
- CA signs identity/key binding.

## 20. Hash guidance in chapter

Preferred:
- SHA-2;
- SHA-3.

Avoid for cryptographic trust:
- SHA-1;
- MD5.

Integrity example:
~~~bash
sha256sum /etc/ssh/sshd_config
~~~

## 21. Randomness

Use kernel entropy:
~~~text
/dev/random
/dev/urandom
~~~

Do not invent user-space cryptographic PRNG logic.

## 22. TLS / PKI

~~~text
private key
→ CSR
→ CA verification/signature
→ certificate
→ TLS endpoint
~~~

Track certificate expiry.

## 23. OpenSSL

Private key:
~~~bash
openssl genrsa -out admin.com.key 2048
~~~

CSR:
~~~bash
openssl req -new -sha256 -key admin.com.key -out admin.com.csr
~~~

Inspect:
~~~bash
openssl x509 -noout -text -in <cert.pem>
~~~

TLS debug:
~~~bash
openssl s_client -connect <host>:443
~~~

## 24. SSH trust chain

First connection:
~~~text
server host key
→ fingerprint
→ verify through trusted channel
→ known_hosts
~~~

Blind acceptance creates MITM risk.

## 25. SSH key permissions

~~~text
~/.ssh             0700
private key        0600
public key         0644
authorized_keys    0600
~~~

Never share private key.

## 26. Key generation

~~~bash
ssh-keygen -t ecdsa -b 384
~~~

Privileged key:
- use passphrase.

Automation without passphrase:
- restrict server-side account privileges.

## 27. ssh-agent

~~~bash
ssh-add ~/.ssh/id_ecdsa
ssh-add -l
ssh-add -d ~/.ssh/id_ecdsa
ssh-add -D
~~~

Agent forwarding extends trust to remote host.

## 28. Port forwarding

~~~bash
ssh -L 8000:webserver:80 server.admin.com
~~~

Useful, but can bypass network policy.

Server control:
~~~text
AllowTCPForwarding no
~~~

## 29. sshd hardening themes

Chapter example includes:
- AllowUsers / AllowGroups;
- public-key auth;
- PasswordAuthentication no;
- PermitRootLogin no;
- MaxAuthTries reduction;
- X11 forwarding off if unused;
- verbose failed-login logging.

Do not copy fixed config blindly; validate against required access paths.

## 30. Reload boundary

~~~bash
sudo systemctl reload sshd
~~~

Before reload:
- keep known-good admin session;
- preserve previous config.

After reload:
- open a new test session;
- only then close old session.

## 31. SSHFP

~~~text
trusted host key
→ SSHFP DNS record
→ client verification
~~~

Source-supported commands:
~~~bash
sshfp server.admin.com
dig server.admin.com. IN SSHFP | grep SSHFP
ssh -o VerifyHostKeyDNS=yes <host>
~~~

## 32. Firewalls

Firewall is not a complete security architecture.

Use:
~~~text
perimeter filtering
+ DMZ
+ host hardening
+ monitoring
+ user training
~~~

## 33. VPN

VPN protects path, not endpoint.

Treat VPN-connected endpoint as external unless trust is explicitly established.

## 34. Standards

Chapter surveys:
- ISO/IEC 27001;
- PCI DSS;
- NIST SP 800;
- Common Criteria;
- OWASP;
- CIS benchmarks.

Pick a recognized methodology and apply it consistently.

## 35. Incident response

~~~text
detect
→ stay controlled
→ define response team
→ preserve evidence
→ assess impact
→ isolate if needed
→ close gaps
→ develop recovery plan
→ communicate
→ recover
→ report
~~~

Do not destroy evidence through premature remediation.

## 36. Recovery criterion

After compromise:
- known-good backup/image/config;
- rotated compromised credentials;
- closed root cause;
- restored monitoring/logging;
- validated service state.

Exact recovery without trustworthy baseline:
[Needs confirmation].
