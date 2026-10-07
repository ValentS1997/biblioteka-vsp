# Source findings — chapter 4

Scope: PDF pages 103-133.

## 1. No blank source units inside the chapter

The book RAG manifest does not list any source unit from PDF 103 through PDF 133 as blank.

Handling:
- chapter boundary is fully addressable at page level;
- no missing-page reconstruction is required.

## 2. [Source extraction limitation] figures are text-only in current RAG

The chapter relies on figures 4.1-4.15, including layered interaction, OSI mapping, protocol stacks, protocol distribution and network-role diagrams.

The current RAG does not encode those figures as independent multimodal objects.

Handling:
- Mermaid and SVG artifacts are newly composed from extracted text;
- original visual geometry is not reconstructed.

## 3. [Source wording] classification is explicitly non-unique

The source states that classification can use different criteria and that other sources may classify networks differently.

Handling:
- chapter artifacts preserve each listed classification dimension independently;
- no single exclusive taxonomy is inferred.

## 4. [Source timeframe] standards and protocol-stack examples are historical source content

The chapter names standards, organizations and stacks in the form current for the book edition.

Handling:
- no web-based freshness correction is applied in `rag_only` mode;
- statements are treated as chapter content, not as a claim about current deployment status.
