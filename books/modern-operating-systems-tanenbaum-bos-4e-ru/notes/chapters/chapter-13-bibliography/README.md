# Глава 13 — Библиография

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 13 — «Библиография»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `1110–1119`
- Addressable RAG chunk range: `p1110:c01 … p1119:c01`
- Chunks in chapter range: `10`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 1110 begins with `Глава 13. Библиография`;
  - PDF page 1120 is publisher/printing colophon, not another chapter.
- Chapter boundary: `VERIFIED`
- End-of-book chapter boundary: `VERIFIED`

Unlike Chapters 1–12, this chapter contains no explicit chapter-end summary and no review-question section. The local source contains curated further-reading recommendations and a note that the detailed alphabetical bibliography is available from the publisher site.

## Main principle

Chapter 13 is a **continuation map**, not a conventional teaching chapter.

Its purpose is to direct further study by topic:

`general OS → processes/concurrency → memory → filesystems → I/O → deadlock → virtualization/cloud → multiprocessors → security → Linux/Android → Windows → OS design`.

The source also recommends recurring research venues: SOSP, OSDI, EuroSys, ACM Transactions on Computer Systems and ACM SIGOPS Operating Systems Review.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 13.1 | Дополнительная литература | 1110–1119 |
| 13.1.1 | Введение и общие труды | 1110–1111 |
| 13.1.2 | Процессы и потоки | 1111 |
| 13.1.3 | Управление памятью | 1111–1112 |
| 13.1.4 | Файловые системы | 1112 |
| 13.1.5 | Ввод-вывод | 1112–1113 |
| 13.1.6 | Взаимоблокировка | 1113–1114 |
| 13.1.7 | Виртуализация и облако | 1114 |
| 13.1.8 | Многопроцессорные системы | 1114–1115 |
| 13.1.9 | Безопасность | 1115–1117 |
| 13.1.10 | Изучение конкретных примеров 1: Unix, Linux и Android | 1117–1118 |
| 13.1.11 | Изучение конкретных примеров 2: Windows 8 | 1118 |
| 13.1.12 | Проектирование операционных систем | 1118–1119 |
| 13.2 | Алфавитный список литературы | 1119 |

## Reading anchors from the source

- **General OS:** Silberschatz et al., Stallings, Stevens.
- **Processes/concurrency:** Arpaci-Dusseau, Andrews & Schneider, Ben-Ari, Zhuravlev et al., Stratton et al.
- **Memory:** Denning, Knuth, Arpaci-Dusseau.
- **Filesystems:** McKusick et al., Silberschatz et al., Stallings, Cornwell.
- **I/O:** Geist & Daniel, Scheible, Stan & Skadron, Swanson & Caulfield, Ion, Walker & Cragon.
- **Deadlock:** Coffman et al., Holt, Isloor & Marsland, Levine, Shub.
- **Virtualization/cloud:** Portnoy, Erl et al., Rosenblum & Garfinkel, Whitaker et al.
- **Multiprocessors:** Ahmad, Dubois et al., Geer, Kant & Mohapatra, Kumar et al., Kwok & Ahmad, Zhuravlev et al.
- **Security:** Anderson, Van der Veen et al., Bratus, Denning, Ford & Allen, Hafner & Markoff, Johnson & Jajodia, Ludwig, Mead, Milojicic, Nachenberg, Sasse, Thibadeau.
- **Linux/Android:** Bovet & Cesati, POSIX standard, Fusco, Maxwell.
- **Windows:** Cusumano & Selby, Rector & Newcomer, Russinovich & Solomon.
- **OS design:** Saltzer & Kaashoek, Brooks, Cooke et al., Corbató, Crowley, Lampson, Wirth.

## Operational interpretation

Use this chapter as a routing layer:

1. identify the topic that needs deeper study;
2. choose a source recommended in the corresponding subsection;
3. preserve the distinction between textbook/tutorial sources, standards, implementation internals and research papers;
4. treat the bibliographic recommendation as historical/source-era guidance rather than a claim that the listed edition is still the newest;
5. verify current availability/edition separately only when external research is explicitly allowed.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- The local PDF does **not** contain the full alphabetical bibliography promised by section 13.2; it points readers to the publisher site.
- External links, availability, newer editions and current venue schedules are not verified under `rag_only`.
- The chapter has no source review questions; canonical review artifacts record `0/0` rather than inventing questions.
- This is the final numbered chapter in the source. PDF page 1120 is colophon/end matter.
