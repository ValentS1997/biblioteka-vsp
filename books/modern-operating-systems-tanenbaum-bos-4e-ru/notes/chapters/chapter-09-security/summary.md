# Chapter-end summary

Provenance: PDF pages 775–776; chunks `p0775:c01` and `p0776:c01`.

The chapter's explicit conclusions are:

- Operating systems must protect valuable and confidential data.
- System security is generally easier to achieve when the trusted computing base is small.
- Resource access can be modeled as a sparse access matrix:
  - by columns as ACLs;
  - by rows as capability lists.
- Formal information-flow models can restrict data movement, but covert channels may still leak information.
- Cryptography protects secrecy and authenticity; symmetric and public-key approaches make different key-distribution/performance trade-offs.
- Hashes, signatures and certificates can authenticate digital information.
- Authentication may rely on something the user knows, has or is; stronger systems can combine factors.
- Many implementation defects can be exploited: buffer overflow, format-string misuse, dangling pointers, NULL dereference, integer overflow, command injection and TOCTOU.
- Insider attacks include logic bombs, backdoors and counterfeit login paths.
- Malware includes trojans, viruses, worms, spyware and rootkits; compromised machines may become remotely controlled zombies.
- The preferred defensive strategy is defense in depth using multiple independent technologies such as firewalls, malware scanners, signed code, confinement, intrusion detection and mobile-code containment.
