# Контрольные материалы — глава 3

## Контрольный тест

### 1. Для каких workloads подходит container read-write layer?

A. С интенсивной записью.  
B. С интенсивным чтением.  
C. С небольшим объёмом данных.  
D. Ничего из вышеперечисленного.

### 2. Storage driver — это software, которое...

A. Создаёт images.  
B. Создаёт containers.  
C. Записывает данные на read-only layer container.  
D. Записывает данные на read-write layer container.

### 3. tmpfs позволяет...

A. Хранить данные в container.  
B. Хранить данные в volume.  
C. Хранить данные в памяти system.  
D. Хранить данные в storage system.

### 4. При bind mount...

A. Host file/directory монтируется в container.  
B. File/directory из Docker area монтируется в container.  
C. Host file/directory сопоставляется с памятью container.  
D. Host и container filesystem никак не связаны.

### 5. Volume drivers позволяют...

A. Только хранить данные на host disk.  
B. Только хранить данные в container filesystem.  
C. Выполнять дополнительные операции, например шифровать/переносить данные.  
D. Только сжимать данные.

### 6. Команда `docker run -it --name myalpine -v /root/test/:/test alpine:latest`...

A. Монтирует `/root/test/` из container в `/test` host.  
B. Монтирует `/root/test/` host в `/test` container.  
C. Не создаёт container, но выполняет mount host → container.  
D. Не создаёт container, но выполняет mount container → host.

### 7. Данные в container read-write layer...

A. Не исчезают при stop/start container.  
B. Теряются при stop/start container.  
C. Могут потеряться частично.  
D. Ничего из вышеперечисленного.

### 8. btrfs и zfs storage drivers можно использовать, если...

A. Backing filesystem поддерживает btrfs/zfs.  
B. Backing filesystem поддерживает direct-lvm.  
C. Backing filesystem поддерживает loopback-lvm.  
D. В backing filesystem также установлены/используются btrfs или zfs.

### 9. overlay2 предпочтительнее overlay, потому что...

A. Только быстрее.  
B. Только потому, что RHEL/CentOS поддерживают overlay2.  
C. В overlay2 решена проблема нехватки inode.  
D. Только потому, что overlay2 проще установить.

## Вопросы

1. Что такое storage driver?
2. Какие storage drivers доступны в Docker?
3. На какой Linux filesystem основаны drivers группы overlay?
4. Что означает diff в контексте image layers?
5. Как работает overlay2?
6. Что такое volume?
7. Что такое bind mount?
8. Чем volume отличается от bind mount?
9. Когда полезно использовать один volume для нескольких containers?
10. Что такое tmpfs?

## Provenance

- Test: `p0073:c01`–`p0074:c01`
- Source answer key: `p0074:c01`
- Open questions: `p0075:c01`
