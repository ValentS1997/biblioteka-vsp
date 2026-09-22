# Диаграмма: логика главы 8

```mermaid
flowchart TD
    start["Asset / service / communication needs protection"] --> goals{"Какое security property требуется?"}

    goals --> cia["Confidentiality / Integrity / Availability"]
    goals --> identity["Authentication / Nonrepudiation"]

    cia --> threat["Threat model: reconnaissance / interception / spoofing / disruption"]
    identity --> threat

    threat --> principles["Design principles: simplicity / fail-safe defaults / complete mediation / least privilege"]

    principles --> controls{"Какой класс control?"}
    controls --> network["Firewall / IDS / IPS"]
    controls --> crypto["Cryptographic primitives"]
    controls --> auth["Authentication protocols"]

    crypto --> symmetric["Symmetric: AES + modes"]
    crypto --> publickey["Public-key: RSA / elliptic-curve context"]
    crypto --> hash["Hashes / digital signatures"]

    publickey --> keymgmt["Certificates / CA / chain of trust"]
    hash --> keymgmt
    auth --> freshness["Nonce / timestamp / replay resistance"]
    auth --> kdc["KDC / Kerberos / Diffie-Hellman / public-key auth"]

    network --> channel["Secure connections"]
    keymgmt --> channel
    freshness --> channel
    channel --> ipsec["IPsec / VPN"]
    channel --> wifi["802.11i / WPA2"]
    channel --> apps["Application security"]

    apps --> mail["PGP"]
    apps --> web["DNSSEC / SSL-TLS / browser sandboxing"]

    start --> observe["Authorized observation: traceroute / tcpdump / Wireshark"]
    apps --> social["Privacy / anonymity / censorship / steganography / DRM"]
```

Диаграмма отражает центральную логику главы: security goals → threat model → principles/controls → cryptography/key management/authentication → защищенные соединения и application security.
