"""One-shot canonical renderer for both chapter 2 SVG summaries.

Text facts must already exist in chapter 2 README, cheatsheet, commands and
diagram; no source PDF or external network is opened by the renderer.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

BOOK = "how-linux-works-brian-ward-3e-ru-2022"
OUT = Path("books") / BOOK / "notes/chapters/chapter-02-basic-commands-and-directory-hierarchy"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
FONT = "DejaVu Sans,Arial,sans-serif"
DARK = "#172a43"
TEXT = "#233c54"
MUTED = "#49627a"

def sub(parent, name, **kwargs):
    return ET.SubElement(parent, f"{{{NS}}}{name}", {
        k.replace("_", "-"): str(v) for k, v in kwargs.items()
    })

def label(parent, x, y, txt, size=20, bold=False, color=TEXT):
    t = sub(parent, "text", x=x, y=y, font_family=FONT,
            font_size=size, font_weight="700" if bold else "400",
            fill=color)
    t.text = txt
    return t

def box(parent, x, y, w, h, fill, radius=0, border=None):
    p = dict(x=x, y=y, width=w, height=h, rx=radius, fill=fill)
    if border:
        p.update(stroke=border, stroke_width=2)
    return sub(parent, "rect", **p)

def card(parent, x, y, width, height, title, rows,
         accent="#2479a7", font=19, gap=33):
    box(parent, x, y, width, height, "#ffffff", 18, accent)
    box(parent, x, y, width, 9, accent, 4)
    label(parent, x+26, y+49, title, 24, True, accent)
    for idx, row in enumerate(rows):
        label(parent, x+26, y+99+idx*gap, row, font)
        
def canvas(w, h, title, subtitle, description):
    node = ET.Element(f"{{{NS}}}svg", {
        "viewBox": f"0 0 {w} {h}", "width":str(w), "height":str(h),
        "role":"img", "aria-labelledby":"title desc"
    })
    a = sub(node, "title", id="title")
    a.text = title
    d = sub(node, "desc", id="desc")
    d.text = description
    box(node, 0, 0, w, h, "#f3f7fc")
    box(node, 0, 0, w, 139, DARK)
    label(node, 54, 59, title, 37, True, "#ffffff")
    label(node, 54, 104, subtitle, 22, False, "#d3e7ff")
    return node

def compact():
    s = canvas(1600, 950, "Глава 2 — Основные команды Linux",
               "От shell и файлов — к процессам, правам и sudo",
               "Обзор shell, read-only проверок, потоков, изменений и каталогов.")
    card(s, 48, 174, 482, 232, "SHELL И ПУТИ", [
        "cd / pwd / PATH / export",
        "Абсолютные и относительные пути",
        "Globbing: * и ? до выполнения",
        "cat: stdin → stdout; Ctrl+D = EOF"
    ], "#2a7397", 20, 35)
    card(s, 559, 174, 482, 232, "НАБЛЮДЕНИЕ", [
        "ls -l / file / find / grep",
        "man / info / diff / less",
        "ps / jobs / groups",
        "journalctl ... sudo"
    ], "#23805d", 20, 35)
    card(s, 1070, 174, 482, 232, "ПОТОКИ И ОШИБКИ", [
        "| соединяет stdout → stdin",
        "> перезаписывает; >> добавляет",
        "2> = stderr, 2>&1 = вместе",
        "Сначала читай первую ошибку"
    ], "#6955a1", 20, 35)
    card(s, 48, 447, 482, 247, "ИЗМЕНЕНИЕ ФАЙЛОВ", [
        "cp / mv / touch / mkdir",
        "rm и особенно rm -r: риск",
        "chmod / umask / ln -s",
        "До изменения: путь и права"
    ], "#bd682f", 20, 35)
    card(s, 559, 447, 482, 247, "ПРОЦЕССЫ И АРХИВЫ", [
        "ps → PID; kill → сигнал",
        "STOP / CONT / TERM / KILL",
        "tar t перед tar x",
        "gzip и tar — разные действия"
    ], "#2b6e9f", 20, 35)
    card(s, 1070, 447, 482, 247, "ИЕРАРХИЯ И ROOT", [
        "/etc — конфиги; /proc — процессы",
        "/var — журналы; /run — runtime",
        "/usr — программы; /home — данные",
        "sudo / visudo — привилегии"
    ], "#6a599b", 20, 35)
    box(s, 48, 739, 1504, 132, "#fcece9", 18, "#d08063")
    label(s, 75, 778, "SAFETY BOUNDARY", 25, True, "#a13e2c")
    label(s, 75, 815, "Не выполнять rm -r, kill -KILL, tar x, chmod или sudo без проверки цели и rollback.", 20)
    label(s, 75, 846, "NOPASSWD: ALL — широкий доступ; пример книги НЕ является конфигурационной рекомендацией.", 19)
    label(s, 52, 918, "Источник: Уорд · гл. 2 · PDF/печатные с. 39–78 · RAG p0039:c01–p0078:c01 · только текстовая реконструкция", 16, color=MUTED)
    return s

def detailed():
    s = canvas(1800, 1510, "Глава 2 — Рабочая карта Unix/Linux",
               "Shell • навигация • диагностика • права • процессы • архивы • sudo",
               "Подробная шпаргалка по основным командам и иерархии каталогов главы 2.")
    c = [
        (45, 169, "ОБОЛОЧКА (с. 40–43)", [
            "Команда = программа или builtin + аргументы",
            "cat без файла читает stdin терминала",
            "Ctrl+D = EOF; Ctrl+C = прерывание",
            "Не вводить $ из приглашения"
        ], "#24749d"),
        (627, 169, "НАВИГАЦИЯ (с. 43–47)", [
            "pwd / pwd -P; ls / ls -l / ls -a",
            "cd — builtin; /, .., . и ~",
            "find dir -name file -print",
            "Globbing * и ?; кавычки сохраняют literal"
        ], "#208263"),
        (1209, 169, "ОКРУЖЕНИЕ (с. 51–53)", [
            "STUFF=blah → export STUFF",
            "PATH=dir:$PATH — поиск в начале",
            "PATH=$PATH:dir — поиск в конце",
            "echo $PATH; испорченный PATH — новый shell"
        ], "#755ca3"),
        (45, 451, "READ-ONLY (с. 48–58)", [
            "grep / less / diff / file",
            "head / tail / sort / locate",
            "man ls / man -k / man 5 passwd",
            "info command; ls --help"
        ], "#24749d"),
        (627, 451, "STDIO (с. 58–59)", [
            "stdin ← < file",
            "stdout → > file (overwrite)",
            "stdout → >> file (append)",
            "stderr → 2> e; объединение 2>&1"
        ], "#208263"),
        (1209, 451, "ОШИБКИ (с. 60–62)", [
            "Первое сообщение: программа / путь / причина",
            "ENOENT — объект не найден",
            "Permission denied — недостаточно прав",
            "Not a directory / No space left / segfault"
        ], "#ae662c"),
        (45, 733, "ПРОЦЕССЫ (с. 62–66)", [
            "ps / ps auxw: PID STAT TIME COMMAND",
            "jobs / fg / bg / Ctrl+Z",
            "kill → TERM; STOP и CONT",
            "KILL только в крайнем случае; PID reused"
        ], "#24749d"),
        (627, 733, "ПРАВА И ССЫЛКИ (с. 66–71)", [
            "u/g/o: r, w, x; каталогу нужен x",
            "chmod go+r / chmod 644",
            "umask 022 / umask 077 для новых файлов",
            "ln -s target linkname — проверить путь"
        ], "#755ca3"),
        (1209, 733, "АРХИВЫ (с. 71–74)", [
            "tar: c создать / t список / x извлечь",
            "gzip — сжатие, tar — архив",
            "tar ztvf file.tar.gz: проверка перед x",
            "zcat ... | tar xvf - меняет файлы"
        ], "#ae662c"),
        (45, 1015, "ИЕРАРХИЯ (с. 74–77)", [
            "/etc = конфигурация; /bin = программы",
            "/home = пользователи; /usr = пакеты",
            "/proc, /sys, /dev = системные интерфейсы",
            "/var = изменяемые данные; /run = runtime"
        ], "#208263"),
        (627, 1015, "ROOT / SUDO (с. 77–78)", [
            "sudo vipw: привилегированное изменение",
            "visudo: синтаксическая проверка sudoers",
            "journalctl SYSLOG_IDENTIFIER=sudo",
            "NOPASSWD: ALL = широкий риск"
        ], "#a64e40"),
        (1209, 1015, "ГРАНИЦА ИЗМЕНЕНИЙ", [
            "Сначала baseline: pwd / ls / ps",
            "Узнать цель и побочные эффекты",
            "Проверить результат read-only",
            "Rollback неизвестен → [Needs confirmation]"
        ], "#a64e40")
    ]
    for x,y,heading,lines,col in c:
        card(s,x,y,545,245,heading,lines,col,19,35)
    box(s,45,1311,1710,119,"#fcece9",17,"#d08063")
    label(s,73,1351,"КРИТИЧНЫЕ ОПЕРАЦИИ",24,True,"#a13e2c")
    label(s,73,1385,"rm -r • kill -KILL • chmod • tar x • sudo • > file: сначала безопасная цель, контроль и откат.",20)
    label(s,48,1481,"Глава 2 · PDF/печатные страницы 39–78 · RAG p0039:c01–p0078:c01 · схемы построены по тексту",17,color=MUTED)
    return s

def save(svg, name):
    OUT.mkdir(parents=True, exist_ok=True)
    ET.indent(svg, space="  ")
    ET.ElementTree(svg).write(OUT / name, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    save(compact(), "visual-cheatsheet.svg")
    save(detailed(), "visual-cheatsheet-detailed.svg")
    print("Rendered 2 SVG files:", OUT)
