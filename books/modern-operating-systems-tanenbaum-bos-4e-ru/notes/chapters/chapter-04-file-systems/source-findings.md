# Source findings — Chapter 4

## [Source code mismatch] Read-only open flag spelling

Relevant provenance:

- PDF page 312 / chunk `p0312:c01`, listing 4.1:
  `open(argv[1], O_RDONLY)`
- PDF page 337 / chunk `p0337:c01`, VFS example:
  `open("/usr/include/unistd.h",ORDONLY)`

The tokens differ inside the same chapter.

Handling:

- no external/model-memory correction was used;
- the mismatch is preserved here;
- `commands.md` identifies the listing 4.1 spelling when describing that exact source code and does not silently claim the two tokens are equivalent.

No other material source contradiction was established from the retrieved chapter RAG.
