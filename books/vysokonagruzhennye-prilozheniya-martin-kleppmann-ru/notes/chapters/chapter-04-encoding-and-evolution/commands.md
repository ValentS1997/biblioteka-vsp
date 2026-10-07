# Команды и инструменты главы 4

## Статус

Глава концептуальная. Полноценных shell/admin commands для выполнения инфраструктурных изменений не приводит.

## Source-confirmed examples

В chapter RAG присутствуют декларативные schema/data examples для:

- JSON record;
- Thrift IDL;
- Protocol Buffers schema;
- Avro IDL;
- Avro JSON schema.

Они относятся к описанию форматов и совместимости, а не к ready-to-run operational commands.

## Source-confirmed protocol/tool names

- HTTP GET;
- HTTP POST;
- REST;
- SOAP/WSDL;
- RPC;
- gRPC;
- command-line utility curl;
- message brokers;
- actor frameworks.

## Classification

- schema/data examples: non-executing;
- GET: обычно read-oriented protocol operation в приведенном контексте;
- POST: state effect зависит от API и в главе не фиксирован;
- curl: tool; конкретная command line в chapter RAG не приведена.

## Verification

Для schema evolution источник требует проверять:

- backward compatibility;
- forward compatibility;
- стабильность field tags для Thrift/Protocol Buffers;
- writer/reader schema compatibility для Avro;
- сохранение неизвестных полей при read-modify-write.

## Rollback

Конкретные CLI/schema rollback procedures в главе отсутствуют: `[Needs confirmation]`.

## Что не добавлено

Compiler commands, endpoint examples, broker CLI, deployment commands и schema-registry commands отсутствуют в chapter RAG и не восстановлены из model memory.
