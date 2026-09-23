# Шпаргалка: DNS и BIND

## 1. Resolution path

~~~text
application
→ resolver library
→ nsswitch.conf source order
→ recursive server from resolv.conf
→ cache?
   ├─ yes → answer
   └─ no  → root → TLD → delegated authoritative server
→ resource record answer
~~~

DNS query = name + record type. Response = resource records, referral or error.

## 2. Client configuration

/etc/resolv.conf:
- search — domains appended to incomplete names;
- nameserver — recursive DNS servers, queried in order.

/etc/nsswitch.conf controls whether files or dns is consulted first.

## 3. Namespace

- root = .;
- FQDN ends with a dot inside DNS syntax;
- forward lookup: name → address/data;
- IPv4 reverse lookup: address → in-addr.arpa → PTR.

Missing a final dot in a zone file can make an intended absolute name relative to the current origin.

## 4. Server roles

~~~text
authoritative
  master → reads official zone file
  slave  → obtains zone via transfer
  stub   → copies NS data only

non-authoritative
  caching → answers from cache

recursive
  follows referrals for client

nonrecursive
  returns answer or referral
~~~

Internet-facing authoritative servers should not provide unrestricted recursion.

## 5. Delegation and cache

Delegation moves responsibility down the DNS tree. A recursive server follows referrals until it reaches authoritative data.

Cache lifetime is controlled by TTL. Longer TTL reduces query traffic but makes changes persist longer in remote caches; shorter TTL increases query load.

## 6. Query tools

~~~bash
dig <name> <type>
dig @<server> <name> <type>
dig +trace <name>
dig -x <address>
dig +norecurse @<server> <name> NS
drill -T <name>
~~~

Also present: nslookup, host, delv.

Interpretation:
- ANSWER → requested data returned;
- AUTHORITY without answer → referral/authority information;
- aa → authoritative answer;
- ad → authenticated DNSSEC data;
- NXDOMAIN → requested name does not exist;
- SERVFAIL → server-side resolution/validation/configuration failure context.

## 7. Zone-file structure

Parser directives:
- $ORIGIN;
- $INCLUDE;
- $TTL;
- $GENERATE — BIND-specific.

Generic RR:

~~~text
[name] [ttl] [class] type data
~~~

## 8. Core records

| RR | Meaning |
|---|---|
| SOA | zone definition / authority metadata |
| NS | zone name servers / delegation |
| A | IPv4 address |
| AAAA | IPv6 address |
| PTR | reverse mapping |
| MX | mail exchanger |
| CNAME | alias → canonical name |
| SRV | service location |
| TXT | arbitrary text / supporting metadata |
| DS / DNSKEY | DNSSEC key linkage |
| RRSIG | DNSSEC signature |
| NSEC / NSEC3 | authenticated denial support |

## 9. BIND model

~~~text
named.conf
= server policy + role + zones + ACL + logging + controls + views

zone files
= DNS data

named
= DNS server daemon

rndc
= live control channel
~~~

## 10. Split DNS

view can return different zone data to different clients.

Typical pattern from the chapter:

~~~text
internal view
→ match internal networks
→ recursion yes
→ private/internal data

external view
→ match any
→ recursion no
→ public data only
~~~

Views are evaluated in order; more restricted views must come first.

## 11. Static-zone update

~~~text
edit master zone
→ increment SOA serial
→ rndc reload
→ dig @master ...
→ dig @slave ...
~~~

Do not edit slave-maintained files.

If address/name mapping changes, update forward and reverse zones as applicable.

## 12. Zone transfer

- AXFR = full zone;
- IXFR = incremental changes;
- transfer uses TCP port 53 in the described model;
- slave compares SOA serial to determine whether data changed.

Restrict allow-transfer to legitimate slave/measurement systems as appropriate.

## 13. Dynamic updates

Dynamic zones maintain a journal zone.jnl.

Manual edit:

~~~bash
rndc freeze <zone>
# edit
rndc thaw <zone>
~~~

Dynamic update:

~~~bash
nsupdate -k <keydir>:<keyfile>
~~~

Prefer authenticated updates; the chapter rejects source-IP trust as sufficient protection.

## 14. Access controls

Relevant BIND controls:
- allow-query;
- allow-recursion;
- allow-transfer;
- allow-update;
- update-policy;
- blackhole;
- ACL definitions.

Open recursive resolvers can be abused for unauthorized resource use and amplification attacks.

## 15. TSIG

TSIG uses a shared secret for authenticated server-to-server operations.

Chapter use cases:
- protect zone transfers;
- protect dynamic updates.

It is positioned for limited numbers of communicating server pairs rather than global trust.

## 16. DNSSEC

~~~text
ZSK → signs zone RRsets
KSK → signs/anchors key material
DNSKEY → publishes public key
DS → parent links child key into trust chain
RRSIG → signature
NSEC/NSEC3 → authenticated denial
~~~

Typical source flow:

~~~text
dnssec-keygen
→ publish keys
→ dnssec-signzone
→ serve signed zone
→ chain trust through parent DS
~~~

Expired signatures can cause validating clients to fail name resolution.

## 17. Debugging BIND

Three families in the chapter:
- logging;
- rndc;
- query tools.

Useful commands:

~~~bash
rndc status
rndc trace
rndc notrace
rndc querylog
rndc reload
rndc reconfig
~~~

named -d2 enables debug level 2; the debug file can grow quickly.

## 18. Lame delegation

Symptoms:
- parent delegates to a server;
- that server is not authoritative for the delegated zone;
- clients become slower; complete failure is possible if all delegated servers are lame.

Check each advertised server directly:

~~~bash
dig @<server> <zone> NS
dig +norecurse @<server> <zone> NS
~~~

## 19. Acceptance boundary

Source-supported verification after a zone/config change:
- query the intended server directly with dig @server;
- verify local and remote data where the chapter calls for both;
- check slave propagation;
- inspect logs;
- check rndc status;
- for DNSSEC, trace signatures/trust with drill or delv.

Universal rollback for arbitrary BIND configuration changes: [Needs confirmation].
