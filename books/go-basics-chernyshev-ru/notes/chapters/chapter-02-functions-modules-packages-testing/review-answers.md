# Ответы на вопросы для самопроверки — глава 2

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Для чего используются функции?

Для повторного использования кода, уменьшения copy/paste и создания уровней абстракции. В chapter functions также рассматриваются как first-class values.

Provenance: `p0101:c01`.

## 2. Точка входа

Top-level function `main` в executable package `main`.

Provenance: `p0117:c01–p0118:c01`.

## 3. `return`

`return` завершает function и возвращает caller значение или значения, соответствующие объявленной signature. Named returns позволяют использовать bare `return`.

Provenance: `p0103:c01–p0104:c01`.

## 4. Область видимости

Глава описывает lexical scope. Inner block видит значения outer scope, но outer block не видит variables, объявленные только внутри inner block. Повторное имя во внутреннем block shadow-ит внешнее.

Provenance: `p0109:c01–p0110:c01`.

## 5. Вызов функции через переменную

Присвоить function переменной и вызвать переменную:

~~~go
myFunc := add
fmt.Println(myFunc(3, 5))
~~~

Provenance: `p0110:c01`.

## 6. Function как argument

Да. Type argument задаётся function signature.

~~~go
func sub(c, a, b int, addFunc func(int, int) int) int {
    return c - addFunc(a, b)
}
~~~

Provenance: `p0110:c01–p0111:c01`.

## 7. `type`

В chapter `type` используется для объявления собственных named types/aliases, чтобы сокращать сложные типы и function signatures.

Provenance: `p0108:c01`, `p0111:c01`.

## 8. Anonymous functions

Это functions без явного имени. Они могут быть assigned variable, passed as argument, returned from function или invoked inline.

Provenance: `p0104:c01`, `p0111:c01–p0112:c01`.

## 9. Function возвращает function?

Да. Это основа примеров closures: outer function возвращает nested function, которая может использовать captured values.

Provenance: `p0112:c01–p0113:c01`.

## 10. Способы передачи аргументов

Chapter рассматривает:
- по значению — function получает copy;
- через pointer — копируется address, а dereference позволяет менять caller value.

Provenance: `p0105:c01–p0107:c01`.

## 11. Варианты объявления functions

Показаны functions:
- без arguments/returns;
- с positional arguments;
- с одним return;
- с multiple returns;
- с named returns;
- variadic;
- anonymous.

Provenance: `p0101:c01–p0104:c01`, `p0111:c01`.

## 12. Сколько values можно вернуть?

Function может вернуть одно или несколько values. Multiple return values должны быть распакованы caller-ом; ненужное value можно принять в `_`. Returns могут быть named.

Provenance: `p0103:c01–p0104:c01`.

## 13. Closure

Closure — nested/returned function, которая сохраняет доступ к variables enclosing lexical scope. Это позволяет создавать functions, параметризованные состоянием outer function, и динамические handlers.

Provenance: `p0112:c01–p0114:c01`.

## 14. Виды recursion

- direct: function вызывает себя;
- indirect: function вызывает другую function, которая затем вызывает первую.

Обе требуют exit condition.

Provenance: `p0114:c01–p0115:c01`.

## 15. Generator functions

Для lazy generation последовательности по запросу. Chapter implementation использует goroutine + channel.

Provenance: `p0115:c01–p0116:c01`.

## 16. Slice/array или generator?

Chapter прямо рекомендует generator как альтернативу, когда values нужно создавать лениво и не хранить всю sequence в памяти. Для уже materialized collection используются slices/arrays. Более детальная decision matrix в source не формализована.

Provenance: `p0115:c01–p0116:c01`.

## 17. Возвращение результатов function

Основной способ — explicit `return` одного/нескольких values. Chapter также показывает изменение caller-provided result через pointer argument. В сравнительном примере explicit bool return признан более понятным по signature.

Provenance: `p0103:c01–p0104:c01`, `p0107:c01–p0108:c01`.

## 18. Value vs reference/pointer

По значению передаётся copy и исходный value не меняется. Через pointer передаётся address; dereference позволяет изменить исходный object.

Provenance: `p0105:c01–p0107:c01`.

## 19. Module и package

Package — namespace/code organization unit. Module — набор связанных packages и dependency-management boundary, описанный через `go.mod`.

Provenance: `p0117:c01–p0118:c01`.

## 20. Типы packages

- executable: только `package main`, обязан иметь `main`;
- utility: остальные reusable packages.

Provenance: `p0117:c01`.

## 21. Типы modules

- executable module: содержит executable package `main`;
- non-executable/service module: не содержит executable package и используется как dependency.

Provenance: `p0118:c01`.

## 22. `go.mod` и `go.sum`

`go.mod` хранит module import path, Go version и external dependency requirements. `go.sum` используется для подтверждения, что dependency modules имеют ожидаемое содержимое.

Provenance: `p0118:c01`.

## 23. Инициализация project/module

Chapter command:

~~~bash
go mod init golang/first
~~~

Provenance: `p0118:c01–p0119:c01`.

## 24. Подключение external module

Два показанных способа:
1. добавить `require module version` в `go.mod`, затем `go mod download`;
2. выполнить `go get <module>`.

Provenance: `p0120:c01–p0122:c01`.

## 25. `go get`

В chapter используется для добавления external dependency в module и обновления module metadata.

Provenance: `p0121:c01–p0123:c01`, `p0143:c01`.

## 26. `go mod tidy`

Добавляет missing requirements и удаляет unused dependencies. В example удаляет неиспользуемый `golang.org/x/time/rate` из `go.mod`.

Provenance: `p0122:c01–p0123:c01`, `p0150:c01`.

## 27. Версии modules и новый package

Modules используют semantic versioning `vMAJOR.MINOR.PATCH`: major — incompatible API changes, minor — compatible functionality, patch — compatible fixes.

Новый package создаётся как directory/files с `package <name>`; в executable root используется `main`, utility directory обычно совпадает с package name.

Provenance: `p0123:c01–p0125:c01`.

## 28. `vendor`

Каталог хранит copies external dependencies внутри project. Создаётся:

~~~bash
go mod vendor
~~~

Если external dependencies отсутствуют, directory не создаётся.

Provenance: `p0124:c01`.

## 29. Доступность functions другого package

Import package и обращение через его name. Identifier должен начинаться с uppercase, чтобы быть exported. Lowercase function доступна только внутри своего package.

Provenance: `p0126:c01–p0128:c01`.

## 30. Другое имя imported package

Использовать import alias:

~~~go
import pack "golang/first/another_package"
~~~

Provenance: `p0128:c01–p0129:c01`.

## 31. Локальный module

Инициализировать local module и в caller module добавить `replace` + `require`:

~~~text
replace golang/second => ../second
require golang/second <version>
~~~

Затем import package из local module обычным способом.

Provenance: `p0129:c01–p0131:c01`.

## 32. Для чего testing

Для обнаружения defects до release, проверки behavior и автоматизации verification. Chapter рассматривает unit/component/integration/end-to-end testing.

Provenance: `p0132:c01`.

## 33. Как хранить test code

Chapter сначала рекомендует отдельную `test` directory и `_test` postfix для test files. В coverage section tests временно переносятся в tested package для корректного coverage example; source затем отмечает, что при росте complexity тесты лучше снова выносить в отдельный package.

Provenance: `p0132:c01`, `p0139:c01–p0140:c01`.

## 34. TDD

Test-Driven Development: test пишется до implementation. Chapter связывает подход с высоким coverage, автоматизацией tests и ограничением избыточной implementation.

Provenance: `p0132:c01`.

## 35. Built-in testing package

`testing`.

Provenance: `p0133:c01`.

## 36. Code coverage

Метрика доли package code, выполняемой tests, в процентах. Chapter показывает summary coverage, profile file и HTML visualization:

~~~bash
go test ./... -cover
go test ./... -coverprofile="coverage.out"
go tool cover -html="coverage.out"
~~~

Provenance: `p0138:c01–p0140:c01`.

## 37. Table-driven test

Cases table содержит inputs и expected results; один loop выполняет target function для каждой комбинации. Подходит, когда одну function надо проверить на многих наборах, включая edge cases.

Provenance: `p0136:c01–p0137:c01`.

## 38. Нюансы tests в Go

По material главы:
- test file использует `_test.go` naming;
- test function starts with `Test`;
- принимает только `*testing.T`;
- failure можно сообщить через `t.Errorf`;
- нужно проверять разные values и boundary cases;
- package placement влияет на coverage example;
- table-driven cases можно разделить через `t.Run`.

Provenance: `p0132:c01–p0140:c01`.

## 39. Performance testing

Используется для измерения speed и сравнения implementations. Benchmark function начинается с `Benchmark`, принимает `*testing.B` и запускает target code `b.N` раз.

Commands chapter:

~~~bash
go test ./... -bench=.
go test ./... -bench=Pow2
go test ./... -bench=Pow2 -benchmem -benchtime=100000x
~~~

Provenance: `p0141:c01–p0142:c01`.
