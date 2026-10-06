# Source findings — глава 20

## Finding 1 — ms-auto code vs ml-auto prose

Classification: **[Source wording/code mismatch]**

Provenance:
- chunk: e0030:c04
- EPUB spine item: 30
- locator: OEBPS/Text/978544614112-27.xhtml

Shown base.html code uses:

~~~html
<ul class="navbar-nav ms-auto mb-2 mb-md-0">
~~~

The following prose names the selector ml-auto and expands it as margin-left-automatic.

The identifier in shown code and the identifier in prose differ.

Adjudication: intended selector [Needs confirmation].

## Finding 2 — services.yaml section labeled routes.yaml

Classification: **[Source code mismatch]**

Provenance:
- chunk: e0030:c11
- EPUB spine item: 30
- locator: OEBPS/Text/978544614112-27.xhtml

The prose introduces the file services.yaml and says it should be saved under .platform/ next to routes.yaml.

The listing label immediately below is:

~~~text
.platform/routes.yaml
~~~

But the listing content defines the db service:

~~~yaml
db:
    type: postgresql:12
    disk: 1024
~~~

The prose/file purpose and listing label conflict.

Adjudication: intended listing filename [Needs confirmation].

## Finding 3 — base.html content div structure in extracted listing

Classification: **[Source extraction issue]**

Provenance:
- chunk: e0030:c05
- EPUB spine item: 30
- locator: OEBPS/Text/978544614112-27.xhtml

The prose says that after the page_header div, another div is defined to contain the content block.

The extracted listing instead contains an additional closing div before the content block and another closing div after it, without a visible opening tag for the second div.

Because the RAG text may have lost or transformed markup during EPUB text extraction, canonical artifacts do not silently repair the HTML.

Adjudication: exact intended markup [Needs confirmation].

## Finding 4 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: e0030:c02–e0030:c19
- EPUB spine item: 30
- locator: OEBPS/Text/978544614112-27.xhtml

Multiple chunks begin with continuation fragments from the preceding chunk, for example e0030:c02 starts inside the phrase "Navbar static" and later chunks repeat the ending of the previous chunk.

Cross-check:
- adjacent chunks preserve the chapter sequence;
- exercises 20.1–20.4 are recoverable;
- chapter-end summary is intact in e0030:c19;
- e0031:c01 begins the next section, «Приложения»;
- no chapter-level semantic loss was detected apart from the markup ambiguity recorded in Finding 3.

Adjudication: extractor/chunker root cause [Needs confirmation].

## Environment-specific sample values

The source contains concrete sample values for:

- Platform.sh region;
- generated deployment URL;
- SSH host fingerprint fragment;
- project/repository identifiers;
- usernames;
- package/runtime versions;
- estimated plan cost.

These are source examples, not portable configuration. Canonical artifacts treat them as environment-specific and do not recommend copying them automatically.
