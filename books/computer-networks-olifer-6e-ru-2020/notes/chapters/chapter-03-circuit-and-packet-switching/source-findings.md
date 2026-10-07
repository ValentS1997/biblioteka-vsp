# Source findings — chapter 3

Scope: PDF pages 75-102.

## 1. [Source extraction issue] mathematical notation on PDF pages 95-100

The extracted text preserves the surrounding explanation and several numerical results, but some formulas lose subscripts, superscripts or variable symbols.

Handling:
- do not silently reconstruct exact notation from model knowledge;
- preserve qualitative relationships supported by the text;
- use numerical results only where the extracted text is unambiguous;
- exact original typography is [Needs confirmation].

## 2. [Source wording / extraction mismatch] message-size notation in the delay example

The extracted formula text renders the message size as `107` bytes, while the following prose explicitly states `10 000 000` bytes and derives an 800 ms serialization time at 100 Mbit/s.

This strongly indicates lost exponent formatting in the extraction, but the artifact does not silently rewrite the original mathematical typography. The source example is therefore summarized by its explicit prose values and final results rather than by reconstructing the damaged equation.

The extracted text explicitly gives:
- distance: 5000 km;
- propagation speed: 200000 km/s;
- link capacity: 100 Mbit/s;
- circuit-switched result: 825 ms;
- packet-switched result: 1856 ms under the stated assumptions.

## 3. Original figures are not multimodal RAG objects

Figures 3.1-3.16 are referenced by extracted text, but their complete geometry is not available as separate multimodal RAG objects.

Chapter diagrams and SVG summaries are newly composed from text evidence and do not reproduce original figures.
