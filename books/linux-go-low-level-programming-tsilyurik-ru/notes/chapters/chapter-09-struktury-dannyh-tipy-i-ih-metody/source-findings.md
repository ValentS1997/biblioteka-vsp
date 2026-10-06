# Source findings — глава 9 «Структуры данных, типы и их методы»

## Finding 1 — contradictory wording about slice argument passing

Classification: **[Source wording contradiction]**

Provenance:

- page 218, chunk `p0218:c01`;
- pages 219–220, chunks `p0219:c01`, `p0220:c01`.

Observed:

На странице 218 источник пишет, что slice «передаётся по ссылке». Позже источник утверждает, что «в корне неверно говорить», что slices Go передаются при вызове по ссылке.

Impact:

Две формулировки нельзя одновременно использовать как одну каноническую терминологию.

Action:

- обе сохранены как source evidence;
- canonical artifacts описывают observable behavior примера;
- точная языковая модель без внешней спецификации: **[Needs confirmation]**.

## Finding 2 — double increment inside garray_c pointer loop

Classification: **[Source code anomaly]**

Provenance:

- page 218, chunk `p0218:c01`;
- output on page 219.

Observed code:

```c
for(i = 0; i < size; i++) p->data[i++]++;
```

`i` увеличивается внутри expression и в post-expression цикла.

Observed output:

```text
[ 7 ]: 2 0 3 0 4 0 5
```

Impact:

Изменяются элементы через один, в отличие от соседних examples с инкрементом каждого элемента.

Action:

- код не исправлялся;
- output считается подтверждением фактического поведения source example;
- intended loop: **[Needs confirmation]**.

## Finding 3 — Stringer explanation is unsupported inside this chapter

Classification: **[Source technical claim / Needs confirmation]**

Provenance:

- page 220, chunk `p0220:c01`.

Observed:

Источник объясняет форматирование arrays/slices через реализацию `Stringer` и метода `String()`.

Chapter evidence показывает только `fmt.Println` и `fmt.Printf("%v", ...)` и не показывает определения `String()` или отдельную проверку interface satisfaction.

Impact:

В режиме `rag_only` механизм нельзя независимо подтвердить по материалам главы.

Action:

- canonical artifacts сохраняют наблюдение, что `fmt` печатает nested slice;
- объяснение через `Stringer` остаётся source claim;
- external adjudication: **[Needs confirmation]**.

## Finding 4 — lifetime explanation for returned locals is source-scoped

Classification: **[Source technical model]**

Provenance:

- page 221, chunk `p0221:c01`.

Observed:

Источник связывает возможность возврата локально созданных значений с garbage collection и временем жизни до исчезновения последней ссылки.

Impact:

Внутри главы нет отдельного доказательства memory/escape mechanism.

Action:

- multiple-return behavior сохраняется;
- объяснение механизма не расширяется и не исправляется внешним знанием.
