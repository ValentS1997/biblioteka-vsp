# Шпаргалка: Chapter 3 — как сформировались incident response models

## Historical chain

```text
Early incidents
   ↓
Morris Worm (1988)
   ↓
need for coordinated response
   ↓
CERT (1988)
   ↓
CIAC (1989 / methodology 1990)
   ↓
US Navy guide (1996)
   ↓
SANS Step-by-Step (1998)
   ↓
NIST SP 800-61 (2004 → Rev.1 → Rev.2)
   ↓
NIST SP 800-61 Rev.3 / CSF alignment (2025)
```

## Early incidents highlighted by the source

| Period | Incident | Why it matters in the chapter |
|---|---|---|
| 1982 | The 414s | ранняя широкая media attention |
| 1984 | CCC BTX Hack | demonstration of systemic weakness |
| 1986 | Cuckoo’s Egg/KGB Espionage | early cyber-espionage |
| 1987 | Max Headroom intrusion | high-profile unauthorized takeover |
| 1988 | Morris Worm | catalyst for formal IR |
| 1992 | Michelangelo | public concern around malware |
| 1994 | Mitnick/Shimomura | targeted intrusion/investigation |
| 1998 | Moonlight Maze | long-running cyber-espionage |
| 1999 | Melissa | mass email malware impact |

## Morris Worm: what to remember

Technical factors named by source:

- Sendmail DEBUG remote-code-execution path;
- Finger buffer overflow;
- weak RSH passwords;
- replication bug;
- reinfection until systems became unusable.

Organizational lesson:

**network-wide incidents require coordinated response, not isolated administrator action.**

## Contribution by model

### CERT
Goal:
- coordination and central point of contact.

### CIAC / Schultz
Goal:
- formal methodology;
- prioritize life/safety, sensitive data, systems, availability;
- six identifiable stages.

### US Navy
Goal:
- procedural expansion for military context.

### SANS
Goal:
- make expert practice usable by generalists under pressure.

Characteristics:
- Preparation;
- Identification;
- Containment;
- Eradication;
- Recovery;
- Follow-up.

### NIST SP 800-61
Goal:
- standardized incident handling guidance.

Rev.1/2 four phases:
1. Preparation
2. Detection and Analysis
3. Containment, Eradication, and Recovery
4. Post-Incident Activity

Revision 3:
- Govern
- Identify
- Protect
- Detect
- Respond
- Recover

## Interpretation

Долговечность old models — сильная сторона.

Но source одновременно показывает mismatch с modern threat landscape:

- cloud-distributed identity;
- third-party SaaS;
- supply-chain compromise;
- AI-orchestrated attack tooling;
- adversary adapts during response.

Отсюда вопрос для дальнейшей книги:

**может ли model, построенная вокруг более простых incidents, достаточно хорошо поддерживать adaptive response сегодня?**

## Verification / acceptance

Для анализа framework проверить:

- origin;
- original threat assumptions;
- lifecycle structure;
- feedback/iteration support;
- role of coordination;
- fit to modern environment.

## Commands / changes / rollback

[Not applicable]

Chapter 3 — historical/conceptual. Operational defender commands отсутствуют.
