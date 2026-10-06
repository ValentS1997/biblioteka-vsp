# Резюме главы 19

Source provenance:

- chunk: `e0029:c16`
- EPUB spine item: `29`
- locator: `OEBPS/Text/978544614112-26.xhtml`

Chapter-end summary фиксирует, что читатель:

- использовал forms для создания Topics/Entries и редактирования существующих data;
- реализовал user accounts, login/logout и registration;
- использовал `UserCreationForm`;
- ограничивал views через `@login_required`;
- связал Topic с User через ForeignKey;
- выполнил migration, требующую one-off default для existing data;
- ограничивал list data через `filter()`;
- сравнивал owner запрашиваемого data с текущим user.

Source отдельно подчёркивает, что security boundaries не всегда очевидны и code review другим разработчиком повышает шанс обнаружить плохо защищённые paths.

Глава 20 — финальная — занимается styling и deployment приложения.

Это структурированный перенос source section «Резюме» без внешних дополнений.
