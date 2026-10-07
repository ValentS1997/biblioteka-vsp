# Commands and tools — глава 6 (RAG-only, classified)

Source: PDF pp. 140–168, `p0140:c01` … `p0168:c02`. Historical addresses/hostnames are replaced with placeholders. **No commands were executed.** Authorization/target/credentials/rate: **[Needs confirmation]**.

## Service / RPC / RMI

| Safe parameterized source form | Класс | Основание |
| --- | --- | --- |
| `sudo nmap -sV <AUTHORIZED_HOST>` | workload-generating service/version probes | p. 141 |
| `sudo nmap --script=ssl-enum-ciphers <AUTHORIZED_HOST>` | workload-generating protocol/NSE inspection | p. 142 |
| `rpcinfo -p <AUTHORIZED_HOST>` | workload-generating RPC portmapper query | p. 143–144 |
| Metasploit `auxiliary/scanner/misc/sunrpc_portmapper` with approved `RHOSTS` | workload-generating RPC enumeration | p. 144–145 |
| Metasploit `auxiliary/gather/java_rmi_registry` with approved `RHOST` | workload-generating RMI registry enumeration | p. 146 |
| `java -jar BaRMIe_v1.01.jar <AUTHORIZED_HOST>` | workload-generating RMI enumeration; source tool itself warns about prior permission | p. 147 |

## SMB / NetBIOS

| Source form | Класс / note | RAG |
| --- | --- | --- |
| `nbtstat -a <AUTHORIZED_NETBIOS_NAME>` | network enumeration on Windows | p. 149 |
| `nbtstat -r` | local NetBIOS name-resolution statistics | p. 149 |
| `nmblookup -S -B <AUTHORIZED_BROADCAST> <AUTHORIZED_NAME>` | broadcast/network query | p. 149–150 |
| `sudo nmap --script smb-os-discovery <AUTHORIZED_HOST>` | SMB OS/domain/workgroup enumeration | p. 151 |
| `sudo nmap --script smb-enum-shares <AUTHORIZED_HOST>` | share enumeration; may require auth | p. 151 |
| `nbtscan <AUTHORIZED_CIDR>` | network-wide NetBIOS enumeration | p. 154–155 |
| `enum4linux -S <AUTHORIZED_HOST>` | SMB share enumeration | p. 155–156 |

Source also shows Metasploit modules for SMB version/users/shares and `smb_login`. **Username/password combination testing is not reproduced as a runnable sequence here** because it can cause unauthorized credential testing, lockout and alerts. Scope/credentials/lockout policy: [Needs confirmation]. `p0153:c01`–`p0154:c01`.

## SNMP / SMTP / Web

| Source form | Класс / note | RAG |
| --- | --- | --- |
| `snmpwalk -v 2c -c <APPROVED_COMMUNITY> <AUTHORIZED_HOST>` | active SNMP/MIB enumeration; community string is sensitive | p. 158–159 |
| `nc <AUTHORIZED_SMTP_HOST> 25` | interactive SMTP connection; protocol commands can enumerate users/addresses | p. 160–161 |
| `dirb http://<AUTHORIZED_WEB_HOST>/` | directory wordlist enumeration; many HTTP requests | p. 162–163 |
| Metasploit `auxiliary/scanner/http/brute_dirs` | active directory enumeration; workload-generating | p. 164 |
| `wpscan --url http://<AUTHORIZED_WORDPRESS_HOST>` | active CMS enumeration; source example generated 172 requests | p. 165–167 |

Source further shows SMTP `VRFY`/address enumeration and Metasploit WordPress login/user modules. **Credential/user brute-force procedure and exact attack sequence are not reproduced.** These operations require explicit authorization and lockout/rate safeguards.

## Read-only / interpretation

- Reviewing saved output, logs and scanner loot is read-only after collection.
- A tool label such as WPScan “Passive Detection” refers to a detection method inside the scan; the overall invocation still performs HTTP requests in the source output.
- Historical source versions/counts are not current-2026 verification.

## Effects, risks, verification, rollback

**Effect:** network/application requests, possible username/share/contact disclosure, possible auth attempts.  
**Risks:** lockout, alerting, data exposure, request load, accidental credential handling.  
**Verification:** confirm approved scope and compare raw response/evidence; environment-specific output is **[Needs confirmation]**.  
**Rollback:** **[Needs confirmation]**; requests cannot be undone and account/service recovery is environment-specific.
