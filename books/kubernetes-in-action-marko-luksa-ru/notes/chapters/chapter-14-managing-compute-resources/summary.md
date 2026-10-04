# Резюме главы 14

Источник: явный раздел 14.7 Резюме, RAG chunks p0527:c01–p0528:c01.

Основные выводы главы:

- resource requests помогают Kubernetes планировать размещение Pods;
- resource limits не дают одному workload бесконтрольно вытеснять другие;
- неиспользуемый CPU source распределяет с учётом CPU requests;
- container не уничтожается за попытку использовать слишком много CPU, но memory overuse может привести к kill;
- при memory pressure процессы уничтожаются с учётом QoS classes и фактического memory consumption;
- LimitRange задаёт minimum/maximum/default requests and limits для отдельных workloads/containers;
- ResourceQuota ограничивает aggregate resources namespace;
- requests/limits нужно корректировать на основе наблюдаемого потребления за достаточно долгий период.

## Центральная модель

~~~text
requests
  → scheduling reservation
  → CPU share under contention

limits
  → CPU throttling
  → memory OOM boundary

QoS
  → memory-pressure priority

LimitRange
  → per-object rules/defaults

ResourceQuota
  → namespace aggregate budget

metrics
  → validate and tune configuration
~~~

## Operational conclusion

Requests и limits нельзя оценивать только по capacity node или по одному моментному измерению.

Source рекомендует сравнивать:
- фактическое CPU usage vs CPU request;
- фактическое memory usage vs memory request;
- configured limits vs observed peaks.

Если CPU consumption устойчиво выше request, workload может быть throttled relative to peers under contention. Если memory request сильно выше фактического usage, namespace/node capacity резервируется впустую.

## Provenance

- Chapter chunks: p0492:c01–p0528:c01
- Summary chunks: p0527:c01–p0528:c01
- PDF pages: 527–528
- Printed pages: 526–527
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
