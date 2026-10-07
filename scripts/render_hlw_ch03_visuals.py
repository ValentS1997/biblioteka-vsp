from pathlib import Path
import xml.etree.ElementTree as ET

N = "http://www.w3.org/2000/svg"
ET.register_namespace("", N)
P = Path("books/how-linux-works-brian-ward-3e-ru-2022/notes/chapters/chapter-03-devices")
CARDS = [
    ("DEV NODES", ["/dev: b / c / p / s", "Block / character / IPC", "Major и minor"]),
    ("SYSFS", ["/sys/devices: топология", "/sys/block: блочные устройства", "Атрибуты оборудования"]),
    ("UDEV", ["devtmpfs: узлы ядра", "uevent -> udevd rules", "Права и /dev/disk/by-id"]),
    ("OBSERVE", ["ls /dev; lsscsi", "udevadm info / monitor", "nvme list; journalctl -k"]),
    ("SCSI STACK", ["Upper: sd / sr", "Middle: сообщения", "Lower: USB / libata"]),
    ("SAFETY", ["dd: риск записи", "mknod: привилегии", "Rollback: Needs confirmation"])
]
def render(name, detailed=False):
    w, h = (1800, 1120) if detailed else (1600, 820)
    root = ET.Element("{%s}svg" % N, {"viewBox": f"0 0 {w} {h}"})
    def add(kind, **a):
        return ET.SubElement(root, "{%s}%s" % (N, kind), {k.replace("_","-"):str(v) for k,v in a.items()})
    def box(x,y,bw,bh,color="#ffffff"):
        add("rect",x=x,y=y,width=bw,height=bh,rx=16,fill=color)
    def text(x,y,v,fs=21,color="#24384d",bold=False):
        el=add("text",x=x,y=y,font_family="Arial,sans-serif",font_size=fs,
               font_weight="700" if bold else "400",fill=color)
        el.text=v
    t=add("title");t.text="Глава 3 — Устройства"
    box(0,0,w,h,"#f2f6fb")
    box(0,0,w,135,"#1a304c")
    text(48,58,"Глава 3 — Устройства Linux",38,"#ffffff",True)
    text(48,104,"/dev • sysfs • devtmpfs • udev • SCSI",23,"#d4e7ff")
    cols=3 if detailed else 2
    row_h=270 if detailed else 284
    gap=22
    card_w=(w-96-gap*(cols-1))//cols
    chosen=CARDS if detailed else CARDS[:4]
    for i,(header,lines) in enumerate(chosen):
        x=48+(i%cols)*(card_w+gap)
        y=165+(i//cols)*row_h
        box(x,y,card_w,row_h-20)
        text(x+24,y+49,header,25,"#1c639b",True)
        for k,line in enumerate(lines):
            text(x+24,y+106+k*42,line,21)
    footer_y=1060 if detailed else 780
    if detailed:
        box(48,740,1704,248,"#fbe9e5")
        text(72,790,"CHECK / ROLLBACK",27,"#a04836",True)
        text(72,841,"Сначала установить реальный путь и атрибуты устройства.",23)
        text(72,890,"Изменения диска/udev требуют отдельной проверки и отката.",22)
        text(72,934,"Схема построена по RAG; не копия рисунков 3.1–3.3.",21)
    text(48,footer_y,"Уорд • глава 3 • PDF 79–101 • RAG p0079:c01–p0101:c01",18)
    P.mkdir(parents=True,exist_ok=True)
    ET.indent(root,space="  ")
    ET.ElementTree(root).write(P/name,encoding="utf-8",xml_declaration=True)
render("visual-cheatsheet.svg")
render("visual-cheatsheet-detailed.svg",True)
