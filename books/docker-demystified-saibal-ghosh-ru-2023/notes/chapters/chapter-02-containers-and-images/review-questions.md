# Контрольные материалы — глава 2

## Контрольный тест

### 1. Dockerfile — это:

A. Файл образа.  
B. Документ.  
C. Текстовый файл.  
D. Ничего из вышеперечисленного.

### 2. Container создаёт...

A. Тонкий слой только для чтения поверх image.  
B. Тонкий слой для чтения и записи под image.  
C. Тонкий слой только для чтения в любом месте image.  
D. Тонкий слой для чтения и записи поверх image.

### 3. Images хранятся в каталоге:

A. `/var/lib/docker/<драйвер_хранилища>`  
B. `/var/lib/docker/`  
C. `/var/lib/docker/netns`  
D. Ничего из вышеперечисленного.

### 4. Docker logs хранятся как JSON files в каталоге:

A. `/var/lib/docker/<id_контейнера>`  
B. `/var/lib/docker/containers/<id_контейнера>`  
C. `/var/lib/docker/containers`  
D. Ничего из вышеперечисленного.

### 5. Каждый layer image содержит:

A. Image ID.  
B. Имя image.  
C. Контрольную сумму (digest) SHA.  
D. Image ID и SHA digest.

### 6. Docker server — ключевой компонент Docker Engine, который включает:

A. containerd.  
B. dockerd.  
C. runC.  
D. Ничего из вышеперечисленного.

### 7. Copy-On-Write — механизм, который...

A. Позволяет копировать image.  
B. Создаёт копию данных/image только при изменении.  
C. Создаёт копию image только если image не изменён.  
D. Создаёт копию image только если image удалён.

### 8. Упорядоченный набор checksum/digest layers для сборки image — это:

A. Configuration object.  
B. SHA checksum.  
C. Filesystem.  
D. Ничего из вышеперечисленного.

### 9. Multi-stage build позволяет использовать:

A. Несколько `RUN` в одном Dockerfile.  
B. Несколько `CMD` в одном Dockerfile.  
C. Несколько Dockerfile вместе.  
D. Несколько `FROM` в одном Dockerfile.

### 10. Container имеет status Dead, если не удалось...

A. Загрузить container.  
B. Запустить container.  
C. Корректно удалить container, потому что resources были недоступны.  
D. Корректно создать container.

## Вопросы

1. Что такое container?
2. Что такое images и как они связаны с containers?
3. В каких состояниях может находиться container?
4. Что означает immutable применительно к images?
5. Как наиболее эффективно управлять logs?
6. Что такое Dockerfile?
7. Что такое configuration object в image?
8. Что такое build cache?
9. Что такое multi-stage build?
10. Что такое intermediate image?

## Provenance

- Test: `p0056:c01`–`p0057:c01`
- Source answer key + open questions: `p0058:c01`
