# Диаграмма: SSO identity, authentication и login flow

~~~mermaid
flowchart TD
    A["User / application needs identity or login"] --> B{"What is needed?"}

    B -->|Identity attributes| C["NSS lookup"]
    C --> C1["nsswitch.conf"]
    C1 --> C2["files first"]
    C1 --> C3["sss"]
    C3 --> D["sssd"]

    B -->|Authentication / account / session| E["PAM stack"]
    E --> E1["auth"]
    E --> E2["account"]
    E --> E3["session"]
    E --> E4["password"]
    E --> D

    D --> F{"Provider"}
    F -->|LDAP| G["LDAP / Active Directory directory"]
    F -->|Kerberos| H["Kerberos realm / KDC"]
    F -->|AD provider| I["Active Directory"]

    G --> G1["LDAP entries / DN / objectClass / LDIF"]
    H --> H1["Ticket-based authentication"]
    H1 --> H2["DNS + synchronized time required"]

    J["Read-only checks"] --> J1["ldapsearch"]
    J --> J2["realm list"]
    J --> J3["klist"]
    J --> J4["getent passwd"]

    K["Linux AD join"] --> K1["Verify realmd + sssd + ntpd + domain + credentials"]
    K1 --> K2["realm join"]
    K2 --> K3["realm list"]
    K3 --> D

    L["FreeBSD AD path"] --> L1["Verify FQDN + NTP"]
    L1 --> L2["Configure krb5.conf"]
    L2 --> L3["kinit"]
    L3 --> L4["klist"]
    L4 --> L5["net ads join"]
    L5 --> D

    M["PAM safety"] --> M1["Order matters"]
    M --> M2["required != requisite != sufficient"]
    M2 --> M3["Bad stack can deny login"]

    N["Legacy alternatives"] --> N1["NIS: not for new systems"]
    N --> N2["rsync passwd/shadow"]
    N2 --> N3["Passwordless SSH risk"]

    O["Rollback boundary"] --> O1["kdestroy removes local ticket"]
    O --> O2["Domain/NSS/PAM rollback: [Needs confirmation]"]
~~~

## Смысл диаграммы

SSO в главе — это не один сервис, а цепочка identity lookup и authentication. sssd связывает directory/authentication providers с двумя системными интерфейсами: NSS для поиска учетных данных и PAM для login/auth/account/session/password policy. Kerberos требует корректных DNS и времени, а PAM-изменения находятся в самом чувствительном участке цепочки.
