# Cheatsheet — глава 9 «Структуры данных, типы и их методы»

## Problem framing

Нужно различать четыре похожие, но не одинаковые конструкции: C array, Go array, pointer to Go array и Go slice.

## Go array

Источник определяет:

```go
type arr [7]int
```

Размер является частью типа. Вызов `atrans(v arr)` работает с копией array, поэтому изменения внутри функции не меняют исходный `a1` в показанном примере.

## Pointer to array

```go
func ptrans(p *arr) {
    for i, x := range *p {
        (*p)[i] = x + 1
    }
}
```

Вызов `ptrans(&a1)` даёт caller-visible mutation.

## Slice

```go
func strans(v []int) []int
a3 := a2[0:len(a2)]
```

После `strans(a3)` source example показывает изменённые элементы.

Источник сам использует две формулировки — «передаётся по ссылке» и позже «неверно говорить ... по ссылке». Это не нормализуется молча; см. `source-findings.md`.

## Type boundary

```text
[7]int ≠ []int
```

Функция, ожидающая array, не принимает slice и наоборот.

## Multidimensional slice

```go
twoD := make([][]int, dim)
for i := 0; i < dim; i++ {
    twoD[i] = make([]int, i+1)
}
```

Nested slices могут иметь строки разной длины.

## Multiple return values

```go
func vals(n int) (int, float64, []string)
i, f, s := vals(5)
_, f, _ = vals(7)
```

`_` используется для игнорирования ненужных результатов.

## Named results

```go
func vals(n int) (i int, f float64, s []string) {
    i = n
    f = float64(n) / 3
    s = []string{"g", "h", "i"}
    return
}
```

Имена результатов уже объявлены в signature, поэтому source example использует `=`.

## Verification examples

```bash
./array_c
./array_go
./garray_c
./cpptr
./3slice
./marg
```

Проверять observable state: изменился ли caller-owned array, изменились ли slice elements, совпадают ли return values.

## Next action

Следующая глава переходит к строкам, rune и Unicode.
