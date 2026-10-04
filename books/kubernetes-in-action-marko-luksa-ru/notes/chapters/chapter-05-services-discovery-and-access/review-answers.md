# Ответы к упражнениям главы 5

Это RAG-grounded решения по материалу главы, не официальный издательский answer key.

## Упражнение 1 — ClientIP session affinity

Source manifest fragment:

~~~yaml
apiVersion: v1
kind: Service
spec:
  sessionAffinity: ClientIP
~~~

Точный полный manifest дополнительного Service и exact create command chapter не даёт.

После создания Service проверку следует выполнять с одного и того же client Pod/IP. Source-supported request pattern:

~~~bash
kubectl exec <client-pod> -- curl -s http://<service-ip>
~~~

Выполнить несколько раз.

Expected:
- при sessionAffinity: ClientIP подключения от одного client IP должны направляться в один и тот же backend Pod;
- для default None source демонстрирует распределение отдельных connections между разными Pods.

Ограничение source model: Service работает на TCP/UDP level; cookie-based session affinity здесь отсутствует.

## Упражнение 2 — Multi-port Service

Source Pod port model:

~~~text
ports:
- name: http
  containerPort: 8080
- name: https
  containerPort: 8443
~~~

Source Service model:

~~~text
ports:
- name: http
  port: 80
  targetPort: 8080
- name: https
  port: 443
  targetPort: 8443
selector:
  app: kubia
~~~

В chapter также показана возможность ссылаться на named target ports:

~~~text
targetPort: http
targetPort: https
~~~

Acceptance criteria по source:

1. Один Service имеет один ClusterIP.
2. Service публикует два named ports.
3. Port 80 направляется на backend port 8080.
4. Port 443 направляется на backend port 8443.
5. Один selector применяется ко всему Service, а не отдельно к каждому port.

Практический caveat: исходный kubia workload главы не подтверждён как реально обслуживающий HTTPS/8443. Поэтому end-to-end проверка второго port требует workload, который действительно слушает 8443: [Needs confirmation].

## Provenance

- Session affinity: p0174:c01
- Multi-port Service/Pod: p0175:c01–p0176:c01
