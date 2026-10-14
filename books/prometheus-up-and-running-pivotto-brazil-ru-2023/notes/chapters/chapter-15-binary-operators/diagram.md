# Mermaid — глава 15 «Двухместные операторы»

**Источник:** канонические RAG `p0258:c01`–`p0272:c01` (PDF 258–272). Визуальные схемы созданы по тексту, не воспроизводят иллюстрации издания.

## Выбор двуоперандной операции

```mermaid
flowchart TD
 A["Операнды PromQL"]
 SC["Scalar + instant vector"]
 VE["Два instant vectors"]
 AR["Арифметика<br/>+ - * / % ^ atan2"]
 CO["Сравнения<br/>фильтр или bool=0/1"]
 SET["Множества<br/>or unless and"]
 MATCH["Проверить ключ и кратность<br/>on / ignoring"]
 A --> SC --> AR
 SC --> CO
 A --> VE --> MATCH
 MATCH --> AR
 MATCH --> CO
 MATCH --> SET
```

PDF 258–265 и 268. Арифметика удаляет имя метрики, фильтр сравнения сохраняет исходное значение, `bool` возвращает 0/1.

## Matching один к одному и многие к одному

```mermaid
flowchart TD
 L["LHS: instance, job, mode"]
 R["RHS: instance, job"]
 IGN["ignoring(mode)<br/>ключ instance, job"]
 BAD["Без group_left:<br/>multiple matches"]
 GL["group_left:<br/>многие слева → один справа"]
 GOOD["Сохранены левые ряды<br/>и mode"]
 L --> IGN
 R --> IGN
 IGN --> BAD
 IGN --> GL --> GOOD
```

PDF 263–266. `group_left(version)` копирует только заданную информационную метку справа, не допускает many-to-many (PDF 266–267).

## Разреженные серии и булева логика

```mermaid
flowchart TD
 HW["sensor temp1,temp2,temp3"]
 INFO["label только у temp2,temp3"]
 JOIN["* ignoring(label) group_left(label)"]
 LOSS["temp1 исчезает"]
 FILL["or ignoring(label)<br/>hwmon_temp*0+1"]
 ALL["temp1 остаётся без label<br/>temp2,temp3 с label"]
 HW --> JOIN
 INFO --> JOIN
 JOIN --> LOSS
 INFO --> FILL
 HW --> FILL --> ALL
```

PDF 267–269. Значение `NaN` не становится 1 при `x*0+1`; `up*0` требует фильтрации по job и успеху scrape (PDF 269–270).

## Приоритет операторов

```mermaid
flowchart LR
 EXP["^"]
 MUL["* / % atan2"]
 ADD["+ -"]
 CMP["== != > < >= <="]
 AND["unless / and"]
 OR["or"]
 EXP --> MUL --> ADD --> CMP --> AND --> OR
```

PDF 272. Стрелка означает снижение приоритета, `^` правоассоциативен.
