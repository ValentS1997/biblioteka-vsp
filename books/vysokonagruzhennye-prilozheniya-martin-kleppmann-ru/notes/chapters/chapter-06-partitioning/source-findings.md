# Source findings — глава 6

Source policy: `rag_only`.

## [Source extraction issue] Рисунок 6.7

- Provenance: `p0256:c01`, PDF 256.
- Наблюдение: addressable text chunk содержит разрозненные слова и подписи рисунка с потерей пространственной структуры.
- Контекст: окружающий текст на `p0255:c01` и `p0257:c01` явно описывает три routing approaches.
- Влияние: точное расположение клиентов, routing tier, nodes и стрелок на оригинальном рисунке 6.7 нельзя надежно восстановить из text-only RAG.
- Действие: `diagram.md` передает только три source-confirmed routing mechanisms из текста; оригинальный layout рисунка не реконструируется по model memory.
- Adjudication: exact visual layout остается `[Needs confirmation]`, если потребуется отдельный visual-source analysis.

## Прочие рисунки

Рисунки 6.1–6.6 и 6.8 используются только через окружающее текстовое описание. Их оригинальная геометрия не воспроизводится в chapter artifacts.
