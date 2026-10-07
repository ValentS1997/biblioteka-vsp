# Запросы и инструменты главы 2

Включены только examples, прямо подтвержденные chapter RAG. Современные product-specific corrections не добавлялись.

## SQL: declarative filter

Источник: `p0070:c01`, PDF 70.

~~~sql
SELECT * FROM animals WHERE family = 'Sharks';
~~~

Тип: read-only query.

Смысл: запрос описывает требуемый набор данных, но не фиксирует algorithm/index/join strategy.

Verification: результат содержит rows, соответствующие `family = 'Sharks'`.

Rollback: `[Not applicable]`.

## SQL: aggregation

Источник: `p0074:c01`, PDF 74.

~~~sql
SELECT date_trunc('month', observation_timestamp) AS observation_month,
       sum(num_animals) AS total_animals
FROM observations
WHERE family = 'Sharks'
GROUP BY observation_month;
~~~

Тип: read-only query.

Смысл: filter → group by month → aggregate count.

Verification: одна aggregated row на календарный месяц для семейства Sharks.

Rollback: `[Not applicable]`.

## MongoDB MapReduce

Источник: `p0074:c01`–`p0075:c01`, PDF 74–75.

~~~javascript
db.observations.mapReduce(
    function map() {
        var year  = this.observationTimestamp.getFullYear();
        var month = this.observationTimestamp.getMonth() + 1;
        emit(year + "-" + month, this.numAnimals);
    },
    function reduce(key, values) {
        return Array.sum(values);
    },
    {
        query: { family: "Sharks" },
        out: "monthlySharkReport"
    }
);
~~~

Тип: state-changing / workload-generating.

Effect: вычисляет monthly aggregation и записывает output collection `monthlySharkReport`.

Source constraint: `map` и `reduce` должны быть pure — без дополнительных DB queries и side effects.

Verification: output collection содержит aggregated values по month.

Rollback: `[Needs confirmation]`.

## MongoDB aggregation pipeline

Источник: `p0076:c01`, PDF 76.

~~~javascript
db.observations.aggregate([
    { $match: { family: "Sharks" } },
    { $group: {
        _id: {
            year:  { $year:  "$observationTimestamp" },
            month: { $month: "$observationTimestamp" }
        },
        totalAnimals: { $sum: "$numAnimals" }
    } }
]);
~~~

Тип: read-only query в представленном примере.

Verification: aggregated results соответствуют monthly shark observations.

Rollback: `[Not applicable]`.

## Cypher: создание graph fragment

Источник: `p0080:c01`, PDF 80.

~~~cypher
CREATE
  (NAmerica:Location {name:'North America', type:'continent'}),
  (USA:Location      {name:'United States', type:'country'  }),
  (Idaho:Location    {name:'Idaho',         type:'state'    }),
  (Lucy:Person       {name:'Lucy' }),
  (Idaho) -[:WITHIN]->  (USA)  -[:WITHIN]-> (NAmerica),
  (Lucy)  -[:BORN_IN]-> (Idaho)
~~~

Тип: state-changing.

Effect: создает vertices и relationships.

Verification: последующие graph queries должны находить созданные paths.

Rollback: `[Needs confirmation]`.

## Cypher: variable-length traversal

Источник: `p0080:c01`, PDF 80.

~~~cypher
MATCH
  (person) -[:BORN_IN]->  () -[:WITHIN*0..]-> (us:Location {name:'United States'}),
  (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (eu:Location {name:'Europe'})
RETURN person.name
~~~

Тип: read-only query.

Смысл: pattern matching с `WITHIN` zero-or-more hops.

Rollback: `[Not applicable]`.

## SPARQL

Источник: `p0086:c01`, PDF 86.

~~~sparql
PREFIX : <urn:example:>

SELECT ?personName WHERE {
  ?person :name ?personName.
  ?person :bornIn  / :within* / :name "United States".
  ?person :livesIn / :within* / :name "Europe".
}
~~~

Тип: read-only query.

Rollback: `[Not applicable]`.

## Datalog

Источник: `p0088:c01`–`p0090:c01`, PDF 88–90.

~~~prolog
within_recursive(Location, Name) :- name(Location, Name).
within_recursive(Location, Name) :- within(Location, Via),
                                    within_recursive(Via, Name).

migrated(Name, BornIn, LivingIn) :- name(Person, Name),
                                    born_in(Person, BornLoc),
                                    within_recursive(BornLoc, BornIn),
                                    lives_in(Person, LivingLoc),
                                    within_recursive(LivingLoc, LivingIn).

?- migrated(Who, 'United States', 'Europe').
~~~

Тип: read-only logical query over facts/rules in the chapter example.

Verification: source example derives `Who = 'Lucy'`.

Rollback: `[Not applicable]` для query.

## Source-confirmed technologies

SQL/RDBMS, MongoDB, RethinkDB, CouchDB, PostgreSQL, ActiveRecord, Hibernate, RDF, Neo4j/Cypher, SPARQL, Datalog, Datomic, Cascalog, Hadoop, CSS, XSL/XPath.

## Что не добавлено

- команды миграции схем;
- `CREATE TABLE` / indexes;
- backup/restore;
- product-specific admin commands;
- современные syntax corrections.

В chapter RAG таких operational commands нет.
