# Translation / editorial findings — Chapter 16

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0472:c01`–`p0545:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-16-accelerating-incident-response-with-ai.md`.

## Итог проверки

- Semantic coverage: extensive.
- Listings 122–139 preserved.
- Tables 43–49 preserved.
- Figures 142–177 represented.
- Main debt: extremely high English-heading density and hybrid AI/security terminology.

## High-priority heading cleanup

Representative examples:

- `INTRODUCTION`
- `AI COSTS AND ACCESS`
- `Opportunities and Cautions`
- `Hallucination Risk`
- `Non-Determinism`
- `Data Handling`
- `Training Cutoff / Staleness`
- `Data Handling Considerations`
- `Frontier Models`
- `Open-Weight Models`
- `Data Sanitization`
- `PROMPTING FOUNDATIONS`
- `Structured Prompts for Complex Tasks`
- `FOUNDATIONAL USE CASES`
- `Code Analysis and Deobfuscation`
- `VERIFICATION IS NON-NEGOTIABLE`
- `Log Analysis and Anomaly Detection`
- `Limitations of AI Log Analysis`
- `Translating Technical Findings for Stakeholders`
- `INTERMEDIATE USE CASES`
- `Generating Incident Response Playbooks`
- `Drafting Incident Reports`
- `Specialized Knowledge Integration with MCP`
- `Creating Tabletop Exercise Scenarios`
- `ADVANCED USE CASES`
- `Model Context Protocol for Defensive Operations`
- `Security Considerations`
- `MCP SUPPLY CHAIN AND REGISTRY RISKS`
- `Forensic Analysis Acceleration with Protocol SIFT`
- `From Tool Use to Tool Orchestration`
- `REACT AGENTS`
- `Human in the Loop (HITL)`
- `OPERATIONAL CONSIDERATIONS`
- `LOOKING FORWARD`

## Canonical terminology proposal

- AI-assisted Incident Response → Реагирование на инциденты с поддержкой ИИ
- Frontier Models → передовые коммерческие модели
- Open-Weight Models → модели с открытыми весами
- Data Handling → обработка данных
- Data Sanitization → обезличивание/очистка данных
- Hallucination → галлюцинация модели
- Non-Determinism → недетерминированность
- Prompting → формирование запросов / prompting
- Context Window → контекстное окно
- MCP → Model Context Protocol (MCP), first use
- MCP Server → MCP-сервер
- Prompt Injection → инъекция инструкций / prompt injection
- Agentic AI → агентный ИИ
- Tool Orchestration → оркестрация инструментов
- ReAct Agent → агент ReAct
- Human in the Loop → человек в контуре (HITL)
- Inference Constraint → ограничение области вывода модели
- Auditability → аудируемость
- Defensibility → доказуемость/защищаемость вывода
- Skill File → файл навыка / skill file
- Prompt Library → библиотека запросов

Tool/product names (OpenAI, Anthropic, Google, Microsoft, Claude, Gemini, Grok, OpenSearch, SIFT, Sigma, Twine, Twee) should remain.

## Structural findings

1. Chapter is extremely long and should be visually segmented into:
   - Data Handling;
   - Prompting;
   - Foundational Use Cases;
   - Intermediate Use Cases;
   - Advanced/MCP/Agentic;
   - Operational Governance.
2. Translation heading hierarchy is inconsistent because embedded generated playbook/report content introduces extra H1/H2/H3 blocks.
3. Generated content excerpts should be visually separated from author narrative.
4. Listings 122–139 need A4 monospace/wrapping QA.
5. Tables 43–49 need A4 QA.
6. MCP/agent sections require explicit trust-boundary callouts.
7. Attacker artifacts and defensive commands must be visually distinguished.
8. AI-generated examples must not be visually mistaken for verified book recommendations.
9. Contemporary product/model names and capabilities must preserve source timing; v2 should not silently update 2026 claims.
10. Data-handling warnings deserve front-of-chapter callout status.

## Visual debt

Figures 142–177.

Highest priority:
- Figure 142 — basic prompting: HIGH
- Figures 148–152 — AI log analysis: HIGH
- Figures 153–156 — playbook/report generation: HIGH
- Figure 167 — MCP architecture: CRITICAL
- Figure 168 — MCP installation anti-pattern: CRITICAL
- Figures 170–171 — MCP approval/query flow: HIGH
- Figures 173–176 — Protocol SIFT/ReAct: CRITICAL
- Figure 177 — Sigma skill generation: HIGH

## Priority

`CRITICAL`

Reason: Chapter 16 introduces powerful AI/MCP/agentic workflows where terminology precision and trust boundaries directly affect operational safety.
