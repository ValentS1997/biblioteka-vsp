# Source findings — chapter 3

Scope: PDF pages 75-102.

## 1. [Source extraction issue] mathematical notation on PDF pages 95-100

The extracted text preserves the surrounding explanation and several numerical results, but some formulas lose subscripts, superscripts or variable symbols. Examples include the propagation/serialization formulas and packet-delay expressions.

Handling:
- do not silently reconstruct exact notation from model knowledge;
- preserve qualitative relationships supported by the text;
- use numerical results only where the extracted text is unambiguous;
- exact original typography is [Needs confirmation].

## 2. Numerical comparison remains partially usable

The extracted text explicitly gives the example inputs and final results:
- message size: 10^7 bytes as represented in source text;
- distance: 5000 km;
- propagation speed: 200000 km/s;
- link capacity: 100 Mbit/s;
- circuit-switched result: 825 ms;
- packet-switched result: 1856 ms under the stated packetization/switch assumptions.

Because notation in intermediate formulas is extraction-damaged, artifacts treat this as an illustrative source example rather than independently recomputing every equation.

## 3. Original figures are not multimodal RAG objects

Figures 3.1-3.16 are referenced by extracted text, but their complete geometry is not available as separate multimodal RAG objects.

Chapter diagrams and SVG summaries are newly composed from text evidence and do not reproduce original figures.
