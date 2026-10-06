# Source findings — глава 19

## Finding 1 — HttpResponseRedirect/reverse prose vs redirect() code

Classification: **[Source prose/code mismatch]**

Provenance:
- chunk: `e0029:c02`
- EPUB spine item: `29`
- locator: `OEBPS/Text/978544614112-26.xhtml`

Shown imports/code use:

~~~python
from django.shortcuts import render, redirect
...
return redirect('learning_logs:topics')
~~~

But prose immediately says that `HttpResponseRedirect` is imported and `reverse()` determines the URL. Neither appears in the shown listing.

Adjudication: intended explanation `[Needs confirmation]`.

## Finding 2 — accounts application path mismatch

Classification: **[Source path mismatch]**

Provenance:
- chunks: `e0029:c07–c08`

After `python manage.py startapp accounts`, the listing shows `accounts/` as a sibling of `ll_project/`.

Later prose names:
- `ll_project/accounts/urls.py`;
- `ll_project/accounts/templates/registration/`.

Those paths conflict with the shown project layout.

Adjudication: intended filesystem path `[Needs confirmation]`.

## Finding 3 — registration form.as_div vs prose as_p

Classification: **[Source template-rendering mismatch]**

Provenance:
- chunks: `e0029:c10–c11`

Shown registration template:

~~~django
{{ form.as_div }}
~~~

Prose then says that `as_p` is used again.

Rendered helper names differ.

Adjudication: intended helper `[Needs confirmation]`.

## Finding 4 — form.as_p description names div tags

Classification: **[Source markup-description mismatch]**

Provenance:
- chunk: `e0029:c03`

Shown template uses `{{ form.as_p }}`.

Prose describes paragraph-style rendering but parenthetically names the HTML element `<div></div>`.

The paragraph wording and cited HTML element do not match each other.

Adjudication: intended markup explanation `[Needs confirmation]`.

## Finding 5 — authorization-complete claim vs exercise 19.4

Classification: **[Source authorization/process contradiction]**

Provenance:
- chunks: `e0029:c15–c16`

After adding ownership checks to Topic display, Entry editing and Topic creation, source states broadly that users will be limited to their own data for any operation.

Immediately afterward exercise 19.4 identifies one remaining unguarded creation path: `new_entry/<topic_id>/` still needs an ownership check for the referenced Topic.

Therefore the broad completion claim appears before the authorization boundary is fully closed.

Policy action: canonical artifacts treat the exercise 19.4 ownership check as required completion of the ownership model.

## Finding 6 — source typos in auth prose

Classification: **[Source terminology/text typo]**

Provenance:
- chunks: `e0029:c07`, `e0029:c09`

Observed:
- `Djano` where surrounding text names Django;
- page “регрессии” in prose where the surrounding section is registration.

These are retained as source-text defects; RAG is not modified.

## Finding 7 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0029:c02–c16`
- EPUB spine item: `29`
- locator: `OEBPS/Text/978544614112-26.xhtml`

Multiple chunks begin with continuation fragments from the preceding chunk.

Cross-check:
- adjacent chunks preserve context;
- exercises 19.1–19.5 are recoverable;
- chapter-end summary is intact;
- `e0030:c01` confirms chapter 20;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

## Migration sample-data boundary

The one-off migration example uses user ID `1` because that ID belongs to the sample `ll_admin` database.

This value is not portable to another database. A valid target user ID must be discovered before migration.
