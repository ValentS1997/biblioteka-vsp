# Source findings — Chapter 7

## [Source extraction issue] Figure-internal text is mojibake in multiple chunks

The RAG text layer contains corrupted figure-internal labels on several pages, while the surrounding prose and captions remain readable.

Examples:
- PDF page 534 / chunk `p0534:c01`: figure 7.1 labels;
- PDF page 535 / chunk `p0535:c01`: figure 7.2 labels;
- PDF page 541 / chunk `p0541:c01`: figure 7.4 labels;
- PDF page 542 / chunk `p0542:c01`: figure 7.5 labels;
- PDF page 546 / chunk `p0546:c01`: figure 7.6 labels;
- PDF page 569 / chunk `p0569:c01`: figure 7.9 labels.

Handling: use the surrounding prose and readable captions; do not reconstruct unreadable labels from model memory. Figure-dependent details unsupported by prose remain `[Needs confirmation]`.

## [Needs confirmation] Review question 37 explicitly requires Internet research

- PDF page 575 / chunk `p0575:c01`.
- Question 37 asks to “find on the Internet two examples of virtual appliances from real life.”
- Chapter policy is `rag_only`: external sources are forbidden.

Handling: `review-answers.md` does not browse or invent examples. The answer is `[Needs confirmation]` unless the source policy is explicitly changed by the user.

## [Needs confirmation] EC2 wording spans two service-model contexts

- PDF page 551 / chunk `p0551:c01`: Amazon EC2 is described as hosting packaged virtual appliances offered to customers as convenient software services.
- PDF page 554 / chunk `p0554:c01`: Amazon EC2 is explicitly identified as an example of an IAAS cloud.

Handling: preserve both statements. For service-model classification in review question 29, use the explicit classification from section 7.11.1: EC2 = IAAS. Do not silently reinterpret the wording on page 551.
