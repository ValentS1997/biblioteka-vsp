# Source-confirmed SQL examples — глава 7

Включены только SQL examples, явно присутствующие в chapter RAG. Product-specific syntax beyond these examples не добавлялся.

## Read-only COUNT

Источник: `p0273:c01`, PDF 273.

~~~sql
SELECT COUNT(*) FROM emails
WHERE recipient_id = 2 AND unread_flag = true;
~~~

Тип: read-only.

Смысл: вычислить количество unread messages.

Verification: результат соответствует фактическому множеству сообщений, удовлетворяющих predicate.

Rollback: `[Not applicable]`.

## Atomic update вместо read-modify-write

Источник: `p0289:c01`, PDF 289.

~~~sql
UPDATE counters
SET value = value + 1
WHERE key = 'foo';
~~~

Тип: state-changing.

Effect: source показывает эту форму как безопасную concurrent atomic update в большинстве relational DB.

Risk: изменяет persistent value; конкретная semantics зависит от matching row и transaction context.

Verification: при двух concurrent increments итоговое значение увеличивается на 2, а не теряет одно update.

Rollback: source не дает универсальной обратной команды — `[Needs confirmation]`.

## Explicit row lock

Источник: `p0290:c01`, PDF 290.

~~~sql
BEGIN TRANSACTION;

SELECT * FROM figures
  WHERE name = 'robot' AND game_id = 222
  FOR UPDATE;

-- Проверяем допустимость хода, после чего обновляем
-- возвращенную предыдущим SELECT позицию фигуры.
UPDATE figures
SET position = 'c4'
WHERE id = 1234;

COMMIT;
~~~

Тип: state-changing transaction.

Effect:

- `SELECT ... FOR UPDATE` блокирует возвращенные rows;
- application выполняет проверку и update;
- `COMMIT` фиксирует transaction.

Risk:

- forgotten lock path возвращает race condition;
- lock contention увеличивает latency;
- concrete row/value from source is an example, not deployment data.

Verification: concurrent transaction не может одновременно изменить locked figure до завершения первой.

Rollback: при abort база должна отбросить writes; explicit product-specific rollback command в example не приведен — `[Needs confirmation]`.

## Explicit lock against write skew

Источник: `p0295:c01`, PDF 295.

~~~sql
BEGIN TRANSACTION;

SELECT * FROM doctors
  WHERE on_call = true
    AND shift_id = 1234
  FOR UPDATE;

UPDATE doctors
SET on_call = false
WHERE name = 'Alice'
  AND shift_id = 1234;

COMMIT;
~~~

Тип: state-changing transaction.

Effect: блокирует rows, на состоянии которых основано решение о снятии врача с дежурства.

Verification: concurrent transactions не должны совместно привести к состоянию без единого on-call doctor.

Rollback: source-specific explicit rollback syntax отсутствует — `[Needs confirmation]`.

## Predicate query used in phantom discussion

Источник: `p0307:c01`, PDF 307.

~~~sql
SELECT * FROM bookings
WHERE room_id = 123
  AND end_time   > '2018-01-01 12:00'
  AND start_time < '2018-01-01 13:00';
~~~

Тип: read-only predicate query.

Смысл: найти bookings, пересекающие заданный room/time range.

Source point: serializable 2PL must protect not only existing rows but also the predicate/range, because a concurrent insert can create a phantom.

Verification: concurrent insert/update matching predicate must not make a serializable transaction observe an impossible history.

Rollback: `[Not applicable]`.

## Source-confirmed mechanisms/tools

Глава явно обсуждает:

- `BEGIN TRANSACTION`;
- `COMMIT`;
- `SELECT ... FOR UPDATE`;
- atomic `UPDATE`;
- MVCC;
- snapshot isolation;
- predicate locks;
- index-range / next-key locks;
- 2PL;
- SSI;
- stored procedures;
- transaction retry.

## Retry rule from source

Источник: `p0277:c01`, PDF 277.

Retry aborted transaction не является универсально безопасным:

- ambiguous commit может привести к duplicate effect;
- overload может усилиться от retry loop;
- permanent error не исправляется retry;
- external side effects не откатываются автоматически вместе с DB transaction.

Source рекомендует ограничивать retries, использовать exponential backoff для overload scenarios и различать transient/permanent errors.

## Что не добавлено

- `SET TRANSACTION ISOLATION LEVEL ...`;
- vendor-specific deadlock diagnostics;
- PostgreSQL/MySQL lock-monitoring queries;
- explicit `ROLLBACK` command;
- DB configuration commands.

Такие команды не были подтверждены выбранными chapter chunks.
