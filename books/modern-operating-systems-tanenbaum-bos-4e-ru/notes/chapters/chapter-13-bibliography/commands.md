# Source-confirmed follow-up reading actions

Scope: Chapter 13 RAG only, PDF pages 1110–1119.

This chapter contains bibliographic guidance rather than operating-system commands. The canonical `commands.md` artifact therefore records actionable reading/research operations supported by the source.

| Need | Source-grounded next action | Acceptance check |
|---|---|---|
| refresh general OS concepts | choose Silberschatz et al. or Stallings | selected source covers the missing concept |
| learn UNIX/POSIX programming | use Stevens and/or the POSIX standard | API semantics come from a source intended for that purpose |
| deepen concurrency knowledge | use Arpaci-Dusseau, Andrews & Schneider, Ben-Ari or related scheduling papers | target topic is processes, synchronization or scheduling |
| deepen VM knowledge | use Denning, Knuth or Arpaci-Dusseau | working sets/replacement/allocation topic is explicitly covered |
| deepen filesystem knowledge | use McKusick et al. or the filesystem chapters in broad texts | source matches implementation/performance need |
| deepen storage/I/O knowledge | use the I/O/storage papers listed in 13.1.5 | source matches disk/storage/power/interrupt topic |
| investigate deadlock | use Coffman, Holt, Isloor & Marsland, Levine or Shub | source targets deadlock theory/modeling |
| study virtualization/cloud | use Portnoy, Erl et al., Rosenblum & Garfinkel or Whitaker et al. | distinction between tutorial/cloud architecture/VMM research is clear |
| study multicore/multiprocessor issues | use Dubois, Kumar, Zhuravlev and related listed works | focus is synchronization, heterogeneity or resource contention |
| study security | begin with Anderson or choose a narrower source by attack/defense topic | source type matches systems/security question |
| inspect Linux internals | use Bovet & Cesati or Maxwell | goal is implementation rather than only API use |
| inspect Windows internals | use Russinovich & Solomon | goal is internal algorithms/data structures |
| study system design | use Saltzer & Kaashoek, Brooks, Corbató, Lampson or Wirth | focus is design principles/experience |

## Verification rule

A bibliographic recommendation is considered source-grounded only if the title/author appears in Chapter 13. Edition freshness, current availability and modern relevance are **not** assumed under `rag_only`.

## External lookup boundary

Section 13.2 points to the publisher website for the detailed alphabetical bibliography. That resource is external to the canonical PDF and is not automatically imported into this artifact set.
