# Ответы на вопросы для самопроверки — глава 4

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Как реализована обработка ошибок?

В chapter обычные ошибки возвращаются из functions/methods как значение типа `error`, обычно вместе с основным результатом. Caller проверяет `err != nil` и решает, как продолжить работу.

Source contrast: Go не использует `try/catch`; обработка строится вокруг возвращаемого `error` и явной проверки результата.

Provenance: `p0199:c01`, `p0205:c01`.

## 2. Что такое panic и для чего она используется?

Panic — аварийный execution path, который может привести к экстренному завершению приложения. Она возникает из runtime failures или может быть сгенерирована разработчиком явно.

Chapter examples: out-of-range slice access и nil pointer dereference.

Provenance: `p0199:c01–p0202:c01`.

## 3. Что такое error и для чего он используется?

`error` — interface:

~~~go
type error interface {
    Error() string
}
~~~

Он используется для передачи информации о recoverable failure caller-у, который может обработать её и продолжить execution.

Provenance: `p0199:c01`, `p0205:c01–p0206:c01`.

## 4. Разница между error и panic

По source framing:
- `error` — ожидаемый/обрабатываемый failure value; application может продолжить работу;
- `panic` — аварийная ситуация, способная завершить application, если её не перехватить через recovery mechanism.

Provenance: `p0199:c01`, `p0212:c01`.

## 5. Пользовательская panic

Используется built-in function:

~~~go
panic(v)
~~~

Source приводит signature `panic(v any)` и рекомендует передавать информативное message.

Provenance: `p0201:c01–p0202:c01`.

## 6. Перехват и обработка panic

Chapter использует `recover()` внутри deferred anonymous function:

~~~go
defer func() {
    if err := recover(); err != nil {
        // handle panic
    }
}()
~~~

В показанном example panic перехватывается, и приложение завершает работу штатно.

Provenance: `p0203:c01–p0205:c01`.

## 7. Panic и deferred functions

Deferred calls, зарегистрированные до точки panic, выполняются при выходе из function. Chapter связывает это с cleanup ресурсов.

Deferred call, расположенный после уже выполненного `panic`, не регистрируется и не выполнится.

Provenance: `p0202:c01–p0203:c01`.

## 8. Способы создания errors

Chapter explicitly показывает:

~~~go
errors.New("message")
fmt.Errorf("message")
~~~

`fmt.Errorf` позже также используется для wrapping lower-level error через `%w`.

Provenance: `p0205:c01–p0206:c01`, `p0209:c01`.

## 9. Пользовательский тип error

Нужно объявить type, обычно struct, и реализовать method:

~~~go
Error() string
~~~

Пример chapter — `DivError` с полями `Numerator`, `Denominator`, `Msg`.

Provenance: `p0208:c01–p0209:c01`.

## 10. Как определить вариант/type error и зачем?

Для известных package-level errors chapter использует `errors.Is(err, target)`, чтобы выбрать разные branches обработки.

Для structured custom error type chapter использует `errors.As(err, &target)`, чтобы получить конкретный error object и его fields.

Это нужно, когда разные errors требуют разной обработки.

Provenance: `p0207:c01–p0209:c01`.

## 11. Расширенные пользовательские errors

Объявляется custom struct с дополнительными fields и method `Error() string`, благодаря чему она удовлетворяет interface `error`.

Caller через `errors.As` получает typed error и может использовать structured context: numerator, denominator, message и другие данные.

Преимущество по source: больше информации и возможностей обработки, чем у одного text message.

Provenance: `p0208:c01–p0209:c01`, `p0212:c01`.

## 12. Вложенные errors

Это chain, где higher-level error добавляет context, сохраняя lower-level cause.

Chapter создаёт wrapping через:

~~~go
fmt.Errorf("DataBase error: %w", err)
~~~

И показывает извлечение lower-level error:

~~~go
errors.Unwrap(err)
~~~

Цель: передавать error до уровня, где достаточно context для корректной обработки, не теряя первопричину.

Provenance: `p0209:c01–p0211:c01`.
