# Source findings — Chapter 9

## [Source extraction issue] Figure-internal text on PDF page 720 is mojibake

- PDF page 720 / chunk `p0720:c01`.
- Figure 9.21 labels are extracted as corrupted Cyrillic mojibake.
- The surrounding prose and caption remain readable.

Handling: do not reconstruct the corrupted figure labels from model memory. Figure-dependent details use surrounding prose only.

## [Source extraction issue] TOCTOU code tokens are damaged in the text layer

- PDF page 724 / chunk `p0724:c01`.
- The extracted code contains forms such as `W OK`, `O WRONLY` and `user input`, where token boundaries/underscores are not trustworthy.

Handling: conceptual artifacts preserve the check/use lesson but do not silently normalize damaged source tokens into current C constants.

## [Needs confirmation] Review question 25 requires an external website

- PDF page 779 / chunk `p0779:c01`.
- The exercise explicitly asks the reader to visit the author's website and extract the hidden Shakespeare plays.
- Chapter policy is `rag_only`.

Handling: no web fallback is used. Values already stated by chapter prose may be cited; website-only answers remain `[Needs confirmation]`.

## [Source contradiction / parameter variation] Salt size

- PDF page 698 / chunk `p0698:c01`: the UNIX example states `n = 12` salt bits.
- PDF page 783 / chunk `p0783:c01`: review question 59 explicitly asks for a 16-bit salt.

Handling: preserve both. The review exercise is treated as a requested variant rather than silently rewritten to 12 bits.

## [Needs confirmation] Review question 59 requires external DES implementation

The question instructs the reader to download DES from the Internet. External sources are forbidden by `rag_only`; no implementation is fetched.

## [Safety boundary] Review questions 58–62 include operational security exercises

Q58 asks for a covert-channel sender/receiver, Q59 for password-verifier code, Q61 for buffer-overflow experimentation and Q62 for an executable-file-overwriting virus simulation.

Handling: answers preserve the learning objective but use non-deployable, defensive/toy descriptions. No credential-cracking, exploit or file-infecting malware code is produced.
