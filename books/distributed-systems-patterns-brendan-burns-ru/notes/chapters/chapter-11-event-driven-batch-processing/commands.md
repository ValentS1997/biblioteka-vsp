# Команды и инструменты главы 11

Only commands explicitly supported by RAG `p0189:c01–p0204:c01`.

## Command inventory

| Command / action | Type | Purpose | Verification | Rollback |
|---|---|---|---|---|
| `helm init` | state-changing | initialize source-era Helm/Tiller | Kafka install follows | `[Needs confirmation]` |
| `helm repo add incubator ...` | state-changing local config | add incubator chart repository | repo available to Helm | `[Needs confirmation]` |
| `helm install --name kafka-service incubator/kafka` | state-changing | deploy Kafka | topics can be created | `[Needs confirmation]` |
| extracted topic-creation loop | state-changing, source-defective | create Photos shard topics | topic creation intended | `[Needs confirmation]` |
| producer `kubectl run` | workload-generating | publish messages to `photos-1` | consumer receives them | Not applicable |
| consumer `kubectl run` | read/workload action | consume `photos-1` from beginning | messages printed | Not applicable |

## Helm initialization

Source:

~~~bash
helm init
~~~

Then:

~~~text
helm repo add incubator
  http://storage.googleapis.com/kubernetes-charts-incubator

helm install --name kafka-service incubator/kafka
~~~

Classification:
- historical/book-era deployment flow;
- current Helm/Tiller/chart compatibility: `[Needs confirmation]`.

## Topic creation

RAG renders a loop beginning with:

~~~text
for x in 0 1 2; do
  kubectl run kafka --image=solsson/kafka:0.11.0.0
  --rm --attach --command -- ...
~~~

and ending around:

~~~text
--topic photos-$x done
~~~

Intent:
- create three topics corresponding to sharded outputs.

Parameters described by source:
- replication factor: `3`;
- partitions: `10`;
- ZooKeeper endpoint: `kafka-service-zookeeper:2181`.

Classification:
- `[Source extraction issue]`;
- not copy/paste-safe as rendered.

Exact executable loop: `[Needs confirmation]`.

## Producer

Source:

~~~text
kubectl run kafka-producer --image=solsson/kafka:0.11.0.0
--rm -it --command --   ./bin/kafka-console-producer.sh
  --broker-list kafka-service-kafka:9092   --topic photos-1
~~~

Purpose:
- open Kafka console producer for topic `photos-1`.

## Consumer

Source:

~~~text
kubectl run kafka-consumer --image=solsson/kafka:0.11.0.0
--rm -it --command --   ./bin/kafka-console-consumer.sh
  --bootstrap-server kafka-service-kafka:9092   --topic photos-1   --from-beginning
~~~

Purpose:
- consume messages from `photos-1` from beginning.

Line wrapping is preserved as source evidence, not normalized into guaranteed current syntax.

## Safety boundary

Do not add from model memory:
- current Helm/Kafka installation procedure;
- delete/uninstall commands;
- corrected topic loop;
- current Kafka image tags;
- consumer-group configuration;
- production topic sizing;
- security/TLS/SASL configuration.

Unsupported/current details remain `[Needs confirmation]`.
