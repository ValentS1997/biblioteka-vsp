# Шпаргалка: SSO, LDAP, Kerberos, sssd, NSS и PAM

## 1. SSO architecture

~~~text
identity store
→ LDAP / Active Directory
→ authentication provider
→ sssd
├─ NSS → identity lookup
└─ PAM → auth/account/session/password
→ login and applications
~~~

Kerberos adds ticket-based authentication. DNS and synchronized time are critical dependencies.

## 2. LDAP mental model

LDAP is a directory service optimized for:
- relatively small information objects;
- frequent reads/searches;
- relatively infrequent writes;
- replication/cache;
- attribute-based records.

Entry:
~~~text
dn: uid=user,ou=People,dc=example,dc=com
objectClass: ...
uid: user
uidNumber: ...
gidNumber: ...
homeDirectory: ...
~~~

Key concepts:
- entry = named attributes + values;
- DN = unique distinguished name;
- objectClass = schema for allowed/required attributes;
- LDIF = textual interchange format.

## 3. LDAP servers in the chapter

OpenLDAP:
- server daemon: slapd;
- server configuration shown with slapd.conf;
- client defaults shown with ldap.conf;
- base/suffix defines root of LDAP namespace.

389 Directory Server:
- multi-master capability;
- AD synchronization support;
- GUI/CLI/web management;
- LDAP + ACI.

## 4. LDAP query

~~~bash
ldapsearch -h <host> -p 389   -x -D "<bind-DN>" -W   -b "<baseDN>" "<filter>"
~~~

Check:
- correct server endpoint;
- correct bind identity;
- correct baseDN;
- filter matches intended entries;
- returned LDIF contains expected attributes.

## 5. Linux + Active Directory

Preconditions from the chapter:
- realmd installed;
- sssd installed;
- ntpd running;
- correct AD domain name;
- account permitted to join hosts.

Change:
~~~bash
sudo realm join --user=<user> <AD-DOMAIN>
~~~

Verify:
~~~bash
realm list
~~~

Rollback: [Needs confirmation].

## 6. Kerberos flow

~~~text
correct DNS + synchronized time
→ realm/KDC configuration
→ kinit
→ ticket cache
→ klist
→ domain join
~~~

Commands:
~~~bash
kinit user@REALM
klist
kdestroy
~~~

klist showing a valid ticket is the chapter's explicit authentication check.

## 7. FreeBSD + AD flow

Before Kerberos:
- FQDN must be in /etc/hosts;
- NTP must work;
- /etc/krb5.conf must map realm/domain/KDC correctly.

Then:
~~~text
kinit → klist → net ads join -U <user>
~~~

Successful join output is the source-supported acceptance signal.

## 8. sssd

sssd centralizes:
- user/identity lookup;
- access/account mapping;
- authentication;
- offline credential caching.

Active Directory example:
~~~text
services = nss, pam
id_provider = ad
access_provider = ad
~~~

LDAP example:
~~~text
services = nss, pam
id_provider = ldap
auth_provider = ldap
ldap_uri = ...
ldap_user_search_base = ...
tls_reqcert = demand
ldap_tls_cacert = ...
~~~

Security rule from the chapter: LDAP authentication through sssd must use an encrypted channel; certificate validation is part of the example.

## 9. NSS

nsswitch.conf controls lookup source order.

Chapter example:
~~~text
passwd: files sss
group:  files sss
shadow: files sss
~~~

Interpretation:
1. local files first;
2. sssd-backed directory second.

Verify:
~~~bash
getent passwd
~~~

## 10. PAM module types

| Type | Role |
|---|---|
| auth | identifies/authenticates user |
| account | checks account conditions |
| session | actions around session start/end |
| password | changes/collects authentication data |

Module order matters.

## 11. PAM control flags

| Flag | Meaning in chapter |
|---|---|
| include | include another config file |
| optional | result normally not decisive |
| required | failure makes final stack fail, but processing continues |
| requisite | failure immediately stops stack |
| sufficient | success can stop stack, unless an earlier required module already failed |

Do not edit PAM rules casually: a control-flow mistake can deny login.

## 12. PAM + sssd example logic

~~~text
auth
→ local checks
→ pam_unix2
→ pam_sss if needed

account
→ validate local/directory account state

password
→ password-quality check
→ update local or sssd-backed credentials

session
→ loginuid / limits / logging / environment/session actions
~~~

Successful stack returns control to login.

## 13. Legacy alternatives

NIS:
- historical centralized account database;
- chapter advises against using it for new systems because of security and scalability limitations.

rsync:
~~~bash
rsync -gopt -e ssh /etc/passwd /etc/shadow <host>:/etc
~~~

Pros described:
- sends only differences where possible;
- preserves metadata.

Critical risk:
- shown design depends on passwordless SSH execution;
- chapter explicitly calls this a security-policy violation.

## 14. Read-only verification order

When troubleshooting SSO integration:

~~~text
1. DNS / time prerequisites
2. LDAP query or Kerberos ticket test
3. domain membership check
4. sssd provider configuration
5. NSS lookup with getent passwd
6. PAM stack behavior
~~~

Do not jump directly to PAM edits before upstream identity/authentication paths are verified.

## 15. Rollback boundary

Source-supported rollback-like action:
- kdestroy removes the current Kerberos ticket.

Not source-supported as universal rollback:
- leaving an AD domain;
- reverting sssd.conf;
- reverting nsswitch.conf;
- restoring PAM stack;
- reverting rsync-distributed passwd/shadow.

Those remain [Needs confirmation].
