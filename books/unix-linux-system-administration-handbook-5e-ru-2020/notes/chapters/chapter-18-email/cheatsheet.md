# Шпаргалка: электронная почта, SMTP и MTA

## 1. Mail flow

~~~text
MUA
→ MSA :587
→ MTA
→ SMTP :25
→ remote MTA
→ DA/LDA
→ message store
→ IMAPS / POP3S
→ recipient MUA
~~~

Roles:
- MUA — compose/read;
- MSA — authenticated submission;
- MTA — transport/routing;
- DA/LDA — local delivery;
- message store — mbox/Maildir/database-like storage;
- access agent — IMAP/POP access.

## 2. Message anatomy

~~~text
envelope
headers
body
~~~

Envelope and visible From/To are not the same thing.

Useful headers:
- Received — transport hops;
- Return-Path — envelope sender-related information;
- Authentication-Results / Received-SPF — authentication/policy results.

Read Received lines from bottom upward to reconstruct path, but remember that header data can be forged.

## 3. SMTP sequence

~~~text
EHLO or HELO
MAIL FROM:<sender>
RCPT TO:<recipient>
DATA
<message>
.
QUIT
~~~

Other commands in the chapter:
- VRFY;
- EXPN;
- RSET;
- HELP.

Manual diagnostics:
~~~bash
telnet <mail-host> 25
telnet <submission-host> 587
~~~

This can become a real delivery attempt once MAIL/RCPT/DATA are used.

## 4. SMTP status codes

~~~text
2xx → success
4xx → temporary failure / retry
5xx → permanent failure
~~~

Extended DSN:
~~~text
X.X.X
~~~

Examples in the chapter distinguish mailbox problems, routing problems and policy rejection.

## 5. Submission security

MSA usually listens on 587, MTA on 25.

Submission should use:
- authentication;
- encrypted transport.

Without correct relay/authentication controls, a mail server can become an open relay.

## 6. Spam / sender identity

Spoofing is easy. Do not treat visible From as proof of identity.

SPF:
- publishes authorized outgoing mail servers in DNS;
- forwarding can cause false failures;
- be cautious about hard decisions based only on SPF failure.

DKIM:
- signs mail cryptographically;
- publishes domain keys/policy through DNS;
- verifies origin/domain association and message integrity as described in the chapter.

## 7. Confidentiality

Transport encryption:
- TLS/STARTTLS protects a transport hop;
- next hop may be unencrypted.

Message/content encryption:
- PGP/GPG;
- S/MIME;
- centralized encryption solutions.

User access:
- prefer IMAPS / POP3S so credentials are not sent in clear text.

## 8. Aliases

Common uses:
- role addresses;
- forwarding;
- mailing lists;
- multiple names for a user.

After editing aliases:
~~~bash
newaliases
~~~

Security-sensitive alias targets:
- files;
- programs.

Alias loops can cause repeated forwarding/bounces.

## 9. sendmail

Configuration chain:
~~~text
host.mc
→ m4
→ host.cf
→ /etc/mail/sendmail.cf
~~~

Read-only checks:
~~~bash
sendmail -d0.1 -bt < /dev/null
sendmail -bv <address>
mailq
mailq -Aa
~~~

Queue processing:
~~~bash
sendmail -q
sendmail -q -v
~~~

sendmail reads its config at start. After changing sendmail.cf, it must be restarted or receive HUP.

## 10. sendmail queues

Typical queues:
- /var/spool/mqueue;
- /var/spool/clientmqueue.

Risks:
- filesystem fill;
- stuck/deferred messages;
- queue/logs in same filesystem increase blast radius.

Use mailq to inspect queue IDs, age, sender/recipient and deferred reason.

## 11. Exim

Core operational commands from the chapter:

~~~bash
exim -bv
exim -bp
exim -bt <address>
exim -q
~~~

Supporting tools:
- exigrep;
- eximstats;
- exiqgrep;
- exiqsumm;
- exiwhat.

Config concepts:
- routers determine address handling;
- transports perform delivery;
- retry controls repeated attempts;
- rewrite changes addresses;
- ACL/local scan provide filtering/control points.

## 12. Postfix architecture

Postfix is split into specialized processes.

Important queues:
- incoming;
- active;
- deferred;
- hold;
- corrupt.

Configuration:
- main.cf — main parameters;
- master.cf — services/processes.

Delivery components include smtp, lmtp, local, virtual and pipe.

## 13. Postfix inspection

~~~bash
postconf
postconf <parameter>
postconf -d <parameter>
postconf -n
postconf -m
~~~

Lookup tables:

~~~bash
sudo postmap hash:/etc/postfix/access
postmap -q <key> hash:/etc/postfix/access
~~~

Queue:

~~~bash
mailq
sudo qshape deferred
~~~

Debugging principle from the chapter:
- find the queue ID;
- follow that ID through log records;
- inspect the queue when delivery is delayed.

## 14. Postfix access control

Examples in the chapter use:
- permit_mynetworks;
- permit_sasl_authenticated;
- reject_unauth_destination;
- client/recipient access tables.

SMTP AUTH should be combined with encrypted transport when credentials are used.

## 15. soft_bounce

During Postfix testing:

~~~text
soft_bounce = yes
~~~

Benefit:
- permanent failures become temporary;
- delivery keeps retrying, reducing risk of losing valid mail while testing.

Risk:
- leaving it enabled causes rejected mail to retry indefinitely.

Disable after testing.

## 16. Cross-layer troubleshooting order

~~~text
1. inspect message headers / queue ID
2. inspect SMTP response
3. inspect queue
4. inspect MTA logs
5. verify DNS MX and network/firewall path
6. inspect routing / aliases / lookup tables
7. inspect local delivery/store
~~~

Do not change MTA configuration before establishing which layer is failing.

## 17. Rollback boundary

Source-supported reversal:
- Postfix soft_bounce test mode should be disabled after testing.

Not universally specified by the chapter:
- restoring sendmail config;
- restoring Exim config;
- restoring Postfix config;
- undoing a submitted SMTP message;
- undoing alias changes.

These remain [Needs confirmation].
