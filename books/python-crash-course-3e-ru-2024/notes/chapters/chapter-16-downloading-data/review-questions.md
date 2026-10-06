# Упражнения главы 16

Source provenance:

- EPUB spine item: `26`
- locator: `OEBPS/Text/978544614112-23.xhtml`
- exercise chunks: `e0026:c07`, `e0026:c12–c13`

## 16.1. Осадки в Ситке

Используйте `sitka_weather_2021_full.csv` и столбец `PRCP` для диаграммы ежедневных осадков. При желании повторите для Death Valley.

Файл full dataset в текущем RAG scope не содержится целиком: `[Needs confirmation]`.

## 16.2. Сравнение Ситки с Долиной Смерти

Установите одинаковый scale оси Y на двух temperature charts и проведите прямое сравнение диапазонов.

Конкретный API изменения Y-axis в тексте главы не показан: `[Needs confirmation]`.

## 16.3. Сан-Франциско

Скачайте weather data для San Francisco, создайте temperature chart и сравните её с Sitka/Death Valley.

External dataset не загружался в `rag_only`.

## 16.4. Автоматические индексы

Вместо hard-coded indices определяйте positions `TMIN` и `TMAX` по header row. Используйте station name для автоматического title.

## 16.5. Исследования

Создайте несколько других visualizations weather aspects для выбранных мест.

Выбранные dataset/metric/location: `[Needs confirmation]`.

## 16.6. Рефакторинг

Уберите временные variables `mag`, `lon`, `lat`, `eq_title` и сразу append значения из `eq_dict`. Body loop должен сократиться до четырёх строк.

## 16.7. Автоматизированный заголовок

Получите title dataset из GeoJSON metadata и используйте его вместо hard-coded `Global Earthquakes`.

## 16.8. Недавние землетрясения

Скачайте один из current USGS GeoJSON datasets за 1 hour / 1 day / 7 days / 30 days и создайте visualization.

External current data не загружались в `rag_only`.

## 16.9. Пожары

Используйте supplemental `world_fires_1_day.csv` и создайте world map по longitude, latitude и fire area.

Supplemental file в текущем source scope отсутствует: `[Needs confirmation]`.

Нумерация и требования сохранены по RAG.
