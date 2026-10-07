# Source findings — глава 3

Source policy: `rag_only`.

## [Source extraction issue] Рисунок 3.8

- Provenance: `p0124:c01`, PDF 124.
- Наблюдение: addressable text chunk содержит фрагментированные слова/подписи рисунка и не сохраняет надежную пространственную структуру схемы.
- Контекст: `p0123:c01` текстом описывает data warehouse и процесс ETL (extract — transform — load), а PDF 124 содержит рисунок 3.8.
- Влияние: точное расположение систем, стрелок и подписей на рисунке 3.8 нельзя надежно восстановить из canonical text-only RAG.
- Действие: chapter artifacts используют только текстовое описание ETL из `p0123:c01`; схема рисунка 3.8 не реконструируется по model memory.
- Adjudication: графическая структура рисунка остается `[Needs confirmation]`, если потребуется отдельный visual-source analysis.

## Прочие визуальные элементы

Рисунки B-tree, SSTable, star schema, column layout и OLAP cube в текстовом RAG представлены главным образом через окружающее текстовое описание. В текущих артефактах не делается попыток восстановить их точный оригинальный layout.
