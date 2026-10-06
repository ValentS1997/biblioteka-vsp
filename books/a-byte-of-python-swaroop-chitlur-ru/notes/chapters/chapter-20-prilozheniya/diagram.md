# Chapter logic diagram — «Приложения»

```mermaid
flowchart TD
    A["Merged final artifact"] --> B["Original Appendix 20: FLOSS"]
    B --> B1["community / sharing"]
    B --> B2["free-software examples"]
    B --> B3["historical resource references"]

    A --> C["Original Appendix 21: About the book"]
    C --> C1["authoring tools"]
    C --> C2["format evolution"]
    C --> C3["author reference"]

    A --> D["Original Appendix 22: Version history"]
    D --> D1["0.10 → ... → 2.0"]
    D --> D2["content / format / tooling changes"]

    A --> E["Original Appendix 23: Translation"]
    E --> E1["Git repository"]
    E1 --> E2["fork / download"]
    E2 --> E3["edit .pd files"]
    E3 --> E4["Pandoc README / build dependencies"]
    E4 --> E5["exact commands not supplied"]

    A --> F["PDF 160: final author bio"]
    F --> G["End of canonical PDF source"]

    B3 --> G
    C3 --> G
    D2 --> G
    E5 --> G
```

## Source boundary

Merged artifact:

`p0151:c01` → `p0160:c01`.

Original appendix boundaries:

- 20: `p0151:c01–p0152:c01`
- 21: `p0153:c01–p0154:c01`
- 22: `p0155:c01–p0158:c01`
- 23: `p0159:c01`
- final back matter: `p0160:c01`

`p0160:c01` is the final PDF page; there is no next source page.
