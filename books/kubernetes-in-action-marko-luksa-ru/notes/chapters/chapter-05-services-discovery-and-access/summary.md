# Резюме главы 5

Источник: явный раздел 5.8 Резюме, RAG chunks p0210:c01–p0211:c01.

После главы читатель должен понимать, как Kubernetes предоставляет стабильный network identity динамическим Pods.

Ключевые результаты:

- Service предоставляет группе Pods единый стабильный IP и port;
- Pods выбираются label selector, а фактические backend addresses отражаются в Endpoints;
- Service по умолчанию доступен изнутри cluster;
- NodePort и LoadBalancer позволяют открыть Service внешним clients;
- Service discovery возможен через environment variables и cluster DNS;
- Service без selector + ручной Endpoints позволяет представить внешнюю систему как Kubernetes Service;
- ExternalName создаёт DNS CNAME alias для внешнего FQDN;
- Ingress предоставляет HTTP access к нескольким Services через единый внешний вход;
- readiness probe определяет, должен ли Pod находиться в Service Endpoints;
- Headless Service позволяет обнаруживать individual Pod IPs через DNS;
- chapter даёт последовательный checklist troubleshooting Services.

Дополнительные operational skills главы:

- kubectl exec для запуска команд и shell внутри Pod;
- изменение GCE firewall rules;
- kubectl apply для обновления resource;
- source-era kubectl run --generator=run-pod/v1 для unmanaged Pod.

## Центральная модель

~~~text
Pod labels + readiness
        ↓
     Endpoints
        ↓
Service stable identity
        ↓
clients

External:
NodePort / LoadBalancer / Ingress

Discovery:
environment variables / DNS / Headless DNS
~~~

## Provenance

- Chapter chunks: p0168:c01–p0211:c01
- Summary chunks: p0210:c01–p0211:c01
- PDF pages: 210–211
- Printed pages: 209–210
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
