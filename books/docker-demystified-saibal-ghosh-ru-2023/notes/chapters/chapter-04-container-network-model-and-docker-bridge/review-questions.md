# Контрольные материалы — глава 4

## Контрольный тест

### 1. Linux network bridge — это:

A. Устройство уровня 1.  
B. Устройство уровня 3.  
C. Устройство уровня 2.  
D. Не относится к модели OSI.

### 2. Network isolation containers реализуется при помощи...

A. Container Network Model.  
B. veth pair.  
C. Network namespace.  
D. Network drivers.

### 3. Если на Linux host запущен Docker Engine, автоматически...

A. Создаётся network bridge.  
B. Создаётся veth pair.  
C. Создаются network namespaces.  
D. Устанавливаются built-in network drivers.

### 4. Network sandbox полностью изолирован, за исключением...

A. Network stack.  
B. Endpoints.  
C. IPAM drivers.  
D. Containers.

### 5. Libnetwork — это:

A. Network interface.  
B. Repository built-in Docker drivers.  
C. Реализация IPAM.  
D. Реализация CNM.

### 6. Какой network driver позволяет подключать несколько hosts без дополнительной конфигурации по описанию главы?

A. MACVLAN.  
B. Overlay.  
C. Bridge.  
D. Ничего из вышеперечисленного.

## Вопросы

1. Что такое network namespace?
2. Как работает veth pair?
3. Нарисуйте и объясните Container Network Model.
4. Что представляет собой Libnetwork и каковы её функции?
5. В чём заключается концепция Linux network bridge?
6. Что такое network drivers?

## Provenance

- Test: `p0085:c01`–`p0086:c01`
- Source answer key + open questions: `p0086:c01`
