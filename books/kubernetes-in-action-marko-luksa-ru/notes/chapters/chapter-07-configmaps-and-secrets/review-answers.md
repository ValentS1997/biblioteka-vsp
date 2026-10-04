# Ответы к упражнениям главы 7

Это RAG-grounded решения, не официальный издательский answer key.

## Упражнение 1 — Pod с args

Source relation:

~~~text
Docker CMD      → Kubernetes args
Docker ENTRYPOINT → Kubernetes command
~~~

Source manifest показывает container args array. Точный manifest уже приведён в chapter; acceptance result:

- Pod создаётся;
- main process получает указанные arguments;
- image rebuild не требуется;
- command/args Pod после создания не обновляются.

Source example использует fortune image с interval argument. Exact create command line для этого Pod в retrieved RAG не выделена отдельно: [Needs confirmation].

## Упражнение 2 — Private image

Создать registry Secret по source pattern, но не помещать реальные credentials в shared artifact:

~~~bash
kubectl create secret docker-registry mydockerhubsecret   --docker-username=<username>   --docker-password=<password>   --docker-email=<email>
~~~

Pod spec relation:

~~~text
spec:
  imagePullSecrets:
  - name: mydockerhubsecret
  containers:
  - image: <private-image>
    name: main
~~~

Exact private image name/tag зависит от user's registry: [Needs confirmation].

Acceptance:
- Secret существует;
- Pod references correct Secret name;
- image pull succeeds;
- Pod starts instead of failing on registry authentication.

Security:
- credentials are sensitive;
- command-line password may leak into shell history/process inspection;
- real credential values must not be committed.

## Provenance

- Args task: p0255:c01
- Registry Secret command: p0285:c01
- imagePullSecrets task: p0286:c01
