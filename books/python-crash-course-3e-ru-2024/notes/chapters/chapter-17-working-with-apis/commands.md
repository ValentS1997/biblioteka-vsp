# Команды и операции главы 17

## Install requests

~~~bash
python -m pip install --user requests
~~~

Source alternative: use `python3` if that is the interpreter command.

Classification: **state-changing package-management action**.

Current interpreter/environment/version/rollback: `[Needs confirmation]`.

## GitHub API request

~~~python
r = requests.get(url, headers=headers)
~~~

Classification: **external network action**.

Effects:
- sends an HTTP request to external API;
- consumes API request quota where applicable;
- response is time-dependent.

Current endpoint/header/auth requirements: `[Needs confirmation]`.

## Inspect HTTP status

~~~python
print(r.status_code)
~~~

Source uses status 200 as successful example.

## Decode JSON response

~~~python
response_dict = r.json()
~~~

Classification: in-memory parsing of received data.

## GitHub rate-limit endpoint

Source asks to inspect:

~~~text
https://api.github.com/rate_limit
~~~

Classification: external network/read operation.

Historical source example:
- search limit: 10/minute;
- remaining: 9;
- reset: epoch timestamp.

Current values: `[Needs confirmation]`.

## Plotly render

~~~python
fig.show()
~~~

Classification: UI/browser workload.

## Hacker News requests

~~~python
r = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json"
)
~~~

and per story:

~~~python
r = requests.get(
    f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
)
~~~

Classification: repeated external network actions.

Source loop performs up to 31 calls for the shown flow: one top-stories request plus 30 item requests.

## JSON pretty formatting

~~~python
response_string = json.dumps(
    response_dict,
    indent=4,
)
print(response_string)
~~~

Classification: in-memory formatting + terminal output.

## Sort by comments

~~~python
submission_dicts = sorted(
    submission_dicts,
    key=itemgetter('comments'),
    reverse=True,
)
~~~

Classification: in-memory transformation.

## Token boundary

Source mentions access tokens only in rate-limit discussion.

Token acquisition, storage, injection and rotation are not specified by chapter source: `[Needs confirmation]`.
