# Ответы к упражнениям главы 6

Это RAG-grounded решения по материалу главы, не официальный издательский answer key.

## Упражнение 1 — Service вместо port-forward

Что source подтверждает:

- fortune Pod содержит web-server container на container port 80;
- port-forward 8080:80 работает;
- exercise требует вместо port-forward предоставить Pod через Service.

Exact Service manifest, label selector и exact create/expose command внутри chapter 6 не приведены.

Поэтому безопасный ответ в рамках RAG-only:

1. создать Service, который маршрутизирует traffic к fortune Pod на port 80;
2. selector должен соответствовать labels Pod;
3. exact selector values: [Needs confirmation];
4. exact Service manifest/command: [Needs confirmation];
5. acceptance: HTTP request через Service возвращает fortune text, как и port-forward example.

Не добавлять команду kubectl expose или manifest из памяти.

## Упражнение 2 — Git synchronization sidecar

Source даёт архитектуру, но не готовый пошаговый manifest.

Подтверждённая схема:

~~~text
Git repository
      ↓
sync sidecar
      ↓
shared gitRepo volume
      ↓
Nginx main container
~~~

Требования:

1. Sync process должен выполняться в отдельном sidecar container, а не в Nginx container.
2. Использовать существующий image, который умеет синхронизировать Git working directory.
3. Смонтировать тот же volume в sidecar.
4. Настроить sidecar на repository из example.
5. После commit в repository файлы в volume должны обновиться.
6. Nginx, читающий этот volume, должен начать отдавать новую version без удаления Pod.

Что source не задаёт:
- конкретный image sidecar;
- его flags/environment variables;
- credentials/config для private repository;
- exact manifest.

Все эти поля: [Needs confirmation].

Source отдельно говорит, что built-in gitRepo не поддерживает private Git repository authentication; для private repository рекомендуется sidecar sync или аналогичный подход.

## Provenance

- Service exercise: p0219:c01
- Sidecar exercise: p0222:c01–p0223:c01
