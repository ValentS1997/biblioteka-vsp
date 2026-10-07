# Review questions — source extract

Provenance: chapter-end questions/exercises, PDF pages 776–783, chunks `p0776:c01 … p0783:c01`.

Numbering follows the source. Long wording is structurally condensed without changing the requested task.

1. Give examples of applications requiring: integrity+availability but not confidentiality; confidentiality+integrity but low availability; all three CIA properties.

2. Which of these functions must be inside the TCB and which may be outside: process context switch, reading a disk file, adding swap space, playing music, obtaining smartphone GPS coordinates?

3. What is a covert channel, and what fundamental condition allows one to exist?

4. In an access-control matrix, what happens when one object is needed in two domains?

5. For 5000 objects and 100 domains: 1% of objects accessible in all domains, 10% in two domains, 89% in one. One storage unit is required for a rights value, object ID or domain ID. Compare full matrix, ACL and capability-list storage.

6. Which access-matrix implementation is preferable for: grant read to everyone; revoke write from everyone; grant write to four named users; revoke execute from four named users?

7. Can ACLs, capabilities or both solve: everyone except one assistant can read; two users share secret files; some files are public?

8. Convert the supplied UNIX owner/group/rwx listing for four files into a four-domain × four-object protection matrix.

9. Convert the same UNIX permissions into ACLs.

10. Modify one ACL to express an access grant/revocation impossible in ordinary UNIX owner/group/other rwx.

11. With levels 1–3, classify nine reads/writes under Bell–LaPadula, Biba or both.

12. In the Amoeba capability scheme, may a friend further reduce rights on an already reduced capability and delegate the new capability?

13. In figure 9.9, may an arrow from process B to object 1 be added? If not, what rule would it violate?

14. If process-to-process messages are allowed in the figure 9.9 model, what information-flow rules apply to messages from process B?

15. In the RGB steganography model, explain what happens to color resolution when the low bit of each R/G/B component carries hidden data.

16. Break the supplied monoalphabetic cipher containing a Lewis Carroll quotation.

17. A secret-key cipher maps every plaintext digraph to a ciphertext digraph using a 26×26 table. What constraints must the table satisfy and how many keys exist?

18. A block transposition cipher permutes n byte positions. How many keys exist and what advantages does this have over monoalphabetic substitution?

19. Sender and receiver have never met, but each shares a different secret key with a trusted third party. How can they establish a new shared session key?

20. Give a simple mathematical function that approximately illustrates a one-way function.

21. A and B trust a third party C with a known public key but have no shared secret. How can A and B establish a new shared secret?

22. Design a smart-card-based digital-signature workflow suitable for use from Internet cafés; assess its security.

23. A 1600×1200 RGB image hides one bit in each component. Natural-language ASCII compresses by at least 50%. How much source text can be hidden, how much does image size increase, and what is useful-data efficiency?

24. A repressive government sends forged steganographic messages to discredit dissidents. How can recipients distinguish authentic hidden messages?

25. Visit the author's steganography demo and determine original/result image sizes, hidden plays and hidden byte count.

26. Passwords use upper/lowercase letters and digits, length 5–8. How much security is gained by displaying nothing instead of one asterisk per typed character, which reveals length?

27. The password-encryption algorithm used by a new UNIX installation is published. What should the administrator do?

28. Does Morris–Thompson salting protect against targeted guessing of the privileged user's password when the password file is readable?

29. With an n-bit salt, how much more work is required to crack all passwords than without salt?

30. Name three properties of a good biometric characteristic.

31. Give two disadvantages of an authentication procedure combining password, card+PIN and fingerprint.

32. Evaluate a historical `rexec machine4 who` scheme that trusts the UID asserted by the source kernel. What changes if one machine is an unprotected student PC?

33. Why does Lamport one-time authentication use the hash chain in reverse order?

34. Can MMU hardware realistically prevent the buffer-overflow attack of figure 9.21? Explain.

35. Explain stack canaries and high-level ways an attacker might bypass the protection.

36. How could filesystem transactions prevent TOCTOU races, and what problems might transactions introduce?

37. Name a C-compiler/language feature that could close many security holes. Why is it not universally used?

38. Can a Trojan horse still be effective in a capability-protected system?

39. Should the OS erase every disk block before returning it to the free list? Discuss security and performance.

40. At a conceptual level, how can a parasitic virus run before its host program and later return control to the host?

41. Why can track-aligned partition starts simplify life for a boot-sector virus?

42. Modify listing 9.2 conceptually so it selects C source files rather than executable files.

43. For an encrypted virus, how can an antivirus analyst identify the decryptor/key area, and what general techniques make that analysis harder?

44. Why does a packed-virus design need a packer as well as an unpacker?

45. Give one disadvantage of a polymorphic encrypted virus from the malware author's perspective.

46. Identify two serious mistakes in the proposed recovery sequence: boot infected OS, back up all files, use fdisk to “format,” reinstall OS, restore all files.

47. Can companion viruses exist on UNIX without modifying existing files? Explain conceptually.

48. Discuss security implications of self-extracting software archives.

49. Why are rootkits unusually difficult to detect compared with ordinary viruses/worms?

50. Can a rootkit-infected machine always be restored safely by reverting software to an earlier system restore point?

51. Could a general program take another arbitrary program as input and always decide whether it contains a virus?

52. Propose additional firewall rules that further restrict access to the three externally exposed services in the chapter example.

53. In the program of figure 9.33b, does it matter whether right shift fills with zeros or sign bits? Which behavior is preferable?

54. How can a browser bootstrap certificate verification if verifying one CA key appears to require another CA key indefinitely?

55. Give three properties that make Java safer than C for untrusted/mobile code.

56. For JDK 1.2, define permissions allowing an applet from `www.appletsRus.com` to load more code from that site, read/write `/usr/tmp/`, and read `/usr/me/appletdir/`.

57. How do applets differ from ordinary applications, and how does that affect security?

58. Write sender/receiver programs for a UNIX covert channel and measure throughput under idle and loaded conditions.

59. Download DES, implement the historical 25-iteration UNIX password verifier, and create ten Morris–Thompson-style password records using a 16-bit salt.

60. Design ACL maintenance functions for object/domain create/delete, grant/revoke one domain, and grant/revoke all domains.

61. Implement the section 9.7.1 buffer-overflow example and experiment with input lengths.

62. Implement a harmless emulator of the overwriting-virus structure from section 9.9.2 using a disposable executable file.
