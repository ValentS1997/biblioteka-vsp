# Шпаргалка главы 4 — encoding, compatibility, evolution

## Symptom / problem framing

Проблема главы: данные и код живут разное время. При rolling upgrade старые и новые версии приложений реально сосуществуют, поэтому формат данных должен переживать изменение схемы и независимое развертывание компонентов.

Негативные сигналы:

- новый reader не читает старые данные;
- старый reader не читает новые данные;
- изменение field name/tag делает старые записи недекодируемыми;
- old code при read-modify-write теряет неизвестное новое поле;
- RPC retry может повторно выполнить действие;
- service/API evolution требует синхронного обновления всех клиентов;
- message producer/consumer нельзя обновлять независимо.

## Baseline / context

### Compatibility

- backward compatibility: новый код читает старые данные;
- forward compatibility: старый код читает новые данные.

### Encoding

- in-memory representation оптимизировано для работы программы;
- storage/network representation — самостоятельная byte sequence;
- encoding преобразует in-memory → bytes;
- decoding преобразует bytes → in-memory.

### Text formats

JSON/XML/CSV широко поддерживаются, но имеют неоднозначности типов, чисел и binary values. Binary data часто приходится кодировать текстом.

### Schema-based binary formats

Thrift, Protocol Buffers и Avro используют schema.

Thrift/Protocol Buffers:
- field tags являются частью encoded contract;
- field name можно менять, tag — нельзя;
- новый field должен иметь новый tag;
- удаленный tag нельзя повторно использовать;
- для backward compatibility новый field не должен внезапно становиться required без default/совместимого поведения.

Avro:
- writer schema и reader schema могут различаться;
- поля сопоставляются по имени;
- неизвестные reader'у поля writer schema игнорируются;
- отсутствующее поле может заполняться default из reader schema;
- совместимость определяется schema resolution rules.

## Read-only checks

1. Определить, кто writer и кто reader.
2. Проверить, могут ли одновременно работать old/new versions.
3. Для каждого изменения schema проверить backward compatibility.
4. Проверить forward compatibility.
5. Для Thrift/Protocol Buffers проверить стабильность field tags.
6. Проверить, не переиспользуется ли удаленный tag.
7. Для Avro проверить writer/reader schema pair и defaults.
8. Проверить сохранение unknown fields при read-modify-write.
9. Для database data определить срок жизни данных относительно code version.
10. Для REST/RPC определить versioning strategy.
11. Для retry определить, может ли request выполниться дважды.
12. Для message broker проверить независимость producer/consumer rollout.
13. Для actor messages проверить совместимость между узлами разных versions.

## Interpretation

- Новый код читает старые данные, старый новый — нет → есть backward, но нет forward compatibility.
- Field tag изменен → существующие encoded records теряют прежний смысл.
- Новое optional/defaulted field → совместимость обычно легче сохранить.
- Old code теряет неизвестное поле после повторной записи → compatibility формально есть на decode, но data evolution нарушена на application layer.
- API требует lock-step deploy client/server → evolvability ограничена.
- RPC timeout не сообщает, был ли request выполнен → retry требует учета duplicate execution.
- Broker отделяет sender/receiver → независимый deploy проще, если message encoding совместим.

## Next action

1. Зафиксировать writer/reader versions.
2. Описать schema/API/message delta.
3. Проверить backward и forward directions отдельно.
4. Прогнать old→new и new→old fixtures.
5. Выполнить controlled staged rollout.
6. Проверить decode errors, unknown-field preservation и behavior retries.
7. Расширять rollout только после acceptance.

## Modifying action

Source-confirmed modifying actions:

- добавить/удалить field в schema;
- изменить field type;
- переименовать field;
- выполнить rolling/staged upgrade;
- изменить API version;
- изменить producer/consumer version;
- перекодировать archival dump по новой schema.

Перед изменением нужно определить compatibility impact.

## Verification / acceptance checks

- новый код читает старые records/messages;
- старый код читает новые records/messages там, где требуется forward compatibility;
- unknown fields не теряются;
- field tags не изменены и не reused;
- defaults позволяют читать old data;
- staged rollout допускает одновременную работу versions;
- API clients старой версии продолжают работать в заявленном compatibility window;
- message consumers/producers обновляются независимо;
- retry behavior не создает неожиданных duplicate effects.

## Rollback

- Staged rollout: остановить расширение новой версии и вернуть traffic к ранее работающей версии; точные deployment commands `[Needs confirmation]`.
- Schema change: конкретный rollback зависит от format/storage и в главе универсально не задан — `[Needs confirmation]`.
- API version: возврат к ранее поддерживаемой version зависит от service implementation — `[Needs confirmation]`.
- Read-only decode/compatibility tests: `[Not applicable]`.

## Operational loop

`schema/API delta → backward test → forward test → staged rollout → observe → keep/rollback`.
