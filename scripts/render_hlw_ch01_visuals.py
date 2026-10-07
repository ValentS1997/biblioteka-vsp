"""One-shot standard-library renderer for two RAG-grounded chapter 1 SVG overviews.

Sources: page chunks p0028:c01–p0038:c01; no additional Linux facts.
Outputs only the two canonical visual chapter summary files.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

BOOK = "how-linux-works-brian-ward-3e-ru-2022"
OUT = Path("books") / BOOK / "notes/chapters/chapter-01-big-picture"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
FONT = "system-ui,-apple-system,Segoe UI,Arial,sans-serif"

def el(parent, name, **attrs):
    return ET.SubElement(parent, f"{{{SVG_NS}}}{name}", {k.replace("_", "-"): str(v) for k,v in attrs.items()})

def label(parent, x, y, message, size=20, weight="400", color="#21344a"):
    t = el(parent, "text", x=x, y=y, fill=color, font_family=FONT,
           font_size=size, font_weight=weight)
    t.text = message
    return t

def rectangle(parent, x, y, width, height, fill, radius=0, stroke=None, border=0):
    args = dict(x=x,y=y,width=width,height=height,fill=fill,rx=radius)
    if stroke:
        args.update(stroke=stroke,stroke_width=border)
    return el(parent,"rect",**args)

def card(parent,x,y,w,h,title,lines,color,size=20,spacing=39):
    rectangle(parent,x,y,w,h,"#ffffff",18,color,2)
    rectangle(parent,x,y,w,10,color,5)
    label(parent,x+24,y+51,title,25,"700",color)
    for i,line in enumerate(lines):
        label(parent,x+24,y+96+i*spacing,line,size,"400")
        
def base(width,height,title,subtitle,desc):
    svg=ET.Element(f"{{{SVG_NS}}}svg",{
        "viewBox":f"0 0 {width} {height}",
        "width":str(width),"height":str(height),
        "role":"img","aria-labelledby":"title desc",
    })
    t=el(svg,"title",id="title");t.text=title
    d=el(svg,"desc",id="desc");d.text=desc
    rectangle(svg,0,0,width,height,"#f1f6fc")
    rectangle(svg,0,0,width,133,"#172941")
    label(svg,54,55,title,37,"750","#ffffff")
    label(svg,54,99,subtitle,21,"400","#d7e7ff")
    return svg

def compact():
    svg=base(1600,900,"Глава 1 — Общая картина","Объекты • уровни • границы привилегий",
             "Три уровня Linux и четыре функции ядра; UID, группы и root.")
    card(svg,48,166,460,228,"USER SPACE",[
        "Приложения, службы, процессы",
        "Режим: ограниченный доступ",
        "Обращение к ядру: syscalls"
    ],"#22688a")
    card(svg,572,166,460,228,"KERNEL",[
        "Управляет CPU и памятью",
        "Связывает процессы и устройства",
        "Kernel mode: широкий доступ"
    ],"#66529b")
    card(svg,1096,166,456,228,"HARDWARE",[
        "CPU, оперативная память",
        "Диски и сетевые интерфейсы",
        "Физический уровень"
    ],"#277452")
    label(svg,522,292,"↔",42,"700","#334969")
    label(svg,1044,292,"↔",42,"700","#334969")
    label(svg,52,447,"ЧЕТЫРЕ ОБЛАСТИ РАБОТЫ ЯДРА",27,"700","#1b3656")
    card(svg,48,474,358,246,"01 · ПРОЦЕССЫ",[
        "Планирование и квант",
        "Переключение контекста",
        "Сохранить / выбрать / вернуть"
    ],"#22688a",19,39)
    card(svg,430,474,358,246,"02 · ПАМЯТЬ",[
        "Изоляция областей",
        "Виртуальные адреса и MMU",
        "Таблицы страниц"
    ],"#66529b",19,39)
    card(svg,812,474,358,246,"03 · ДРАЙВЕРЫ",[
        "Посредник к устройствам",
        "Единый интерфейс",
        "Различия оборудования"
    ],"#277452",19,39)
    card(svg,1194,474,358,246,"04 · SYSCALLS",[
        "Процесс запрашивает ядро",
        "fork(): создаёт процесс",
        "exec(): заменяет программу"
    ],"#a8662a",19,39)
    rectangle(svg,48,754,1504,80,"#e0eaf5",14)
    label(svg,75,786,"ГРАНИЦЫ:",21,"750","#243851")
    label(svg,75,816,"UID — процессы/файлы  •  groups — общий доступ  •  root не означает kernel mode",20)
    label(svg,52,871,"Уорд · глава 1 · PDF/печатные с. 28–38 · RAG p0028:c01–p0038:c01 · схема составлена по тексту",16,"400","#5a6d81")
    return svg

def detailed():
    svg=base(1800,1320,"Глава 1 — Подробная карта Linux",
             "Общая картина · абстракции → механизмы ядра → пользователи",
             "Слои Linux; планирование CPU, MMU, драйверы, fork/exec, UID/root.")
    card(svg,48,174,540,230,"01 · USER SPACE",[
        "Программы и процессы в user mode",
        "Примеры: браузер, службы и syslog",
        "Сервисы могут зависеть друг от друга",
        "Слои внутри user space условны"
    ],"#22688a",20,34)
    card(svg,632,174,540,230,"02 · KERNEL",[
        "Посредник между программой и hardware",
        "Управляет процессами и RAM",
        "Драйверы, системные вызовы",
        "Kernel mode / защищённая область"
    ],"#66529b",20,34)
    card(svg,1216,174,536,230,"03 · HARDWARE",[
        "CPU: инструкции и вычисления",
        "RAM: состояние ядра и процессов",
        "Диски, сетевые интерфейсы",
        "Разграничение операций — через ядро"
    ],"#277452",20,34)
    label(svg,595,302,"↔",30,"700","#4e6480")
    label(svg,1176,302,"↔",30,"700","#4e6480")
    label(svg,48,458,"ОСНОВНЫЕ ФУНКЦИИ ЯДРА",27,"750","#193650")
    card(svg,48,479,401,255,"ПРОЦЕССЫ",[
        "Временные кванты CPU",
        "Таймерное прерывание",
        "Сохранение контекста",
        "Выбор следующего процесса"
    ],"#22688a",20,35)
    card(svg,481,479,401,255,"ПАМЯТЬ",[
        "Изоляция и разделение",
        "Виртуальные адреса → MMU",
        "Таблицы страниц",
        "Ядро обновляет отображения"
    ],"#66529b",20,35)
    card(svg,914,479,401,255,"ДРАЙВЕРЫ",[
        "Устройства обычно через ядро",
        "Унификация интерфейсов",
        "Диски / сетевые адаптеры",
        "Скрытие аппаратных различий"
    ],"#277452",20,35)
    card(svg,1347,479,405,255,"SYSTEM CALLS",[
        "Запрос процесса к ядру",
        "Чтение / запись файлов",
        "fork() создаёт копию процесса",
        "exec() запускает программу"
    ],"#a8662a",20,35)
    label(svg,48,787,"ПРИМЕРЫ ПОВЕДЕНИЯ И ГРАНИЦ",27,"750","#193650")
    card(svg,48,807,827,303,"ПЕРЕКЛЮЧЕНИЕ КОНТЕКСТА",[
        "1. Таймер завершает квант; вход в kernel mode",
        "2. Ядро сохраняет состояние и выполняет задачи",
        "3. Планировщик выбирает готовый процесс",
        "4. Подготавливаются память, CPU и новый квант",
        "5. Возврат в user mode — продолжение процесса"
    ],"#22688a",20,39)
    card(svg,925,807,827,303,"ЗАПУСК ПРОЦЕССА И ПРАВА",[
        "Shell → fork() → дочерний процесс → exec(ls)",
        "fork()/exec() — API, не shell-команды",
        "UID связывает пользователя с процессами и файлами",
        "groups позволяют совместный доступ к файлам",
        "root обладает особыми правами, остаётся user mode"
    ],"#a8662a",20,39)
    rectangle(svg,48,1142,1704,116,"#e0eaf5",16)
    label(svg,77,1180,"OPERATIONAL BOUNDARY",22,"750","#24415c")
    label(svg,77,1214,"В главе нет диагностического runbook и действий по изменению конфигурации.",21)
    label(svg,77,1243,"ls — пример read-only команды; рисунки 1.1–1.3 не воспроизведены из графики PDF.",20)
    label(svg,51,1297,"Уорд · глава 1 · PDF/печатные с. 28–38 · p0028:c01–p0038:c01 · текстовая схема, не копия рисунков",17,"400","#5a6d81")
    return svg

def save(svg,filename):
    ET.indent(svg,space="  ")
    OUT.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(svg).write(OUT / filename,encoding="utf-8",xml_declaration=True)

if __name__ == "__main__":
    save(compact(),"visual-cheatsheet.svg")
    save(detailed(),"visual-cheatsheet-detailed.svg")
    print("Chapter 1 visual summaries rendered:",OUT)
