# Упражнения главы 10

В проверенной границе найдено одно явно обозначенное упражнение.

## Упражнение 1 — StatefulSet при аварийном отключении worker node

Источник: p0378:c01–p0382:c01.

Цель — увидеть, почему StatefulSet не создаёт replacement Pod, пока control plane не может доказать, что старый stateful instance действительно прекратил работу.

Source scenario:

1. использовать multi-node GKE cluster;
2. выбрать worker node, на котором работает один StatefulSet Pod;
3. отключить network interface eth0 этого node;
4. наблюдать переход node в NotReady и Pod в Unknown/Terminating;
5. попробовать обычное удаление Pod;
6. понять, почему replacement не появляется;
7. только после подтверждения, что old node действительно не работает, выполнить force-delete;
8. наблюдать создание replacement Pod с той же stable identity;
9. восстановить node source-supported reset command.

## High-risk boundary

Source failure injection:

~~~bash
sudo ifconfig eth0 down
~~~

Source force-delete:

~~~bash
kubectl delete po kubia-0 --force --grace-period 0
~~~

Обе операции опасны.

Force-delete допустим только если старый экземпляр гарантированно больше не работает и не вернётся. Иначе возможны два процесса с одинаковой identity/storage.

## Provenance

- Exercise introduction: p0378:c01
- network failure: p0379:c01
- normal deletion behavior: p0380:c01–p0381:c01
- force deletion and recovery: p0381:c01–p0382:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
