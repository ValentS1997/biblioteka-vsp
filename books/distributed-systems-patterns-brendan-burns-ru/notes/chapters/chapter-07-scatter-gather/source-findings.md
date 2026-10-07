# Source findings — глава 7

## Finding 1 — probability expression presentation

Classification: `[Source wording/math mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0131:c01`

Source text states that, with five leaf nodes each having a 1% chance of taking at least two seconds, the probability that one leaf is slow is about 5%.

The parenthetical expression shown is:

~~~text
0.99 × 0.99 × 0.99 × 0.99 × 0.99 = 0.95
~~~

Observation:
- `0.99^5 ≈ 0.95` is the probability that all five leaves stay outside the slow tail;
- the approximately 5% slow-request probability is the complementary probability;
- the chapter's qualitative conclusion about tail amplification remains consistent.

Action:
- preserve the source expression;
- do not rewrite the original source text;
- when explaining the result, distinguish the 95% all-fast probability from its roughly 5% complement.

## Finding 2 — no executable deployment example

Classification: `[Needs confirmation]`

The chapter contains architecture/performance examples but no explicit deployment manifest or command sequence.

Action:
- commands.md records the absence of executable CLI;
- no Kubernetes/load-test/retry/timeout commands are imported from model knowledge.
