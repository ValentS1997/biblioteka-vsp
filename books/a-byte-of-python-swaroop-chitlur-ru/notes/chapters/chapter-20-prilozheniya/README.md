# Глава 20. Приложения

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Эта финальная объединённая глава создана по решению пользователя и объединяет
оригинальные приложения 20–23 книги, а также последнюю post-appendix страницу,
чтобы закрыть source coverage до конца PDF.

Внутреннее соответствие оригиналу:

- original 20 — «Приложение: FLOSS»
- original 21 — «Приложение: о книге»
- original 22 — «Приложение: История версий»
- original 23 — «Приложение: Инструкция по переводу»
- PDF 160 — финальная биографическая back-matter страница автора

Это объединение является организацией артефактов библиотеки; исходная структура
книги в provenance сохраняется явно.

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- merged RAG range: `p0151:c01` — `p0160:c01`
- PDF pages: 151–160
- original appendix 20: PDF 151–152
- original appendix 21: PDF 153–154
- original appendix 22: PDF 155–158
- original appendix 23: PDF 159
- final author bio/back matter: PDF 160
- end of canonical PDF source: PDF 160
- boundary verified: yes

## Main principle

Финальные материалы книги дают четыре вида контекста:

1. FLOSS как community/sharing model и перечень свободного ПО;
2. история создания книги и использовавшихся authoring tools;
3. хронология версий книги;
4. инструкция по участию в переводе через исходный Git repository / Pandoc workflow.

Последняя страница добавляет краткую биографическую справку об авторе.

## Source map

| Original section | PDF | Source-grounded content |
|---|---:|---|
| Appendix 20 — FLOSS | 151–152 | FLOSS concept; Linux/GNU/Ubuntu/LibreOffice/Firefox/Thunderbird/Mono/Apache/MySQL/VLC and other examples; community/resources. |
| Appendix 21 — About the book | 153–154 | KWord → DocBook XML/Kate → OpenOffice → XEmacs/Quanta+ → MediaWiki/Vim → Vim/Pandoc/Mac OS X; author link. |
| Appendix 22 — Version history | 155–158 | Timeline from 0.10 (2003) through 2.0 (2012); format/tool/content changes. |
| Appendix 23 — Translation instructions | 159 | Git repository, fork/download/edit `.pd` files, Pandoc README/build prerequisites. |
| Final back matter | 160 | Short author biography/current-role statement from the source edition. |

## Operational acceptance

После объединённого финального артефакта читатель должен уметь:

- объяснить FLOSS framing источника;
- перечислить несколько FLOSS examples exactly as source examples;
- описать evolution authoring workflow книги;
- локализовать major version-history milestones;
- описать source translation workflow without inventing Git commands;
- отличить appendices from final author-bio back matter;
- понимать, что ecosystem/company/project-status claims относятся к source edition and
  are not current-verified facts.

## Safety / integrity boundary

Эта объединённая глава почти полностью conceptual/historical.

Potential modifying actions присутствуют только как instructions in Appendix 23:

- create a repository fork;
- download repository;
- edit `.pd` source files;
- install tools required by README/Pandoc build process.

Source не даёт exact commands, repository permissions, branch policy, rollback or build
environment details. Поэтому canonical artifacts не синтезируют `git clone`,
`git checkout`, `pip`, package-manager или push commands.

Все current-looking claims about project popularity, market share, platform support,
company roles and software status are treated as historical source statements and marked
in `source-findings.md`.

## Completion boundary

This artifact closes chapter-analysis source coverage at `p0160:c01` / PDF 160,
the last page of the canonical source.

Chapter-analysis collection for this book is therefore complete for:

- chapters 1–19;
- merged chapter 20 covering original appendices 20–23;
- final PDF back matter through page 160.

Reading-state metadata is not changed by this artifact.

## Conditional artifacts

- No common explicit chapter-end summary exists across appendices 20–23, therefore
  `summary.md` is not created.
- No formal review/control-question section exists, therefore
  `review-questions.md` / `review-answers.md` are not created.
- Source extraction defects and time-sensitive historical claims exist, therefore
  `source-findings.md` is created.
