# Шпаргалка: CI/CD

## 1. Термины

Continuous Integration:
~~~text
commit
→ merge/integration branch
→ automatic build
→ automatic tests
~~~

Continuous Delivery:
~~~text
CI
→ automatic deployment to non-production
→ release-ready artifact
~~~

Continuous Deployment:
~~~text
CI/CD
→ automatic production deployment
~~~

Human approval может оставаться отдельной boundary.

## 2. Source of truth

Хранить в VCS:
- application code;
- infrastructure code;
- configuration;
- Jenkinsfile;
- deployment scripts;
- supporting documentation where appropriate.

Rule:
~~~text
no hidden manual state
~~~

## 3. Build once

~~~text
source
→ one build
→ one immutable artifact
→ dev
→ staging
→ production
~~~

Не пересобирать artifact между environments.

## 4. Commit discipline

Каждая integration commit:
~~~text
commit
→ trigger pipeline
→ build
→ tests
~~~

Малые частые commits:
- упрощают fault isolation;
- дают быстрый feedback.

## 5. Broken pipeline rule

~~~text
failed build/test
→ stop promotion
→ diagnose
→ fix pipeline/code
→ resume
~~~

Production не должен быть достижим при failed tests.

## 6. Environments

Development:
- integration;
- infrastructure changes;
- obvious-failure detection.

Staging/test:
- manual/automated validation;
- business/security testing.

Production:
- end users;
- highest availability/security requirements.

## 7. Environment parity

Чем ближе lower environment к production:
- тем надёжнее pre-production validation.

Differences still exist:
- credentials;
- URLs;
- hostnames;
- scale.

Управлять ими через authoritative configuration source.

## 8. Production-like data

Если production data используются ниже:
- anonymize sensitive user data;
- preserve meaningful size/content where feasible.

## 9. Feature flags

~~~text
deploy code disabled
→ test in lower env
→ enable by config
~~~

Advantage:
- activation separated from deployment;
- bad feature can be disabled without new release.

## 10. Pipeline stages

Basic mature flow:
~~~text
build
→ tests
→ deploy dev
→ tests
→ deploy staging
→ tests
→ deploy prod
~~~

Build → candidate after tests → release after production.

## 11. Artifact types

Examples from chapter:
- JAR/WAR;
- static binary;
- RPM/DEB;
- Python/Ruby package;
- container image;
- VM image;
- EXE.

Artifact repository must be reachable by deployment systems.

## 12. Testing layers

Static analysis:
- syntax;
- duplication;
- coding rules;
- security/complexity.

Unit:
- function/method behavior.

Integration:
- application + external dependencies.

Acceptance:
- user-facing workflows.

Performance:
- realistic traffic/load.

Infrastructure:
- expected config/services.

## 13. Test execution

Prefer parallel tests where safe.

Do not parallelize blindly when:
- tests depend on each other;
- tests mutate shared state;
- tests interfere with same environment.

## 14. Deployment methods

Source-supported classes:
- shell + SSH;
- configuration management;
- container orchestrator API;
- dedicated deploy tools;
- cloud deployment services.

## 15. Immutable deployment

~~~text
old server/image
→ create new server/image
→ validate
→ switch traffic
→ retire old
~~~

Avoid in-place mutation where infrastructure permits replacement.

## 16. Zero-downtime strategies

Blue-green:
~~~text
blue live
→ build/test green
→ switch traffic
~~~

Rolling:
~~~text
remove one node
→ update
→ return to rotation
→ repeat
~~~

Canary:
~~~text
small traffic share
→ observe telemetry
→ expand or revert
~~~

## 17. Jenkins role

Jenkins:
- orchestrates;
- triggers;
- coordinates stages;
- records logs/status.

External tools actually:
- compile;
- test;
- package;
- deploy.

## 18. Jenkins distributed builds

~~~text
Jenkins coordinator
→ labeled agents
→ build/test workspaces
~~~

Agents can be:
- containers;
- VMs;
- ephemeral cloud systems.

## 19. Pipeline as code

~~~text
repository
├── application code
├── Jenkinsfile
└── pipeline scripts/config
~~~

Benefit:
- reviewable;
- reproducible;
- recoverable;
- versioned.

## 20. Minimal Jenkinsfile concept

~~~text
Checkout
→ Unit tests
→ Build
→ Image build
→ Test infrastructure
→ Integration test
→ Production infrastructure
→ Production test
~~~

## 21. UlsahGo commands

~~~bash
go test
go build
~~~

Verification:
- tests PASS;
- build succeeds.

## 22. Jenkins learning instance

~~~bash
docker run -p 8080:8080 --name jenkins jenkinsci/jenkins
~~~

Use:
- learning/basic workflow.

Not presented by chapter as production architecture.

## 23. Packer stage

~~~text
binary
→ Packer
→ cloud VM image
→ image ID
~~~

Image ID is propagated to later deployment stages.

## 24. Secret handling

Bad:
~~~text
API token inside Packer template
→ committed to repository
~~~

Good:
~~~text
Jenkins Credentials Store
→ environment variable
→ pipeline stage
~~~

Never store secrets in VCS.

## 25. Terraform test environment

~~~text
image ID
+ credentials
→ terraform apply
→ temporary droplet
→ test
→ terraform destroy
~~~

The environment is disposable and reproducible.

## 26. Integration check

Chapter example validates:
- valid request → HTTP 200;
- invalid request → HTTP 404;
- /healthy → healthy response.

## 27. Production example

~~~text
same tested image
→ two droplets
→ load balancer
→ /healthy backend check
→ HTTP validation
~~~

Same artifact is promoted instead of rebuilt.

## 28. Destructive action

~~~bash
terraform destroy -force
~~~

Before:
- verify state directory;
- verify resources are temporary/test;
- verify no required data.

Rollback:
- recreate from versioned config/artifact;
- exact instance restoration: [Needs confirmation].

## 29. Containers in CI/CD

Three patterns:
- CI/CD server/agents in containers;
- build/test inside containers;
- runtime container image as artifact.

Build image and runtime image should differ when compiler/test tooling is unnecessary at runtime.

## 30. Container artifact flow

~~~text
build container
→ application
→ runtime image
→ registry
→ orchestrator
~~~

## 31. Acceptance model

A healthy pipeline demonstrates:
- traceable source revision;
- reproducible artifact;
- passing gates;
- environment-aware config;
- protected secrets;
- observable deploy;
- reproducible rollback/recreate path.
