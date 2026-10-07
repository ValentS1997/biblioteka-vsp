# Source-confirmed security-related operations and APIs

Scope: chapter 9 RAG only, PDF pages 659–783.

| Item | Class | Source-grounded role | Safety / verification |
|---|---|---|---|
| `read` / `write` | state-changing | Rights associated with protected objects/domains | Verify subject has the required right. |
| `open` | state-changing | Creates an access relationship/file descriptor | ACL revocation may not affect an already-open file. |
| `access(path,...)` | read-only | Checks pathname access using real credentials in TOCTOU example | Source explicitly shows why check-then-open is unsafe. |
| `fstat(fd,...)` | read-only | Check metadata/permissions on the already-open object | Safer than re-resolving a mutable pathname in the source example. |
| `malloc` / `free` | state-changing | Heap lifetime example for dangling-pointer errors | Use-after-free is a correctness/security defect. |
| `printf("%s", s)` | workload-generating | Safe formatting pattern shown before the unsafe format-string variant | Keep untrusted data out of the format string. |
| `system(cmd)` | state-changing | Shell-command execution used in command-injection example | Do not construct from untrusted input; source example is explicitly unsafe. |
| `CTRL+ALT+DEL` | state-changing | Trusted attention sequence in the chapter's Windows login example | Used to escape a counterfeit login program. |
| `rexec machine4 who` | workload-generating | Review example of remote execution trusting a remote UID assertion | Safe only if every asserting kernel is trusted; historical example. |
| `nmap` | read-only | Mentioned as a port-scanning tool while discussing attack reconnaissance | No operational scan procedure is included here. |
| `fdisk` | state-changing | Appears in a deliberately flawed malware-recovery exercise | Destructive; do not use as a generic “format disk” instruction. |

## Source defensive API lesson: TOCTOU

The chapter contrasts pathname check/use with acting on one already-open descriptor:

```text
open target → inspect same object/descriptor → write same descriptor
```

The point is object identity, not a particular modern API recipe.

## Unsafe source examples

The chapter contains intentionally vulnerable examples using unchecked input, untrusted format strings, shell construction and executable-file infection. They are retained in source provenance but are not reproduced here as executable attack recipes.

## Safety boundary

No current firewall, password-cracking, exploitation, malware deployment or rootkit commands are added from model memory. Exact platform procedures remain `[Needs confirmation]`.
