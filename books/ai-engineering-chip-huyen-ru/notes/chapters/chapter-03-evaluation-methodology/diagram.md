# Диаграммы главы 3

## Выбор метода оценки

~~~mermaid
flowchart TD
    FAIL["Определить failure mode / свойство"] --> FUNC{"Можно проверить функцию<br/>автоматически?"}
    FUNC -- "да" --> FC["Functional correctness<br/>tests · pass@k · objective"]
    FUNC -- "нет" --> REF{"Есть надежный<br/>reference answer?"}
    REF -- "да" --> FORM{"Что важно?"}
    FORM -- "точное совпадение" --> EXACT["Exact match"]
    FORM -- "форма текста" --> LEX["Lexical similarity<br/>BLEU · ROUGE · edit/n-gram"]
    FORM -- "смысл" --> SEM["Semantic similarity<br/>embeddings · cosine"]
    REF -- "нет / недостаточно" --> SUBJ{"Нужна subjective judgment?"}
    SUBJ -- "да" --> JUDGE["Human or AI judge"]
    JUDGE --> DEF["Fix evaluator definition:<br/>model + prompt + sampling"]
    DEF --> REPEAT["Check consistency / bias / cost"]
    FC --> CONTEXT["Interpret in application context"]
    EXACT --> CONTEXT
    LEX --> CONTEXT
    SEM --> CONTEXT
    REPEAT --> CONTEXT
~~~

## Жизненный цикл AI-судьи

~~~mermaid
flowchart LR
    INPUT["Evaluation set"] --> V1["Judge v1<br/>model + prompt + settings"]
    V1 --> SCORE1["Scores v1"]
    CHANGE["Change model / prompt / settings"] --> V2["Judge v2"]
    INPUT --> V2
    V2 --> SCORE2["Scores v2"]
    SCORE1 --> COMP{"Comparable?"}
    SCORE2 --> COMP
    COMP -- "только после control run" --> INTERP["Interpret app change"]
    COMP -- "нет" --> DRIFT["Evaluator drift risk"]
~~~

Глава подчеркивает: изменение evaluator-а может имитировать improvement/regression приложения.

## Comparative evaluation

~~~mermaid
flowchart TD
    MODELS["Candidate models"] --> PAIRS["Pairwise comparisons"]
    PAIRS --> SIGNAL["winner / tie signals"]
    SIGNAL --> RANK["Ranking algorithm<br/>Elo · Bradley–Terry · TrueSkill"]
    RANK --> REL["Relative ranking"]
    REL --> LIMIT["Не дает автоматически<br/>absolute usefulness / ROI"]
~~~
