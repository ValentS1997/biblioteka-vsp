# Chapter 13 conceptual / reading flow

```mermaid
flowchart TD
    GAP["Identify knowledge gap"] --> TYPE{"What kind of source?"}

    TYPE --> GEN["Broad textbook / tutorial"]
    TYPE --> STD["Standard"]
    TYPE --> INT["Implementation internals"]
    TYPE --> PAP["Paper / survey"]
    TYPE --> DES["Design / experience"]

    GEN --> TOPIC["Choose topic"]
    STD --> POSIX["POSIX / interface semantics"]
    INT --> CASE["Linux or Windows internals"]
    PAP --> TOPIC
    DES --> OSD["OS design"]

    TOPIC --> PROC["processes / threads"]
    TOPIC --> MEM["memory"]
    TOPIC --> FS["filesystems"]
    TOPIC --> IO["I/O"]
    TOPIC --> DL["deadlock"]
    TOPIC --> VC["virtualization / cloud"]
    TOPIC --> MP["multiprocessors"]
    TOPIC --> SEC["security"]

    CASE --> LNX["Linux / Android"]
    CASE --> WIN["Windows"]

    OSD --> PRIN["Saltzer / Brooks / Corbato / Lampson / Wirth"]

    GAP --> VENUE["Research venues"]
    VENUE --> SOSP["SOSP"]
    VENUE --> OSDI["OSDI"]
    VENUE --> EURO["EuroSys"]
    VENUE --> ACM["ACM TOCS / SIGOPS OSR"]
```

## Boundary

```text
bibliographic recommendation ≠ proof of current edition
source-era venue cadence ≠ current schedule
publisher-linked bibliography ≠ content present in local PDF
chapter 13 ≠ conventional review-question chapter
```
