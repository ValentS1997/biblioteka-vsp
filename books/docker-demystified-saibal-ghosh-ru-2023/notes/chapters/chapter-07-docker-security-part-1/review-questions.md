# Контрольные материалы — глава 7

## Контрольный тест

### 1. Сколько kernel namespaces использует Docker на Linux по source?

A. 4  
B. 5  
C. 6  
D. 7

### 2. Какой namespace позволяет нескольким containers использовать одинаковый internal port при разных host ports?

A. PID  
B. NET  
C. Kernel  
D. IPC

### 3. Для какой OS family source связывает AppArmor?

A. RHEL  
B. CentOS  
C. Fedora  
D. Ubuntu

### 4. На каком уровне source описывает загрузку/включение SELinux для Docker?

A. Демон  
B. Container  
C. Swarm  
D. Host

### 5. При создании container большинство Linux capabilities...

A. Изменены  
B. Недоступны  
C. Доступны  
D. Ограничены

### 6. Какую задачу выполняет SELinux в формулировке теста?

A. Performance tuning  
B. Ограничение syscalls  
C. Ограничение user calls  
D. Метки objects/files/networks и т. д.

### 7. Отказ по DAC имеет приоритет...

A. Над AppArmor  
B. Перед root  
C. Над SELinux  
D. Перед privileged user

### 8. Docker позволяет контролировать consumption ресурсов...

A. Network и CPU  
B. Memory и CPU  
C. Network и memory  
D. Memory и users

## Вопросы

1. Какие security options предоставляет OS для Docker?
2. Что такое kernel namespaces?
3. В чём концепция cgroups?
4. Что такое MAC и чем он отличается от DAC?
5. Что такое seccomp?
6. Что такое capabilities?
7. Как Docker containers работают с capabilities?
8. Какие преимущества SELinux даёт Docker containers?
9. Как настроить AppArmor profile для container?
10. Какими способами source контролирует memory и CPU consumption?

## Provenance

- Test: `p0182:c01`–`p0183:c01`
- Source answer key + questions: `p0183:c01`
