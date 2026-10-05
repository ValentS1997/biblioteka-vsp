# Контрольные материалы — глава 8

## Контрольный тест

### 1. База данных CVE содержит:

A. Все исправления vulnerabilities, доступные для Docker.  
B. Последние исправления vulnerabilities, доступные для Docker.  
C. Все исправления security violations в Docker.  
D. Все известные vulnerabilities с регулярными updates.

### 2. Какие задачи выполняет Universal Control Plane?

A. Повышает performance.  
B. Динамически применяет vulnerability fixes.  
C. Обеспечивает centralized management.  
D. Поддерживает system stability.

### 3. Верное утверждение о Docker Trusted Registry:

A. DTR входит в Docker Community Edition.  
B. DTR — enterprise solution для хранения images.  
C. DTR повышает performance.  
D. DTR не предоставляет security-risk information.

### 4. Выберите верное утверждение:

A. В Docker и Kubernetes нет predefined roles.  
B. В Docker есть predefined roles, а в Kubernetes нет.  
C. В Docker и Kubernetes есть predefined roles.  
D. В Kubernetes есть predefined roles, а в Docker нет.

### 5. Что такое организация?

A. Group of users с одинаковым набором permissions/privileges.  
B. Такая group обязательно должна входить в team.  
C. Users одной team могут иметь разные permissions/privileges.  
D. Ничего из перечисленного.

### 6. Какие environment variables автоматически обновляет Client Bundle?

A. `docker_host, docker_certification_path, docker_tls_verify`  
B. `docker_host_path, docker_cert_path, docker_tls_verify`  
C. `docker_host, docker_cert_path, docker_tls_verify`  
D. `docker_host, docker_cert_path, docker_tls_verification`

### 7. Как source предлагает обновить CVE database без Internet?

A. JAR update file.  
B. Script update file.  
C. TAR update file.  
D. ZIP update file.

### 8. Что не является default collection?

A. `/Shared/Legacy/`  
B. `/Shared/Private/`  
C. `/System`  
D. `/System/Shared/`

### 9. Что не является default role?

A. Role Only.  
B. View Only.  
C. Full Control.  
D. Restricted Control.

### 10. Верное утверждение о Client Bundle:

A. Создаёт private/public key pair, authorizing requests to UCP.  
B. Создаёт private/secondary key pair for UCP.  
C. Public key authorizes only DTR requests.  
D. Public key authorizes direct Docker Engine requests.

## Вопросы

1. Из каких компонентов состоит Docker Enterprise Edition?
2. Каковы основные функции UCP?
3. Каковы основные функции DTR?
4. Для чего нужен Client Bundle?
5. Какие environment variables обновляет Client Bundle?
6. Что такое CVE?
7. Что такое RBAC?
8. Что означают users, organizations и teams в source RBAC model?
9. Что такое role?
10. Что такое collection?

## Provenance

- Test: `p0210:c01`–`p0212:c01`
- Source answer key: `p0212:c01`
- Open questions/key terms: `p0212:c01`
