# Ответы на вопросы для самопроверки — глава 8

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. TCP: назначение и работа

В source TCP представлен как connection-oriented transport protocol.

Client инициирует connection, после чего между processes поддерживается communication channel до завершения session.

Source emphasises:
- connection establishment;
- persistent exchange;
- detection of communication failures;
- server-side need to handle multiple blocking socket connections concurrently.

В Go chapter uses `net.Dial`, `net.Listen`, `Accept`, `Read`, `Write`.

Provenance: `p0417:c01–p0425:c01`.

## 2. UDP: назначение и работа

UDP source describes as connectionless transport protocol.

Each message is handled independently; persistent connection is not created and delivery is not guaranteed in the source framing.

Chapter connects UDP with short/stateless interactions and demonstrates an echo service through `DialUDP`, `ListenUDP`, `ReadFromUDP`, `WriteToUDP`.

Provenance: `p0418:c01–p0421:c01`.

## 3. TCP vs UDP

По source framing:
- TCP establishes and maintains a connection;
- UDP processes independent datagrams without persistent connection;
- TCP provides session-oriented reliable interaction in the chapter explanation;
- UDP has lower connection-state overhead but no delivery guarantee in the source explanation.

Provenance: `p0418:c01–p0419:c01`.

## 4. REST и REST API

REST is an architectural style describing how a web service should behave, using HTTP client-server interaction.

API is an interface that allows one program to interact with another.

REST API in source is an application interface using HTTP requests to obtain, create/write, update and delete resources.

Provenance: `p0429:c01–p0430:c01`.

## 5. Common HTTP request types

Chapter highlights:
- `GET` — retrieve resources;
- `PUT` — create/write or update in source framing;
- `POST` — create/write;
- `DELETE` — delete resources.

Provenance: `p0429:c01`.

## 6. HTTP message structure

Source divides HTTP messages into:
- header;
- body.

Headers carry metadata. Body carries data and may be absent for some request/response types.

Content format is identified through `Content-Type`, for example `application/json`.

Provenance: `p0430:c01`.

## 7. Header types

Request headers in source are grouped into:
1. general headers;
2. request headers;
3. entity headers.

Response headers are grouped into:
1. general headers;
2. response headers;
3. entity headers.

Provenance: `p0430:c01`.

## 8. Status code

Status code is a numeric part of the server response status line indicating request outcome.

Example:

~~~text
HTTP/1.1 404 Not Found
~~~

It contains protocol version, numeric status code and textual description.

Provenance: `p0431:c01`.

## 9. Common response status codes

Source lists:
- `200 OK`;
- `201 Created`;
- `400 Bad Request`;
- `401 Unauthorized`;
- `404 Not Found`;
- `405 Method Not Allowed`;
- `409 Conflict`;
- `500 Internal Server Error`.

Provenance: `p0431:c01`.

## 10. REST URL and construction rules

REST URL identifies a resource through a URI/URL path.

Source example:

~~~text
/api/v1/todo/projects/3/tasks/1
~~~

Rules emphasized:
- model resources as nouns rather than verbs;
- use HTTP method to represent action;
- allow path parameters;
- allow query strings for additional parameters;
- version the API.

Source examples also show:

~~~text
/api/v1/todo/projects/3/tasks?id=1
/api/v1/todo/projects/tasks?projID=3&taskID=1
~~~

Provenance: `p0431:c01–p0432:c01`.

## 11. OpenAPI v3: purpose

Source uses OpenAPI v3 to describe and document a REST API independently of implementation language.

Benefits stated:
- humans and programs can inspect service capabilities;
- no need to study implementation source or network traffic;
- API contract can be designed before service implementation;
- visualization/documentation can be generated from the spec.

Main sections shown:
- `info`;
- `paths`;
- `components`.

Provenance: `p0432:c01–p0437:c01`.

## 12. GET with parameter in path

Source path-parameter pattern:

~~~yaml
/resource/{id}:
  get:
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
~~~

In the chapter the concrete path-parameter example is shown for `/project/del/{id}` with `in: path`; the same OpenAPI mechanism answers the question about a GET path parameter.

Provenance: `p0442:c01–p0443:c01`.

## 13. GET with query-string parameter

Source explicitly shows:

~~~yaml
/task:
  get:
    parameters:
      - in: query
        name: projectID
        schema:
          type: integer
~~~

This maps to a query such as:

~~~text
/task?projectID=1
~~~

Provenance: `p0446:c01`.

## 14. POST with request body

Source pattern:

~~~yaml
/project:
  post:
    requestBody:
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Project"
~~~

The body schema is referenced from `components/schemas`.

Chapter also uses the same pattern for creating a task.

Provenance: `p0440:c01–p0441:c01`, `p0445:c01–p0446:c01`.
