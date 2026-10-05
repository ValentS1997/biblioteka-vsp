# Ответы на вопросы для самопроверки — глава 1

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Требования при разработке Go

Источник перечисляет: простой синтаксис, компилируемость и быструю компиляцию, лёгкость изучения, встроенный удобный параллелизм, развитую стандартную библиотеку, отсутствие неявных преобразований, garbage collection, разделение интерфейсов и реализации, package system с явными зависимостями.

Provenance: `p0016:c01`.

## 2. Основные особенности Go

Глава характеризует Go как cross-platform compiled language со strict static typing и open source. Также подчёркиваются быстрая сборка, self-contained executable, garbage collection, package/dependency model и сравнительно простой concurrent code.

Provenance: `p0016:c01–p0017:c01`.

## 3. Ближайший по синтаксису язык

Go ближе всего к C (Си).

Provenance: `p0016:c01–p0017:c01`.

## 4. Виды типов данных

Глава делит types на:
- встроенные (основные);
- составные.

Provenance: `p0026:c01–p0027:c01`.

## 5. Встроенные типы

В chapter list входят:
- integers;
- floats;
- complex numbers;
- `byte`;
- `rune`;
- `string`;
- `bool`.

Provenance: `p0026:c01–p0027:c01`.

## 6. Составные типы

Три категории:
- aggregate/value: arrays, structs;
- reference: slices, maps, channels, pointers, functions, methods;
- interface type: interfaces.

Provenance: `p0027:c01`.

## 7. `float64` vs `int`

`int` хранит целые значения; его размер зависит от platform. `float64` хранит floating-point values и занимает 64 bits; при type inference вещественного literal chapter использует `float64`.

Provenance: `p0027:c01–p0028:c01`.

## 8. Комплексные числа

Используются `complex64` и `complex128`. Их можно создавать через `complex(a, b)` или complex literal.

Provenance: `p0029:c01`.

## 9. `byte` vs `rune`

- `byte` — alias `uint8`, в chapter применяется для ASCII-oriented byte values.
- `rune` — alias `int32`, используется для Unicode code points.

Provenance: `p0029:c01–p0030:c01`.

## 10. `string`

Глава определяет string как read-only sequence/slice of bytes. Она хранит текст; UTF-8 character может занимать несколько bytes, поэтому byte indexing не всегда соответствует character indexing.

Provenance: `p0030:c01–p0031:c01`.

## 11. Операции над `bool`

`bool` принимает `true` или `false`. Глава показывает три logical operations:
- AND `&&`;
- OR `||`;
- NOT `!`.

Provenance: `p0032:c01`.

## 12. Array и slice

Array:
- fixed length;
- elements одного type;
- assignment copies the array.

Slice:
- изменяемая последовательность;
- структура `ptr + len + cap`;
- assignment может разделять underlying storage;
- для независимой копии chapter показывает `copy`.

Provenance: `p0033:c01–p0039:c01`.

## 13. `map`

`map` — key/value collection. Key должен быть unique и поддерживать comparison. Глава показывает creation, read/write, `delete` и проверку наличия key через `value, ok := map[key]`.

Provenance: `p0039:c01–p0041:c01`.

## 14. Pointer

Pointer хранит address переменной.

- получить address: `p := &value`;
- прочитать value: `*p`;
- изменить исходную переменную: `*p = newValue`.

Zero value pointer — `nil`.

Provenance: `p0042:c01–p0044:c01`.

## 15. Constants и `iota`

`const` объявляет значение, которое нельзя изменить после объявления. Typed constant задаётся с type, например `const x int = 30`.

`iota` — generator последовательных значений в constant block; пример начинается с 0 и затем увеличивается.

Provenance: `p0045:c01–p0047:c01`.

## 16. Максимальный `int8` + 5

Максимум `int8` по таблице главы — 127. При 8-bit arithmetic результат выходит за диапазон; по показанному в разделе 1.13 механизму overflow старшие биты теряются/значение оборачивается. Для runtime `int8` arithmetic результат будет `-124`.

Это вывод из:
- диапазона `int8`;
- source example fixed-width overflow (`uint8 255 + 5 → 4`).

Provenance: `p0027:c01`, `p0065:c01`.

## 17. `int` ↔ `float64`

Явное conversion:
~~~go
f := float64(i)
i2 := int(f)
~~~

При float → int дробная часть отбрасывается; chapter предупреждает о возможной потере данных при narrowing.

Provenance: `p0064:c01–p0065:c01`.

## 18. `int` ↔ `string`

Chapter uses `strconv`:
~~~go
s := strconv.Itoa(n)
n2, err := strconv.Atoi(s)
~~~

Ошибка `Atoi` проверяется через `err`.

Provenance: `p0066:c01`.

## 19. Integer formatting with `Printf`

Source table:
- `%b`
- `%c`
- `%d`
- `%o`
- `%O`
- `%x`
- `%X`
- `%U`

Provenance: `p0077:c01`.

## 20. Float formatting with `Printf`

Source table:
- `%b`
- `%e` / `%E`
- `%f` / `%F`
- `%x` / `%X`

Для `%f` можно задавать precision.

Provenance: `p0077:c01–p0078:c01`.

## 21. String formatting with `Printf`

Source table:
- `%s`
- `%q`
- `%x` / `%X`

Provenance: `p0078:c01`.

## 22. Операторы Go

Глава классифицирует:
- arithmetic;
- comparison;
- logical;
- bitwise;
- assignment;
- unary;
- other operators.

К «other» в показанной таблице относятся address `&` и dereference `*`.

Provenance: `p0047:c01–p0050:c01`.

## 23. Именование переменных

Source rules/recommendations:
- meaningful names;
- `MixedCaps` / `mixedCaps`, а не underscore-separated names;
- exported identifier starts with uppercase;
- internal identifier — lowercase/mixedCaps;
- имя не должно совпадать с keyword;
- one-letter names допустимы для небольших loops;
- initialisms полностью uppercase внутри identifier, например `productAPI`.

Provenance: `p0024:c01–p0025:c01`.

## 24. Обязателен ли `else`

Нет. Source прямо называет `else` optional. Если `else` нет и condition false, body `if` просто не выполняется.

Provenance: `p0051:c01–p0052:c01`.

## 25. Для чего циклы

Для repeated execution однотипных действий, чтобы не дублировать одинаковый код.

Provenance: `p0058:c01`.

## 26. Сколько loop keywords

Одно: `for`.

Source explicitly says, что все формы loops в Go организуются одним keyword `for`.

Provenance: `p0058:c01`.

## 27. Precondition и postcondition

Precondition:
~~~go
for condition {
    // body
}
~~~
Тело может не выполниться ни разу.

Postcondition chapter имитирует через infinite loop, выполняя body до проверки и завершая `break`:
~~~go
for {
    // body
    if exitCondition {
        break
    }
}
~~~

Provenance: `p0059:c01`.

## 28. `range`

Используется для iteration по collections. В chapter:
- array/slice: index + copy of value;
- map: key + copy of value;
- string: byte offset + rune.

Также показана форма `for i := range N`.

Provenance: `p0060:c01–p0062:c01`.

## 29. `break` и `continue`

- `break` завершает текущий loop и передаёт управление после него.
- `continue` пропускает остаток текущей iteration и передаёт управление к следующей.

Provenance: `p0059:c01–p0060:c01`.

## 30. `switch–case`

Используется как альтернативная control-flow конструкция, особенно вместо длинных chains `if–else`, когда выполняется выбор по значениям/выражению.

`default` optional. Source также показывает multiple values per `case` и `fallthrough`.

Provenance: `p0055:c01–p0056:c01`.

## 31. Комментарии

Comments — строки/фрагменты, ignored by compiler, используемые для объяснения кода и особенно причины выбранного решения.

- `// ...`
- `/* ... */`

Source discourages obvious/noisy comments.

Provenance: `p0025:c01–p0026:c01`.

## 32. Расположение фигурных скобок

Да. В Go opening `{` должна располагаться на той же строке после declaration/condition. Перенос opening brace на следующую строку в показанном example приводит к compile error.

Provenance: `p0026:c01`.

## 33. Безусловный переход

Это переход к label без проверки condition. Используется keyword `goto`.

Label имеет function scope. Source не рекомендует этот механизм из-за ухудшения последовательной логики и риска infinite loop.

Provenance: `p0063:c01`.

## 34. Нужны ли braces при одном действии в loop

Да. Source syntax всех `for` forms использует block в braces; отдельного однострочного варианта без `{ ... }` глава не вводит.

Provenance: `p0058:c01–p0059:c01`.

## 35. Бесконечный цикл и выход

Структурированный вариант:
~~~go
for {
    // body
}
~~~

Выход — explicit `break` при нужном condition.

Глава также показывает бесконечное повторение через `goto label`, но приводит это как риск и не рекомендует.

Provenance: `p0059:c01`, `p0063:c01`.

## 36. Приоритет операторов

От высокого к низкому:

1. `* / % << >> & &^`
2. `+ - | ^`
3. `== != < <= > >=`
4. `&&`
5. `||`

Круглые скобки позволяют явно изменить порядок evaluation.

Provenance: `p0050:c01`.
