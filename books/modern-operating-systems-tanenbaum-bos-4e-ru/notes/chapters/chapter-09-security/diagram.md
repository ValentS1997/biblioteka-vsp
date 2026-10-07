# Chapter 9 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Asset / security requirement"] --> B{"Which property?"}
    B --> C["Confidentiality"]
    B --> I["Integrity"]
    B --> V["Availability"]

    C --> P["Protection policy"]
    I --> P
    V --> P

    P --> T["Small TCB / reference monitor"]
    T --> AU["Authentication"]
    AU --> AZ["Authorization"]
    AZ --> AZ1["Domains / POLA"]
    AZ --> AZ2["ACL"]
    AZ --> AZ3["Capabilities"]
    AZ --> M["Formal information-flow model"]
    M --> M1["Bell-LaPadula"]
    M --> M2["Biba"]
    M --> M3["Covert-channel check"]

    AU --> CR["Crypto / key protection"]
    CR --> CR1["symmetric"]
    CR --> CR2["public key"]
    CR --> CR3["hash / signature"]
    CR --> CR4["salt / OTP / challenge-response"]

    T --> IMPL["Implementation correctness"]
    IMPL --> E1["bounds / type / lifetime"]
    IMPL --> E2["integer / format / injection"]
    IMPL --> E3["TOCTOU"]
    E1 --> MIT["canary + DEP + ASLR"]
    E2 --> MIT
    E3 --> MIT

    MIT --> MAL["Malware / persistence"]
    MAL --> MAL1["trojan / virus / worm"]
    MAL --> MAL2["spyware / rootkit"]
    MAL --> DEF["Defense in depth"]
    DEF --> D1["firewall / AV"]
    DEF --> D2["signed code"]
    DEF --> D3["jail / IDS"]
    DEF --> D4["mobile-code sandbox / Java safety"]
```

## Diagnostic boundary

```text
authentication ≠ authorization
encryption ≠ integrity
formal policy ≠ bug-free implementation
malware deletion ≠ restored trust
one defense layer ≠ defense in depth
```
