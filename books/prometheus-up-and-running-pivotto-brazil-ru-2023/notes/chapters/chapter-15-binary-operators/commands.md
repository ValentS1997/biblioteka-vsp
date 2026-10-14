# PromQL: двухместные операторы — глава 15

**Источник:** только canonical RAG PDF 258–272 (`p0258:c01`–`p0272:c01`), `rag_only`. Ни один запрос не исполнялся. Все примеры — **read-only** относительно TSDB, но могут создавать **workload-generating** нагрузку. Состояние среды и фактическое наличие именованной метрики: [Needs confirmation]. Rollback чтения: **[Not applicable]**.

## 1. Скаляр, арифметика, сравнения (PDF 258–261)

```promql
process_resident_memory_bytes / 1024
5 % 1.5
1e9 - process_resident_memory_bytes
x atan2 y
process_open_fds > 10
process_open_fds > bool 10
42 <= bool 13
```

- В книге `5 % 1.5` → scalar `0.5`; `process_resident_memory_bytes / 1024` формирует значения в KiB и теряет имя метрики (PDF 259).
- Шесть арифметических операторов: `+`, `-`, `*`, `/`, `%`, `^`; `atan2` работает как арифметический оператор и допускает vector matching (PDF 259–260).
- `process_open_fds > 10` возвращает только прошедшие фильтр исходные значения (в примере `14`), включая `__name__`; `> bool 10` возвращает значения 1/0 без имени (PDF 260–262).
- `42 <= bool 13` → scalar `0`; сравнение scalar/scalar **без** `bool` недопустимо по источнику (PDF 261–262).
- Float-сравнения на равенство ненадёжны. PDF 261 иллюстрирует проверку с epsilon:
```promql
(some_gauge - 1) < 1e-6 > -1e-6
```
  Это буквальный source example **цепочки фильтров**, а не новое соглашение синтаксиса без проверки текущей версии. Ожидаемые series и точные float semantics [Needs confirmation].

## 2. Сколько объектов превышают предел и какая доля (PDF 261–262)

```promql
count without(instance)(process_open_fds > 10)
sum without(instance)(process_open_fds > bool 10)
avg without(instance)(
  count without(device)(node_disk_io_now) > bool 4
)
```

- `count` после фильтра не показывает job без прошедших series. В тестовом примере `prometheus=1`, `node` отсутствует.
- `sum` после `bool` показывает `prometheus=1`, `node=0` при сохранении входных sample.
- `avg` по 0/1 даёт долю машин, где `count without(device)(node_disk_io_now)` больше 4 (как минимум пять устройств). Результаты текущей TSDB [Needs confirmation].

## 3. Сопоставление «один к одному»: метки, ignoring и on (PDF 263–265)

```promql
process_open_fds / process_max_fds

sum without(cpu)(rate(node_cpu_seconds_total{mode="idle"}[5m]))
/
ignoring(mode)
sum without(mode, cpu)(rate(node_cpu_seconds_total[5m]))

sum by(instance, job)(rate(node_cpu_seconds_total{mode="idle"}[5m]))
/
on(instance, job)
sum by(instance, job)(rate(node_cpu_seconds_total[5m]))

process_open_fds > (process_max_fds * .5)
(process_max_fds * .5) < process_open_fds
```

- Первое отношение в книге: `14/1024 = 0.013671875` и `7/1024 = 0.0068359375`, при совпадении `instance`, `job` (PDF 263).
- `ignoring(mode)` исключает mode из ключа, `on(instance,job)` ограничивает ключ конкретными labels. Во втором случае будущие новые target labels могут перестать участвовать в сопоставлении (PDF 264).
- Для сравнений двух instant vectors берётся **значение слева**, поэтому `process_open_fds > limit/2` лучше сообщает текущие дескрипторы, чем обратная перестановка (PDF 264–265).

## 4. «Многие к одному», динамическая кардинальность (PDF 265–268)

**Source-failing example, ожидаемая ошибка:**

```promql
sum without(cpu)(rate(node_cpu_seconds_total[5m]))
/
ignoring(mode)
sum without(mode, cpu)(rate(node_cpu_seconds_total[5m]))
```

При нескольких mode слева соответствует один RHS: `multiple matches for labels: many-to-one matching must be explicit (group_left/group_right)` (PDF 265).

**Explicit many-to-one:**

```promql
sum without(cpu)(rate(node_cpu_seconds_total[5m]))
/
ignoring(mode) group_left
sum without(mode, cpu)(rate(node_cpu_seconds_total[5m]))
```

Сохраняет `mode` слева и даёт относительную долю режима для каждого `instance` (PDF 266). Это не many-to-many: в группе справа должна быть одна серия на matching key.

**Копирование метки из информационной метрики:**

```promql
up
* on(instance) group_left(version)
prometheus_build_info
```

Ожидаемо source series `{instance="localhost:9090",job="prometheus",version="2.2.1"} 1` (PDF 266). **Внимание:** PDF 267 явно указывает, что `instance` не всегда глобально уникален: проверьте добавление `job` в matching key прежде чем применять к многим jobs.

**Датчики hwmon:**

```promql
node_hwmon_temp_celsius
* ignoring(label) group_left(label)
node_hwmon_sensor_label
```

Source: серии sensor=temp2/temp3 получают `label=core_0/core_1`; sensor=temp1 **отсутствует**, поскольку нет пары в `node_hwmon_sensor_label` (PDF 267).

## 5. Операции над множествами и заполнение разреженных рядов (PDF 268–271)

**Подстановка отсутствующей информационной метки:**

```promql
node_hwmon_sensor_label
or ignoring(label)
(node_hwmon_temp_celsius * 0 + 1)
```

```promql
node_hwmon_temp_celsius
* ignoring(label) group_left(label)
(
  node_hwmon_sensor_label
  or ignoring(label)
  (node_hwmon_temp_celsius * 0 + 1)
)
```

Это возвращает в итоговый температурный вектор также sensor=temp1 без `label`; `x*0+1` оставит `NaN` как `NaN`, по сноске PDF 269.

**Отсутствующая пользовательская метрика:**

```promql
node_custom_metric or up * 0
node_custom_metric or (up{job="node"} == 1) * 0
up{job="node"} == 1 unless node_custom_metric
up == 1 unless on(job, instance) node_custom_metric
```

Первый вариант возвращает 0 при неудачном scrape и для других jobs — известный риск. Второй ограничивает job и успешный scrape. `unless on(job,instance)` может учитывать любое число дочерних серий справа с дополнительными labels (PDF 269–270).

**Условное max-подобное выражение по тем же labels, из PDF 270:**

```promql
(a >= b) or b
```

Возвращает `a` при `a >= b`, иначе `b`, если совпадают групповые метки. **[Source contradiction]** словесное описание `unless` PDF 270 конфликтует с примерами и обычным значением разности; не переносить спорную фразу как исполнимую семантику, см. [source-findings.md](source-findings.md).

**Два условия тревоги через `and`:**

```promql
(
  rate(http_request_duration_seconds_sum{job="prometheus"}[5m])
  /
  rate(http_request_duration_seconds_count{job="prometheus"}[5m])
) > 1
and
rate(http_request_duration_seconds_count{job="prometheus"}[5m]) > 1
```

**Время суток UTC:**

```promql
(
  rate(http_request_duration_microseconds_sum{job="prometheus"}[5m])
  /
  rate(http_request_duration_microseconds_count{job="prometheus"}[5m])
) > 1000000
and
rate(http_request_duration_microseconds_count{job="prometheus"}[5m]) > 1
and on()
hour() >= 9 < 17
```

Примеры **используют разные исходные семейства** `_seconds_` и `_microseconds_` (PDF 271). Источник отмечает, что `hour()` — UTC, 09:00–17:00 в локальной зоне **не подтверждены**.

## 6. Приоритет (PDF 272)

```text
1) ^
2) * / % atan2
3) + -
4) == != > < >= <=
5) unless and
6) or
```

`a or b * c + d` эквивалентно `a or ((b * c) + d)`; `a/b*c` — `(a/b)*c`, `a^b^c` — `a^(b^c)`. При неочевидном порядке использовать круглые скобки.

## Verification и rollback

Каждый пример проверять на реально существующих метриках, количестве рядов до и после matching, метках `instance`/`job`/`mode`/`version`, успешности scrape и ожидаемой кардинальности RHS. **State-changing operations в этой главе не приведены; rollback [Not applicable]**. Конкретный объём нагрузки, source API/version и правила алертов окружения [Needs confirmation].
