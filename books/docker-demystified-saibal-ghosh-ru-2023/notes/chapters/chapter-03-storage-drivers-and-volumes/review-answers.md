# Ответы к контрольным материалам — глава 3

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | C |
| 2 | D |
| 3 | C |
| 4 | A |
| 5 | C |
| 6 | B |
| 7 | A |
| 8 | D |
| 9 | C |

Ключ `1-C, 2-D, 3-C, 4-A, 5-C, 6-B, 7-A, 8-D, 9-C` приведён в `p0074:c01`.

## Ответы на открытые вопросы

### 1. Что такое storage driver?

Storage driver — software, которое записывает данные на container read-write layer и определяет способ хранения images/containers на Docker host.

### 2. Какие storage drivers доступны в Docker?

Глава перечисляет `overlay2`, `aufs`, `Device Mapper`, `btrfs`, `zfs` и `vfs`, а также рассматривает `overlay` как более старый вариант OverlayFS.

### 3. На какой Linux filesystem основаны drivers группы overlay?

На OverlayFS — современной union filesystem, которую источник сравнивает с aufs.

### 4. Что означает diff в контексте image layers?

Каждый верхний layer хранит только отличия от lower layer(s). Это позволяет не дублировать неизменившееся содержимое.

### 5. Как работает overlay2?

Overlay2 объединяет lower read-only layers и upper writable layer через union mount. Нижние layers представлены `lowerdir`, изменения попадают в `upperdir`; `diff` содержит layer content/differences, `work` используется OverlayFS, а merged view представляет итоговую filesystem.

### 6. Что такое volume?

Volume — Docker-managed directory на host, смонтированный в container. Данные находятся за пределами container writable layer и сохраняются после удаления container.

### 7. Что такое bind mount?

Bind mount — сопоставление произвольного host file/directory с path внутри container. В отличие от volume, source path задаётся непосредственно в host filesystem и не обязан находиться в Docker-managed area.

### 8. Чем volume отличается от bind mount?

Volume управляется Docker и хранится в Docker area; bind mount указывает arbitrary host path. Volume также поддерживает volume drivers, а named volumes проще использовать и переиспользовать между containers.

### 9. Когда полезно использовать один volume для нескольких containers?

Когда нескольким containers нужно работать с одними и теми же данными. Источник прямо указывает совместное подключение одного volume как удобный вариант обмена данными.

### 10. Что такое tmpfs?

tmpfs — temporary mount, при котором files хранятся в host RAM, а не в container writable layer. После остановки container tmpfs удаляется и данные становятся недоступны.

## Operational map

```text
container write
├─ small/ephemeral → writable layer → storage driver
├─ persistent Docker-managed → volume
├─ persistent arbitrary host path → bind mount
└─ temporary memory-only → tmpfs
```

## Provenance

Ответы сформированы только по chapter RAG `p0059:c01`–`p0075:c01`. External sources и model-memory не использовались.
