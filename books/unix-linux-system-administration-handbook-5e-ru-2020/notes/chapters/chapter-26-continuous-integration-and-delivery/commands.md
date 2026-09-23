# Команды главы 26

Только команды и формы команд, подтверждённые RAG главы 26. Команды cloud/infrastructure stages относятся к демонстрационному UlsahGo pipeline и не являются универсальными production recipes.

## Read-only / verification

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| go test | Запустить unit tests UlsahGo | PASS/FAIL и failing test | workload-generating |
| curl <ulsahgo-url>/?edition=5 | Проверить valid application response | expected JSON / HTTP success | read-only |
| curl -vs <ulsahgo-url>/?edition=6 | Проверить invalid edition handling | expected HTTP 404 | read-only |
| curl <ulsahgo-url>/healthy | Проверить health endpoint | expected healthy response | read-only |
| terraform show terraform.tfstate | Просмотреть state после apply | created resources/attributes | read-only |

Глава использует grep/awk для извлечения image/IP identifiers из command output. OCR содержит неоднозначные quoting/regex details; exact copy/paste pipelines: [Needs confirmation].

## Build

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| go build | Собрать UlsahGo static binary | build succeeds and binary exists | workload-generating |
| make | Пример build step Jenkins для C-like project | successful build | workload-generating |
| make test | Пример Jenkins test step | tests pass | workload-generating |
| apt-get -y install golang-go | Установить Go toolchain на Jenkins system в примере | package installation succeeds | state-changing |

Build rule:
- build artifact создаётся один раз;
- последующие environments используют этот же artifact.

## Jenkins

Source-supported example:

~~~bash
docker run -p 8080:8080 --name jenkins jenkinsci/jenkins
~~~

Purpose:
- запустить Jenkins в Docker для изучения basic workflow.

Type:
- workload-generating.

Checks:
- container runs;
- Jenkins UI доступен через port 8080;
- initial admin password берётся из container output и немедленно меняется.

Production suitability этого single-container example: нет; chapter прямо ограничивает его учебным сценарием.

Pipeline shell steps supported by chapter:
~~~text
sh 'go test'
sh 'go build'
sh 'make'
sh 'make test'
sh 'deploy.sh'
~~~

Exact deploy.sh content is project-specific: [Needs confirmation].

## Packer image build

Chapter pipeline stage normalizes to:

~~~bash
packer build pipeline/packer/ulsahgo.json > packer.txt
~~~

Purpose:
- build DigitalOcean VM image;
- capture output containing resulting image ID.

Type:
- workload-generating.

Risks:
- temporary cloud resources are created;
- image/snapshot is created;
- API credentials are required.

Security:
- do not hardcode API token in template/repository;
- use Jenkins credential storage/environment variables.

Exact grep regex used to extract image ID is OCR-sensitive: [Needs confirmation].

## Terraform test environment

Chapter invokes an external script:

~~~bash
bash pipeline/testing/tf_testing.sh
~~~

Inside it, source supports the sequence:
~~~text
copy image-ID file into testing directory
cd pipeline/testing
terraform apply with do_image, do_token and ssh_fingerprint variables
terraform show terraform.tfstate
extract resulting IPv4 address
~~~

Normalized executable command family:
~~~bash
terraform apply -var do_image=<image-id> -var do_token=<secret> -var ssh_fingerprint=<fingerprint>
terraform show terraform.tfstate
~~~

Exact shell quoting in the printed listing is OCR-corrupted; use the canonical project script rather than reconstructing from memory.

Types:
- terraform apply: state-changing / workload-generating;
- terraform show: read-only.

Acceptance:
- expected droplet exists;
- state contains expected image/region/resources;
- resulting IP is available to integration tests.

## Integration tests and teardown

Chapter tests temporary droplet with curl and then destroys it.

Conceptual source-supported sequence:
~~~bash
curl ... <test-droplet-ip>:8000/?edition=5
curl ... <test-droplet-ip>:8000/?edition=6
terraform destroy -force
~~~

Expected:
- edition=5 → HTTP 200;
- edition=6 → HTTP 404.

terraform destroy -force:
- state-changing;
- destructive;
- removes temporary test infrastructure.

Before destroy:
- verify active Terraform directory/state;
- verify resources are test resources;
- production rollback is not implied.

Rollback after destroy:
- recreate from versioned Terraform configuration and known artifact;
- exact restore of prior instance: [Needs confirmation].

## Production environment

Chapter runs project script:

~~~bash
bash pipeline/production/tf_prod.sh
~~~

Purpose:
- create two DigitalOcean droplets and a load balancer.

Type:
- state-changing / workload-generating.

Checks:
- load balancer listens on port 80;
- backends serve on port 8000;
- /healthy returns HTTP 200;
- valid/invalid edition tests return expected codes.

Exact tf_prod.sh body is omitted by the chapter, so no invented command sequence is provided.

## Secrets

Jenkinsfile uses credentials() to expose:
- DigitalOcean API token;
- SSH fingerprint.

Operational boundary:
- secrets must not be committed to VCS;
- secret values from the book example are intentionally not reproduced here.

## Container-oriented CI/CD

Chapter gives conceptual workflow:
~~~text
build application in build container
→ create runtime container image
→ push image to registry
→ deploy through container orchestrator
~~~

No exact docker build/push or kubectl commands are provided in chapter 26. Do not import them from chapter 25 or model memory.

## Command classification summary

Read-only:
- curl health/response checks;
- terraform show.

Workload-generating:
- go test;
- go build;
- make / make test;
- Jenkins container start;
- Packer image build.

State-changing:
- package install;
- Terraform apply;
- Terraform destroy;
- production Terraform script.

Destructive:
- terraform destroy -force.

Unknown rollback:
- exact restoration after destroyed cloud instance: [Needs confirmation].
