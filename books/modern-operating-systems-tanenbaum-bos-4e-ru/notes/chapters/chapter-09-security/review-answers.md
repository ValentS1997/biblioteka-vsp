# Review answers — RAG-grounded

These answers are derived from chapter 9 only. They are not an official publisher answer key. External-site tasks and unsafe implementation exercises are constrained by the chapter's `rag_only` policy and the safety boundary stated in the chapter README.

1. Examples:
   - integrity + availability, no confidentiality: a public software/package mirror whose content must not be altered and should stay online;
   - confidentiality + integrity, low availability: an offline archive of highly sensitive records that can tolerate delayed access;
   - all three: an online banking/accounting service holding private balances and executing transactions.

2. TCB membership depends on whether violating the function can violate the security policy.
   - context switching: **inside TCB**, because register/address-space/privilege separation must be correct;
   - reading a file from disk: the complete filesystem/UI need not be inside, but the enforcement path that checks and performs protected access must be trusted;
   - adding swap: the mechanism that preserves process isolation/confidentiality while swapping is TCB-relevant;
   - playing music: outside TCB;
   - GPS acquisition: outside TCB unless the security policy specifically relies on location confidentiality/authorization.
   
   The chapter's rule is to minimize TCB, not to place all OS functionality inside it.

3. A covert channel is an unintended communication path that transmits information through observable shared state rather than the authorized channel. The fundamental requirement is that the sender can influence some state/timing/resource that the receiver can observe.

4. The same object simply appears in more than one domain row, potentially with different rights. The object itself is not duplicated; the access matrix records separate `(domain, object, rights)` relationships.

5. Nonempty access pairs:
   - 50 objects × 100 domains = 5000;
   - 500 × 2 = 1000;
   - 4450 × 1 = 4450;
   - total = **10,450** pairs.
   
   Full matrix: **5000 × 100 = 500,000 rights cells**.
   
   Sparse ACL: each nonempty entry needs domain ID + rights = **20,900 units**.
   
   Sparse capability lists: each nonempty entry needs object ID + rights = **20,900 units**.
   
   If a representation separately counts table/list headers, small additional metadata is needed, but the dominant comparison is 500,000 vs 20,900.

6. All four operations are object-centric, so ACLs are the natural representation:
   - grant read to everyone: edit one object's ACL;
   - revoke write from everyone: edit one object's ACL;
   - grant write to four users: add four ACL entries;
   - revoke execute from four users: edit/remove four entries.
   
   Capability lists would require locating and editing each affected subject's list.

7. All can be represented by either model in principle, but:
   - everyone except one assistant: ACL is simplest using public/default access plus an exception;
   - two users sharing secret files: both work; capabilities make explicit delegation natural;
   - public files: ACL with a public/default entry is simplest.

8. Effective protection matrix from the supplied UNIX listing:

   | Domain | PPP-Notes | prog1 | project.t | splash.gif |
   |---|---|---|---|---|
   | asw | r | rwx | rw | rw |
   | gmw | rw | rx | rw | — |
   | users | r | rx as “other” for prog1 | rw | — |
   | devel | r as “other” | rx | — | r |

   This normalization treats user rows as effective user access and group rows as the group's rights. UNIX owner/group/other precedence is not a fully general ACL model.

9. Source-equivalent ACL view:
   - `PPP-Notes`: `gmw: rw; users: r; other: r`
   - `prog1`: `asw: rwx; devel: rx; other: rx`
   - `project.t`: `asw: rw; users: rw; other: none`
   - `splash.gif`: `asw: rw; devel: r; other: none`

10. Example impossible in classic owner/group/other rwx: allow group `users` to write `project.t` but explicitly deny write to `gmw`, who is a member of `users`. An ACL can add a user-specific deny/restriction; the basic three-class UNIX mode cannot express that exception.

11. Using Bell–LaPadula (BLP: read down, write up) and Biba (read up, write down):
   - a) P1(L1) writes D(L2): **BLP only**
   - b) P4(L2) reads A(L1): **BLP only**
   - c) P3(L2) reads C(L2): **both**
   - d) P3(L2) writes C(L2): **both**
   - e) P2(L1) reads D(L2): **Biba only**
   - f) P5(L3) writes F(L3): **both**
   - g) P6(L3) reads E(L3): **both**
   - h) P4(L2) writes E(L3): **BLP only**
   - i) P3(L2) reads F(L3): **Biba only**

12. Yes. A capability can be attenuated repeatedly: the friend asks the server for another capability containing a subset of the rights already present. Rights can be removed, not recreated or increased by attenuation.

13. No, if the arrow is B → object 1 and therefore represents a write from a higher level to a lower object. It violates the Bell–LaPadula * property: **no write down**.

14. Process-to-process messages must obey the same information-flow direction as writes. Process B may send information only to a process at the same or higher security level, not to a lower-level process. Exact process labels/levels visible only in figure 9.9 remain **[Needs confirmation]**.

15. One hidden bit replaces the least-significant bit of each 8-bit R/G/B component. The visible image effectively retains 7 bits of original precision per component: 256 levels become 128 per channel, so the underlying exact color resolution is reduced by a factor of (2^3 = 8), although the visual change is usually hard to notice.

16. **[Needs confirmation]**. The source gives only the ciphertext plus the statement that it is a Lewis Carroll quotation. No plaintext or cryptanalysis key is present in RAG, and no external cryptogram source/solver is used under `rag_only`.

17. All (26^2 = 676) plaintext digraphs must map one-to-one onto 676 distinct ciphertext digraphs; otherwise decryption is ambiguous. The table is therefore a permutation of all digraphs. Number of keys: **676!**.

18. A key is a permutation of the n byte positions, so the keyspace contains **n!** keys. For large n this can exceed a simple monoalphabetic keyspace and it works on arbitrary byte values, not just letters. However, it preserves the frequency of individual byte values, so it does not eliminate statistical leakage.

19. Use the trusted third party as a key-distribution center. It generates a fresh session key K and sends K to the sender encrypted under their shared key and separately to the receiver encrypted under the receiver's shared key. Both then possess K without sending it in plaintext.

20. A source-consistent approximate example is multiplication of two large primes: computing the product is easy, while recovering the factors from a very large product is much harder. The chapter uses this asymmetry when discussing public-key cryptography.

21. A and B can each establish a private symmetric channel to C by sending a freshly generated local key encrypted with C's public key. C then generates (or accepts) a session key K and returns it to A encrypted under A's temporary key and to B under B's. C is the trusted mediator.

22. Keep the private signing key inside the smart card. The user reviews the document, the system computes a hash, the card signs the hash after local PIN/user authorization, and recipients verify with the certified public key. The main weakness in an Internet café is the untrusted host: it can show one document and send a different hash to the card. A trusted display/reader path is therefore needed for strong assurance.

23. The chapter's scheme stores 3 hidden bits/pixel.
   - hidden compressed payload: (1600×1200×3 / 8 = 720,000) bytes;
   - with ≥50% compression, at least **1,440,000 bytes** of original ASCII text fit;
   - an uncompressed 24-bit image already uses (1600×1200×3 = 5,760,000) bytes, so replacing LSBs does **not increase** its raw size;
   - useful original-text efficiency = (1,440,000 / 5,760,000 = 25%).

24. Digitally sign the hidden message with a private key controlled by the dissident group. Recipients verify the signature using an authenticated public key. Forgers may hide arbitrary text in images, but they cannot create a valid signature without the private key.

25. Under `rag_only`, exact website-only image sizes are **[Needs confirmation]**. The chapter itself states:
   - hidden plays: **Hamlet, King Lear, Macbeth, The Merchant of Venice, Julius Caesar**;
   - original plaintext + short message: **734,891 bytes**;
   - compressed embedded payload: about **274 KB**.
   
   Exact source/result image file sizes require the external demo.

26. Alphabet size = 62. If length is hidden, search space is:
   [
   62^5+62^6+62^7+62^8 = 221,919,436,559,520.
   ]
   If asterisks reveal an actual length L, the space is (62^L). Improvement from hiding length:
   - L=5: **242,235×**
   - L=6: **3907×**
   - L=7: **63.0×**
   - L=8: **1.016×**
   
   Thus length hiding helps most when the actual password is near the minimum length.

27. Publishing the algorithm is not itself a compromise. A sound system must depend on secret passwords/keys, not secrecy of the algorithm. Verify that only the algorithm was disclosed, preserve/rotate secrets if exposure is suspected, and continue with a publicly reviewable scheme.

28. Not against a targeted dictionary attack on one known account. The salt is public, so each password guess can be combined with that user's salt and tested. Salting prevents one precomputed dictionary from being reused efficiently against many salts/accounts.

29. For exhaustive precomputation across all possible salts, work/storage increases by approximately **(2^n)**. This is the anti-precomputation benefit described by the chapter.

30. A useful biometric should:
   - vary enough between different people;
   - remain sufficiently stable over time;
   - be repeatably measurable with low enough false accept/reject rates.
   
   Practical acceptability to users also matters.

31. Two major disadvantages:
   - usability/reliability: more steps, forgotten PINs/lost cards and false biometric rejections increase lockouts and support cost;
   - privacy/attack surface: several credential stores/readers now exist, and biometric compromise is difficult to “rotate.”

32. If every participating kernel is trusted, the scheme can trust the UID assertion as part of the trusted distributed system. If an unprotected student PC can emit arbitrary UID claims, the trust model collapses: it can impersonate another UID to the remote machine.

33. If passwords were used in forward order, observing (f^i(s)) would let an attacker compute all later values by applying f again. Reverse use means an observed current password only derives values that have already expired.

34. MMU hardware can help but cannot generally stop the overflow itself at byte granularity. Page permissions/DEP can prevent execution of injected data, and guard pages can detect some large overflows, but a small stack buffer and adjacent return/data fields normally share a page. Therefore MMU protection is a mitigation, not a complete bounds-checking solution.

35. A stack canary places a value between local buffers and control data; the function checks it before returning and aborts if it changed. High-level bypass classes include learning/leaking the canary, corrupting security-relevant data without crossing the canary, or exploiting corruption outside the protected stack-return path. The chapter's main lesson is that the canary is one layer, not a proof of safety.

36. A filesystem transaction can make “check object identity/rights” and “use/update that same object” one atomic operation, eliminating the attacker-controlled gap. Costs include transaction bookkeeping, locking/contention, possible deadlocks, crash recovery and the difficulty of defining transaction boundaries across ordinary filesystem APIs.

37. Automatic **array-bounds checking** would eliminate a large class of C/C++ memory errors. It is not universal in C because the language and enormous legacy code base assume low-level unchecked pointer/array behavior, while extra checks have compatibility and performance costs.

38. Yes. A Trojan running with legitimate capabilities can misuse exactly those capabilities. Capability protection limits damage to the rights actually held, but does not make authorized code trustworthy.

39. Zeroing before free improves confidentiality by preventing the next user from reading residual data, but adds write I/O and latency. A common design alternative is to zero before reallocation/read exposure rather than on every free, or rely on encryption for some storage layers. The chapter's trade-off is security vs performance.

40. Conceptually, an infecting program can change the program entry path so control reaches the added code first, while preserving enough original entry/state information to continue the legitimate host afterward. This is the architectural idea only; no file-modification recipe is provided here.

41. Predictable track-aligned partition starts make boot metadata locations more regular and may provide predictable nearby sectors/geometry for preserving or relocating boot information. Exact figure/layout details are **[Needs confirmation]**.

42. Conceptually replace the selection predicate in listing 9.2: instead of selecting executable-file candidates, select filenames/source metadata matching C source files (for example the source's C-file naming convention). No infection behavior is added.

43. An analyst can locate the small code path that must execute before the encrypted body becomes usable, then observe or emulate that decryption stage. General polymorphism, instruction substitution and changing decryptor structure make signature matching harder. No evasion recipe or mutation engine is provided here.

44. If the virus compresses the host to hide its added size, the **packer** is needed when creating the infected file: it compresses the original host/body into the stored representation. The unpacker is needed later at runtime to restore the host before it continues.

45. Polymorphism increases size/complexity and processing cost, and the mutation/decryption machinery itself can become a detectable invariant or contain bugs. The chapter explicitly notes that a good mutation engine is difficult to build.

46. Two major errors:
   1. booting the compromised OS before acquiring a trusted backup allows resident malware/rootkits to interfere with observations and backup;
   2. restoring **all** backed-up files can simply restore infected executables/persistence.
   
   Additionally, `fdisk` is not a generic statement of secure disk erasure/formatting.

47. Yes conceptually. A companion program can arrange for a different executable/script with the same command name to be found first by command/path resolution, then optionally invoke the legitimate program. This depends on execution/search-path semantics and does not require modifying the legitimate file.

48. A self-extracting archive is executable code plus payload. Running it means trusting the unpacker before payload inspection is complete. Security therefore depends on provenance/signature verification, sandboxing/least privilege, and validation of extracted paths/content.

49. A rootkit can subvert the very OS interfaces and utilities used to look for it, hiding files, processes, registry/kernel structures or lower-level persistence. Ordinary malware may be visible to a still-trusted kernel/scanner; a rootkit attacks that observation boundary.

50. No. The restore point may already contain the rootkit, and persistence may live outside the restored layer (boot path, firmware or other storage). A compromised host should be recovered from an independently trusted base and then verified.

51. No general perfect detector can decide this for arbitrary programs: malicious behavior is a semantic program property and reduces to undecidable program-behavior questions. Practical scanners therefore use incomplete signatures, heuristics, models and sandboxing.

52. Further restrictions can narrow the already exposed services by source network/address, destination host, direction, time or authenticated gateway, and deny all other traffic by default. The exact original three-service rule set is figure-specific, so concrete addresses/ports are **[Needs confirmation]**.

53. Yes. The check isolates the high-order sandbox prefix by shifting the candidate address right. The desired operation is a **logical right shift filling with zeros**; sign extension can inject ones into the high bits and corrupt the isolated prefix for addresses whose sign bit is set.

54. Browsers/OSes ship with a small set of trusted root CA public keys already installed by the software/vendor distribution channel. That local trust anchor terminates the certificate chain; intermediate CAs are then verified recursively from it.

55. Three source-supported Java safety properties:
   - strong/type-safe language rules;
   - no raw pointer arithmetic/user-managed `malloc/free` style memory;
   - runtime array bounds checks and bytecode/JVM verification/sandbox controls.
   
   These reduce the memory-corruption surface common in C.

56. Conceptual JDK 1.2 policy:
   - code source: `www.appletsRus.com`;
   - permit network/code loading only back to `www.appletsRus.com`;
   - permit read+write on `/usr/tmp/*`;
   - permit read-only on `/usr/me/appletdir/*`;
   - no other filesystem/network rights.
   
   If signer identity is required by policy, add the trusted signer explicitly. Exact JDK policy-file syntax is not reconstructed from model memory.

57. An applet is downloaded and runs inside another host process/runtime under a restricted policy; a normal installed application is normally granted the user's ordinary process privileges. Because an applet's origin is less trusted, the runtime must restrict memory, filesystem, network and system-call behavior.

58. The chapter's learning objective is to demonstrate that observable file/permission/resource state can carry bits even without authorized data access. No operational covert-channel sender/receiver code is provided. A safe classroom substitute is an in-process toy simulation where one thread toggles an in-memory boolean and another samples it, measuring synchronization overhead without crossing a security boundary.

59. External DES download is forbidden by `rag_only`, and credential-verifier/cracking code is not produced. Source-grounded verifier structure is:
   `password + public salt → 25 historical DES-based iterations/derivation → compare stored verifier`.
   The review exercise explicitly requests a **16-bit** salt, while the chapter's UNIX discussion uses **12 bits**.

60. Safe ACL data-model functions:
   - `create_object(o)`: create empty/default ACL;
   - `delete_object(o)`: remove object and ACL;
   - `create_domain(d)`: register domain, no rights by default;
   - `delete_domain(d)`: remove d from every ACL;
   - `grant(d,o,rights)`: add/merge rights;
   - `revoke(d,o,rights)`: subtract rights, remove empty entry;
   - `grant_all(o,rights)`: add a default/public or explicit entries according to policy;
   - `revoke_all(o,rights)`: remove rights from all ACL entries.
   
   Every mutation should preserve a canonical rights set and verify object/domain existence.

61. No exploitable overflow implementation is provided. Safe experiment: write a bounds-checked toy program that copies characters into a fixed-size logical buffer, records when input would exceed 128 bytes, and compares the result with compiler/runtime diagnostics. This demonstrates the boundary failure without overwriting control data.

62. No file-infecting or executable-overwriting virus code is provided. Safe emulator: represent “files” as in-memory byte arrays or disposable non-executable text fixtures and simulate the transformation into a separate output object, never modifying an executable, never auto-running output and never adding propagation logic.
