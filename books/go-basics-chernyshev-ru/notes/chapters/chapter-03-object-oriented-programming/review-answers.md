# Ответы на вопросы для самопроверки — глава 3

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Объект, класс и характеристики

В source framing класс описывает объект предметной области и объединяет его состояние и поведение. Объект/экземпляр — конкретное созданное представление такого описания. Его основные характеристики в главе раскрываются через состояние и поведение.

Для Go chapter вместо классического класса использует struct для state и methods для behavior.

Provenance: `p0153:c01–p0154:c01`.

## 2. Состояние объекта

Состояние — данные/характеристики объекта. В классическом class framing оно хранится в fields/variables class; в Go chapter состояние хранится в fields структуры.

Provenance: `p0153:c01–p0155:c01`.

## 3. Поведение объекта

Поведение — операции над объектом. В классическом class framing это methods; в Go chapter поведение реализуется methods, связанными с named types/structs.

Provenance: `p0153:c01`, `p0161:c01–p0162:c01`.

## 4. Основные принципы ООП

Chapter framing перечисляет инкапсуляцию, наследование и полиморфизм как базовые ООП-концепции.

Provenance: `p0153:c01`.

## 5. Реализация ООП-принципов в Go

По chapter framing:
- state → structs;
- behavior → methods;
- encapsulation/hiding → package boundary + exported/unexported identifiers;
- inheritance-like reuse → composition through embedded structs;
- runtime polymorphism → interfaces.

Provenance: `p0153:c01`, `p0164:c01–p0169:c01`.

## 6. Struct

Struct — пользовательский type, объединяющий fields разных types. Глава использует его для описания и хранения state объекта предметной области.

Provenance: `p0153:c01–p0155:c01`.

## 7. Экземпляр структуры

Это конкретное value, созданное на основе объявленного struct type и содержащее собственные field values.

Examples chapter: `employee{...}`, `Shape{...}`, `Rectangle`, `Board`, `Player`, `Game`.

Provenance: `p0154:c01–p0156:c01`, `p0190:c01–p0194:c01`.

## 8. Constructor function

Поскольку language-level constructors в Go source не использует, chapter предлагает ordinary function, обычно `New` или `New<Type>`, которая создаёт и инициализирует struct и возвращает value либо pointer.

~~~go
func NewShape(...) Shape
func NewShapeWithPoint(...) *Shape
~~~

Ограничение подхода по source framing: это обычная function/convention, а не специальный constructor mechanism языка; chapter не описывает автоматический обязательный вызов такой function.

Provenance: `p0163:c01–p0164:c01`, `p0197:c01`.

## 9. Encapsulation vs hiding

Source различает:
- encapsulation — объединение данных и methods работы с ними в одну оболочку; в Go chapter этой оболочкой выступает package;
- hiding — настройка доступа к encapsulated data/methods через lowercase/uppercase names.

Цель их совместного использования — поддерживать data invariants.

Provenance: `p0164:c01–p0165:c01`.

## 10. Новый уровень abstraction

Class/structural abstraction позволяет работать не с разрозненными variables/functions, а с domain entity, у которой state и behavior организованы вместе. Source связывает высокий уровень abstraction с упрощением изменений, сопровождения и более сложных architecture decisions.

Provenance: `p0153:c01`.

## 11. Три столпа abstraction

В chapter framing эту роль выполняют инкапсуляция, наследование/composition и полиморфизм. Вместе они позволяют скрывать детали, повторно использовать state/behavior и работать через общие abstractions.

Provenance: `p0153:c01`, `p0164:c01–p0169:c01`.

## 12. Interface

Interface объявляет method set без concrete implementation. Concrete type в chapter может использоваться как interface, если реализует требуемые methods; отдельного explicit `implements` declaration source не использует.

Interfaces применяются как variable type, function argument/return, slice element и struct field. Работа через interface ограничивает доступ method set интерфейса и позволяет подменять concrete implementations.

Provenance: `p0168:c01–p0175:c01`.

## 13. Anonymous fields

Anonymous field объявляется только type. В chapter это используется для embedding/composition: outer struct получает удобный доступ к state/methods embedded struct и может расширять их своим behavior.

Provenance: `p0156:c01`, `p0159:c01`, `p0165:c01–p0167:c01`.

## 14. Наследование в Go

Source прямо подаёт composition как замену inheritance: base-like struct встраивается anonymous field в более специализированную struct, которая получает её state/behavior и добавляет своё.

Provenance: `p0165:c01–p0167:c01`.

## 15. Связывание function с type

Так создаётся method: function получает receiver и вызывается через instance этого named type.

Value receiver работает с copy; pointer receiver позволяет менять instance state. Source также указывает, что receiver type и method должны быть объявлены в одном package.

Provenance: `p0161:c01–p0162:c01`.

## 16. Переопределение method

Chapter показывает outer struct method с тем же именем, что method embedded struct. При вызове через outer type Go сначала находит outer method; при необходимости source example явно обращается к embedded method.

Source затем уточняет, что это method lookup/promotion behavior, а не классическое переопределение в строгом смысле.

Provenance: `p0167:c01–p0168:c01`.

## 17. Interface как field структуры

Это позволяет хранить interchangeable implementation за interface contract.

В car example field `motor motor.IMotor` позволяет `Car` работать с различными engines и менять их через `ChangeMotor`, если новый type реализует `IMotor`.

Provenance: `p0175:c01–p0180:c01`.

## 18. Public/private methods and fields

По chapter convention:
- uppercase first letter → exported/public across packages;
- lowercase first letter → package-internal/private in source terminology.

Это относится к struct names, fields, functions and methods.

Provenance: `p0154:c01`, `p0159:c01–p0160:c01`, `p0197:c01`.

## 19. Generics

Generics — type parameters, позволяющие одной implementation работать с несколькими types и уменьшать duplication. Chapter связывает их появление с Go 1.18.

Generics применяются к functions и structs; source показывает multiple type parameters и generic map helpers.

Provenance: `p0184:c01–p0189:c01`.

## 20. Type constraints

Ограничение задаётся рядом с type parameter:

~~~go
func Sum[T int | float64 | string](a, b T) T
~~~

Другие варианты chapter:
- `any` — любой type;
- `comparable` — types supporting equality, используется для map keys;
- custom constraint interface;
- `~int` — разрешает named types с underlying type `int`.

Provenance: `p0185:c01–p0188:c01`.
