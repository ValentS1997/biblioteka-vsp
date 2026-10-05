# Контрольные материалы — глава 5

## Контрольный тест

### 1. При помощи чего Docker Swarm позволяет быстро развёртывать приложения на нескольких hosts?

A. Минимального API.  
B. Гипервизора.  
C. Многофункционального API.  
D. Безопасных networks.

### 2. Docker Swarm — это:

A. Backup solution.  
B. Orchestrator.  
C. Load balancer.  
D. Orchestrator и load balancer.

### 3. Docker Swarm автоматически создаёт:

A. Overlay network.  
B. Overlay network и network bridge.  
C. Network bridge и host network.  
D. Physical network.

### 4. В каких режимах можно создавать replicas?

A. Universal и global.  
B. Universal и replicated.  
C. Replicated и global.  
D. Режим указать нельзя.

### 5. Как реализовать autolock в Docker Swarm?

A. Изменить autolock на true.  
B. Autolock включён по умолчанию.  
C. Изменить autolock на true и restart Docker.  
D. Изменить autolock на true и сменить keys.

### 6. Что происходит при global mode?

A. При добавлении node новая replica/task создаётся автоматически.  
B. Replica создаётся вручную.  
C. На новых nodes tasks создавать нельзя.  
D. Новые nodes добавлять нельзя.

### 7. Когда Swarm locked...

A. Node можно добавить только после unlock.  
B. Node можно добавить сразу.  
C. Node можно добавить, если доступен любой manager.  
D. Node можно добавить только как manager.

### 8. Если node переведён в DRAIN...

A. Existing tasks остаются, но новых не будет.  
B. Existing tasks останавливаются и больше нигде не запускаются.  
C. Existing tasks останавливаются и пересоздаются на ACTIVE nodes.  
D. Existing tasks продолжаются и новые тоже принимаются.

## Вопросы

1. Что такое Docker Swarm?
2. Что такое service в Docker Swarm? Чем service отличается от task/replica?
3. Что такое routing mesh и как она работает?
4. Как можно lock/unlock Docker Swarm?
5. Что такое consensus в контексте Docker Swarm?
6. В чём разница между replicated и global modes?
7. Что такое overlay networks и как они работают в Docker Swarm?
8. Как опубликовать пользовательские ports/protocols в Docker Swarm?

## Provenance

- Test: `p0111:c01`–`p0112:c01`
- Source answer key: `p0112:c01`
- Open questions / key terms: `p0113:c01`
