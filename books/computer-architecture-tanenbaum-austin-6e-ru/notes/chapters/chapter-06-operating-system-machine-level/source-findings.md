# Source findings — глава 6

Policy: **rag_only**. Findings are recorded without silent correction.

## SF-01 — Windows version naming is inconsistent inside chapter material

**Classification:** [Source terminology/version drift]

**Provenance:** TOC `p0011:c01`; chapter pages including `p0537:c01`–`p0547:c01`.

The table of contents labels the examples section as UNIX and **Windows XP**, while chapter prose and API discussion repeatedly refer to **Windows 7**. Some paragraphs still use Windows XP wording while adjacent text describes Windows 7.

**Handling:** artifacts use “Windows 7” when directly following the chapter's main running example and otherwise describe this as historical Windows material. No external modernization is applied.

## SF-02 — exercise 33 references figure 6.27, while the relevant directory/link example is figure 6.29

**Classification:** [Source cross-reference mismatch]

**Provenance:** exercise `p0553:c01`; directory/link material `p0532:c01`–`p0534:c01`.

Exercise 33 asks about:

```text
unlink("/usr/ast/bin/game3")
```

“in the context of figure 6.27”.

The exact same path/link scenario is described around **figure 6.29**: `/usr/ast/bin/game3` and `/usr/jim/jotto` are links to the same file, and the chapter explicitly explains what the unlink does.

**Handling:** review answer 33 follows the explicit link/unlink prose, while preserving the figure-number mismatch here.

## SF-03 — listing 6.1 contains code/text extraction irregularities

**Classification:** [Source code/extraction issue]

**Provenance:** `p0512:c01`.

Examples include forms such as `return(O)`, `new producer )`, `MAX__PRIME`, and spacing irregularities in field references.

**Handling:** artifacts use the algorithmic producer/consumer behavior, not these snippets as copy/paste-safe Java.

## SF-04 — exercise 38 is experimentally underspecified for numeric results

**Classification:** [Source task underspecification]

**Provenance:** `p0554:c01`.

The exercise asks to simulate LRU/FIFO over 64 virtual pages and report results for generated address traces, but the number of physical frames and the exact trace-generation parameters are not fixed in the exercise text.

**Handling:** review answer gives the simulator design and leaves numeric performance results **[Needs confirmation]** rather than inventing experiment parameters.

## Adjudication status

No direct page-image inspection or external documentation is used under the current chapter contract.
