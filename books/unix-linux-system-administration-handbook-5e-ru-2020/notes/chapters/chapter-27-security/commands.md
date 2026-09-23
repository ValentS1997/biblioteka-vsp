# Команды главы 27

Только команды и формы команд, подтверждённые RAG главы 27. Security-sensitive operations должны выполняться только на собственных системах или при явном разрешении владельца.

## Read-only / observation

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| netstat -an \| grep LISTEN | Показать listening sockets в примере FreeBSD | unexpected TCP/UDP exposure | read-only |
| sudo lsof -i :22 | Найти process, связанный с port 22 | expected sshd/listener and sessions | read-only |
| ssh server.admin.com | Открыть SSH connection | host-key fingerprint and expected server | workload-generating |
| ssh server.admin.com "df -h /var/log" | Выполнить удалённую read-only command | exit status/output | workload-generating |
| ssh -v server.admin.com | SSH diagnostic logging | authentication/connection failure point | workload-generating |
| ssh -h | Краткая справка ssh | supported options | read-only |
| ssh-add -l | Показать keys loaded in agent | expected identities only | read-only |
| ls -l ~/.ssh/cm_socket/ | Проверить ControlMaster socket | expected socket/owner | read-only |
| dig server.admin.com. IN SSHFP \| grep SSHFP | Проверить DNS SSHFP records | expected fingerprints | read-only |
| openssl x509 -noout -text -in <certificate.pem> | Просмотреть certificate | subject, issuer, validity, algorithms | read-only |
| openssl s_client -connect <host>:443 | Inspect/debug TLS session | certificate/verify result/protocol/cipher | workload-generating |
| sha256 /etc/ssh/sshd_config | FreeBSD example: SHA-256 file hash | compare expected integrity value | read-only |
| sha256sum /etc/ssh/sshd_config | Linux example: SHA-256 file hash | compare expected integrity value | read-only |

## Active security scans — authorization required

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| nmap -sT <authorized-host> | TCP connect scan | externally visible open ports/services | workload-generating |
| sudo nmap -sV -O <authorized-host> | Service/version and OS fingerprinting | unexpected service/version/exposure | workload-generating |

Boundary:
- chapter explicitly says never scan someone else's network without administrator permission;
- use only against systems/networks you own or are authorized to test;
- scans may trigger IDS/alerts and policy controls.

## Password/account policy changes

Linux example, OCR-normalized where option letters are unambiguous:

~~~bash
sudo chage -m 2 -M 90 -E 2017-07-31 -W 14 ben
~~~

Effect:
- changes password-aging/account-expiry policy for user.

Type:
- state-changing.

Verification:
- exact read-only verification command is not provided by the chapter: [Needs confirmation].

FreeBSD example:

~~~bash
sudo pw user mod trent -p 2017-09-25 -e 90
~~~

Effect:
- modifies password/account aging parameters in the chapter example.

Type:
- state-changing.

Rollback:
- restore previous account-policy values;
- exact source-supported rollback command: [Needs confirmation].

## Password audit — sensitive

Chapter example:

~~~bash
sudo ./john /etc/shadow
~~~

Purpose:
- authorized audit for weak passwords.

Type:
- workload-generating / security-sensitive.

Requirements:
- management approval before use;
- output may contain recovered passwords;
- protect output and delete it after audit.

Chapter says the same tool can be run with -show to view recovered passwords; exact full command line is not repeated here because secret exposure is the purpose of that mode.

## OSSEC HIDS

Start manager:

~~~bash
sudo /var/ossec/bin/ossec-control start
~~~

Register/manage agents:

~~~bash
sudo /var/ossec/bin/manage_agents
~~~

On agent:

~~~bash
sudo /var/ossec/bin/manage_agents
~~~

Type:
- state-changing.

Effect:
- starts HIDS manager and manages authenticated agent enrollment.

Verification:
- expected agent appears in manager list/menu;
- alerts should reflect configured monitoring.

Rollback:
- exact source-supported stop/removal command sequence: [Needs confirmation].

## OpenSSL / PKI

Generate 2048-bit RSA private key:

~~~bash
openssl genrsa -out admin.com.key 2048
~~~

Type:
- state-changing: creates sensitive private-key file.

Security:
- private key must remain secret;
- filesystem protection/backup procedure: [Needs confirmation] if not otherwise defined by local policy.

Create CSR:

~~~bash
openssl req -new -sha256 -key admin.com.key -out admin.com.csr
~~~

Type:
- state-changing: creates CSR.

Inspect certificate:

~~~bash
openssl x509 -noout -text -in google.com.pem
~~~

Type:
- read-only.

Debug TLS:

~~~bash
openssl s_client -connect google.com:443
~~~

Type:
- workload-generating/read-only remote handshake.

## SSH public-key authentication

Create ECDSA keypair from chapter example:

~~~bash
ssh-keygen -t ecdsa -b 384
~~~

Alternative chapter-supported form:
- RSA with 2048 or 4096 bits.

Type:
- state-changing: creates key files.

Security:
- privileged-account keys should use a passphrase;
- never share private key.

Use explicit identity:

~~~bash
ssh -i ~/.ssh/id_ecdsa hsolo@server.admin.com
~~~

Type:
- workload-generating.

Expected permissions:
~~~text
~/.ssh                 0700
private key            0600
public key             0644
authorized_keys        0600
~~~

## Provision authorized_keys

Chapter example, normalized to standard home-directory notation:

~~~bash
mkdir -p ~hsolo/.ssh
chmod 0700 ~hsolo/.ssh
cat /tmp/hsolo.pub >> ~hsolo/.ssh/authorized_keys
chmod 0600 ~hsolo/.ssh/authorized_keys
~~~

Type:
- state-changing.

Precondition:
- verify user account and supplied public key identity.

Verification:
- authenticated SSH login succeeds using intended key;
- password/root access policy remains as designed.

Rollback:
- remove only the newly added authorized key;
- exact command not supplied by chapter: [Needs confirmation].

## ssh-agent

Load key:

~~~bash
ssh-add ~/.ssh/id_ecdsa
~~~

List keys:

~~~bash
ssh-add -l
~~~

Remove one key:

~~~bash
ssh-add -d ~/.ssh/id_ecdsa
~~~

Remove all loaded keys:

~~~bash
ssh-add -D
~~~

Recover public key from private key if needed:

~~~bash
ssh-keygen -yf "$key" > "$key.pub"
~~~

Agent forwarding:
~~~bash
ssh -A <trusted-host>
~~~

Risk:
- any party controlling the forwarding host can use forwarded identities on your behalf;
- use only on trusted systems.

## SSH host aliases / policy

Chapter shows client configuration in ~/.ssh/config, including:
- PasswordAuthentication;
- Host / HostName;
- User;
- IdentityFile;
- ForwardAgent;
- Port;
- ServerAliveInterval;
- ControlMaster / ControlPath / ControlPersist.

Insecure diagnostic/example command from chapter:

~~~bash
ssh -o StrictHostKeyChecking=no server.admin.com
~~~

Do not use as a default security recommendation: it disables an authenticity check and increases MITM exposure.

## SSH local port forwarding

Chapter example:

~~~bash
ssh -L 8000:webserver:80 server.admin.com
~~~

Effect:
- forwards local TCP port 8000 through SSH server to webserver:80.

Type:
- state-changing to effective network reachability / workload-generating.

Risk:
- can intentionally or accidentally bypass firewall/network policy;
- use only where policy explicitly permits.

Server-side control:
~~~text
AllowTCPForwarding no
~~~

## Reload sshd

Source-supported forms:

~~~bash
sudo kill -HUP $(sudo cat /var/run/sshd.pid)
~~~

Linux alternative:

~~~bash
sudo systemctl reload sshd
~~~

Effect:
- reloads sshd configuration for new connections;
- existing sessions remain under previous settings.

Type:
- state-changing.

Precondition:
- keep a known-good administrative session open;
- validate intended sshd_config changes by review;
- exact source-supported syntax-test command is not provided: [Needs confirmation].

Rollback:
- restore previous sshd_config;
- reload sshd;
- verify new test login before closing known-good session.

## SSHFP

Generate record from trusted source:

~~~bash
sshfp server.admin.com
~~~

Verify DNS record:

~~~bash
dig server.admin.com. IN SSHFP | grep SSHFP
~~~

Client use:
~~~bash
ssh -o VerifyHostKeyDNS=yes <host>
~~~

Boundary:
- SSHFP is only as trustworthy as the key source and DNS trust model.

## File transfer

~~~bash
scp ./file server.admin.com:
scp server.admin.com:file ./file
scp server1.admin.com:file server2.admin.com:file
~~~

Type:
- state-changing: copies/overwrites files.

Precondition:
- verify destination path and host identity.

Rollback:
- depends on previous destination content/backup: [Needs confirmation].

## Firewall/VPN scope

Chapter names iptables, ufw and ipfw and discusses IPsec/VPN principles, but does not provide exact executable firewall or IPsec configuration commands in this section.

Do not invent firewall/VPN command lines.

## Incident response

Chapter provides a process rather than shell commands:
- preserve evidence/logs;
- back up systems;
- assess impact;
- isolate compromised hosts where appropriate;
- close discovered gaps;
- plan recovery;
- communicate;
- execute recovery;
- report as required.

Destructive remediation before evidence collection is an anti-pattern.
