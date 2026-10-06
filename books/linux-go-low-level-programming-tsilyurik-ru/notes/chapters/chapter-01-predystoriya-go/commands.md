# Commands — глава 1 «Предыстория Go»

Только команды, присутствующие в chapter RAG.

| Команда | Класс | Назначение | Effect / risk | Verification | Rollback |
|---|---|---|---|---|---|
| `dnf list golang*` | read-only | Показать пакеты с префиксом golang в Fedora-окружении автора | Не изменяет систему | Просмотр списка | [Not applicable] |
| `dnf list golang* \| wc -l` | read-only | Посчитать строки результата | Не изменяет систему | Числовой вывод | [Not applicable] |
| `gcc --version` | read-only | Зафиксировать версию GCC | Не изменяет систему | Версия в stdout | [Not applicable] |
| `g++ --version` | read-only | Зафиксировать версию G++ | Не изменяет систему | Версия в stdout | [Not applicable] |
| `clang++ --version` | read-only | Зафиксировать версию Clang | Не изменяет систему | Версия в stdout | [Not applicable] |
| `go version` | read-only | Зафиксировать версию Go | Не изменяет систему | Версия в stdout | [Not applicable] |
| `javac --version` | read-only | Зафиксировать версию Java compiler | Не изменяет систему | Версия в stdout | [Not applicable] |
| `java --version` | read-only | Зафиксировать Java runtime | Не изменяет систему | Версия в stdout | [Not applicable] |
| `rustc --version` | read-only | Зафиксировать версию Rust compiler | Не изменяет систему | Версия в stdout | [Not applicable] |
| `python --version` | read-only | Зафиксировать версию Python | Не изменяет систему | Версия в stdout | [Not applicable] |
| `ls -l <artifact>` | read-only | Проверить наличие/размер артефакта | Не изменяет систему | Строка файла | [Not applicable] |
| `file fibo.class` | read-only | Проверить тип Java class-файла | Не изменяет систему | Определение типа | [Not applicable] |
| `gcc fibo_c.c -O3 -o fibo_c` | state-changing | Собрать C-вариант | Создаёт/заменяет `fibo_c` | `ls -l fibo_c` | [Needs confirmation] |
| `g++ fibo_cc.cc -O3 -o fibo_cc` | state-changing | Собрать C++-вариант | Создаёт/заменяет `fibo_cc` | `ls -l fibo_cc` | [Needs confirmation] |
| `clang++ ... fibo_cc.cc -o fibo_cl` | state-changing | Собрать C++ через Clang с путями окружения автора | Создаёт/заменяет `fibo_cl`; пути environment-specific | `ls -l fibo_cl` | [Needs confirmation] |
| `go build -o fibo_go fibo_go.go` | state-changing | Собрать Go-вариант | Создаёт/заменяет `fibo_go` | `ls -l fibo_go` | [Needs confirmation] |
| `javac fibo.java` | state-changing | Скомпилировать Java source | Создаёт `fibo.class` | `ls -l fibo.class`; `file fibo.class` | [Needs confirmation] |
| `rustc fibo_rs.rs` | state-changing | Собрать Rust-вариант | Создаёт `fibo_rs` | `ls -l fibo_rs` | [Needs confirmation] |
| `go run xxx.go` | workload-generating | Быстро скомпилировать и выполнить Go source по модели, описанной автором | Запускает программу; поведение зависит от кода | [Needs confirmation] | [Needs confirmation] |
| `time ./fibo_c 45` | workload-generating | Измерить выполнение C-варианта | CPU workload | Совпадение результата + time output | [Not applicable] |
| `time ./fibo_cc 45` | workload-generating | Измерить выполнение C++-варианта | CPU workload | Совпадение результата + time output | [Not applicable] |
| `time ./fibo_cl 45` | workload-generating | Измерить Clang/C++ вариант | CPU workload | Совпадение результата + time output | [Not applicable] |
| `time ./fibo_go 45` | workload-generating | Измерить Go-вариант | CPU workload | Совпадение результата + time output | [Not applicable] |
| `time java fibo 45` | workload-generating | Измерить Java-вариант | CPU workload + JVM | Совпадение результата + time output | [Not applicable] |
| `time ./fibo_rs 45` | workload-generating | Измерить Rust-вариант | CPU workload | Совпадение результата + time output | [Not applicable] |
| `time ./fibo.py 45` | workload-generating | Измерить Python-вариант | Длительный CPU workload в приведённом примере | Совпадение результата + time output | [Not applicable] |

## Environment-specific command

Источник приводит Clang-команду:

```bash
clang++ -O3 -I/usr/include/c++/11/ -I/usr/include/x86_64-linux-gnu/c++/11 \
  -L /usr/lib/gcc/x86_64-linux-gnu/11 fibo_cc.cc -o fibo_cl
```

Она жёстко привязана к путям GCC 11/Ubuntu из окружения автора. Автоматически переносить эти пути на другую систему нельзя.

## Benchmark acceptance rule from the chapter

Сравнивать следует эквивалентные реализации одного алгоритма, фиксируя версии инструментов. Автор отдельно предупреждает, что один benchmark не является общим рейтингом языков.
