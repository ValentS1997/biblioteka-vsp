# Шпаргалка: application configuration

## 1. Configuration layers

~~~text
container image defaults
  ↓
Pod command / args
  ↓
env variables
  ↓
ConfigMap
  ↓
Secret
~~~

Выбор зависит от sensitivity и lifecycle.

## 2. command / args

Source mapping:

| Docker | Kubernetes |
|---|---|
| ENTRYPOINT | command |
| CMD | args |

args позволяет переопределить arguments без пересборки image.

Source note: command/args после создания Pod не обновляются.

## 3. Environment variables

Pod container env:

~~~text
env:
- name: INTERVAL
  value: "30"
~~~

Плюс:
- простой способ configuration.

Минус:
- hardcoded environment-specific data остаётся в Pod spec;
- env list после создания Pod не обновляется.

## 4. ConfigMap

Использовать для non-sensitive configuration.

Source create patterns:

~~~bash
kubectl create configmap fortune-config --from-literal=sleep-interval=25
kubectl create configmap my-config --from-file=config-file.conf
kubectl create configmap my-config --from-file=customkey=config-file.conf
kubectl create configmap my-config --from-file=/path/to/dir
~~~

Read-only:

~~~bash
kubectl get configmap fortune-config -o yaml
~~~

## 5. Consume ConfigMap

### One env variable

~~~text
valueFrom:
  configMapKeyRef:
    name: fortune-config
    key: sleep-interval
~~~

### All entries as env

~~~text
envFrom:
- configMapRef:
    name: my-config-map
~~~

### As files

~~~text
volumes:
- name: config
  configMap:
    name: fortune-config
~~~

## 6. ConfigMap file controls

items:
- select specific keys;
- map key to chosen file path.

subPath:
- mount one file without hiding existing directory content;
- source-era caveat: single-file mount does not receive ConfigMap updates.

defaultMode:
- controls permissions of files in volume.

## 7. ConfigMap update behavior

Source update:

~~~bash
kubectl edit configmap fortune-config
~~~

Verification:

~~~bash
kubectl exec fortune-configmap-volume -c web-server -- cat /etc/nginx/conf.d/my-nginx-config.conf
~~~

Application reload example:

~~~bash
kubectl exec fortune-configmap-volume -c web-server -- nginx -s reload
~~~

Important:
- file update is not immediate;
- files update atomically;
- different Pods may temporarily see different versions;
- application must reload configuration itself.

## 8. Secret

Use for sensitive data.

Source contrasts:
- ConfigMap YAML values appear as plain text.
- Secret data values appear Base64-encoded.
- Base64 is encoding, not encryption.

stringData:
- write-only convenience field for plain text;
- reads back under data as Base64.

## 9. Secret delivery

Preferred source pattern:

~~~text
Secret
  ↓ secret volume
decoded file
  ↓
application
~~~

Alternative:

~~~text
secretKeyRef → env variable
~~~

Source warning: env variables may leak through logs/crash reports and child processes.

## 10. Secret storage check

Source:

~~~bash
kubectl exec fortune-https -c web-server -- mount | grep certs
~~~

Expected source example: tmpfs mounted read-only.

## 11. Private registry

Create docker-registry Secret:

~~~bash
kubectl create secret docker-registry mydockerhubsecret   --docker-username=<username>   --docker-password=<password>   --docker-email=<email>
~~~

Security:
- credentials are sensitive;
- do not paste real password into shared logs/history.

Pod relation:

~~~text
imagePullSecrets:
- name: mydockerhubsecret
~~~

## 12. Decision table

| Need | Source mechanism |
|---|---|
| simple process flag | args |
| simple non-secret scalar | env |
| reusable non-secret config | ConfigMap |
| non-secret config files | ConfigMap volume |
| sensitive file/data | Secret |
| private registry credentials | docker-registry Secret |

## Acceptance checks

- configuration source exists;
- Pod references correct ConfigMap/Secret name and key;
- mounted files/variables contain expected values;
- application has reloaded if required;
- sensitive data is not printed unnecessarily;
- imagePullSecrets points to registry credential Secret.
