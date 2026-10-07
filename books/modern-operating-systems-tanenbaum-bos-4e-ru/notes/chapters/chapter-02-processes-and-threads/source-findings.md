# Source findings — Chapter 2

## [Source extraction issue] Mojibake in figure 2.19 labels

Provenance: PDF page 178 / chunk `p0178:c01`.

The extracted text for several labels inside figure 2.19 is mojibake (for example sequences such as `Äîáàâëåíèå óçëà`). The surrounding body text and the figure caption remain readable and identify the topic as RCU insertion/removal.

Handling:

- the visual artifacts use only concepts that are readable in surrounding RAG text;
- corrupted figure-label strings are not reconstructed from model memory;
- exact original labels remain `[Needs confirmation]`.

## [Source extraction issue] Pthreads listing string quoting

Provenance: PDF page 135 / chunk `p0135:c01`.

The extracted C listing contains malformed doubled quote characters in `printf` strings, for example a fragment resembling:

`printf("... %d\n"", i);`

This is treated as a text-layer extraction defect. The chapter artifacts use the function names and control-flow meaning from the listing but do not silently repair the literal source code.

No other material source contradiction was classified during this chapter analysis.
