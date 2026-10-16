from figstyle import *

H = 880
fig, ax = canvas(H)
title(ax, "HID input reports, byte by byte")

USED, PAD, EX = "#fbefe0", "#f1efea", AMBER
CW, CH, X0 = 128, 58, 330

reports = [
    ("Keyboard", "report ID 1 · 8 bytes", 150,
     [("modifiers", "8 key bits", True), ("reserved", "always 0", False),
      ("key 1", "usage code", True), ("key 2", "", True), ("key 3", "", True),
      ("key 4", "", True), ("key 5", "", True), ("key 6", "", True)],
     ["00", "00", "4E", "00", "00", "00", "00", "00"],
     "Page Down pressed (usage 0x4E). All zeros 30 ms later releases it."),
    ("Relative mouse", "report ID 2 · 4 bytes", 345,
     [("buttons", "3 bits + 5 pad", True), ("dx", "int8, px", True), ("dy", "int8, px", True),
      ("wheel", "int8", True)],
     ["00", "05", "00", "00"],
     "One square step: move 5 px right. dx and dy run from −127 to +127."),
    ("Absolute pointer", "report ID 3 · 5 bytes", 540,
     [("buttons", "3 bits + 5 pad", True), ("X low", "", True), ("X high", "", True),
      ("Y low", "", True), ("Y high", "", True)],
     ["00", "00", "40", "00", "40"],
     "Centre of the screen: X = Y = 0x4000 = 16384, on a 0 to 32767 scale, low byte first."),
]

for name, sub, y, cells, ex, note in reports:
    label(ax, X0 - 30, y + 18, name, size=14.5, ha="right", fontweight="bold")
    label(ax, X0 - 30, y + 44, sub, size=12, ha="right", color=GREY)
    for i, ((head, hint, used), val) in enumerate(zip(cells, ex)):
        x = X0 + i * CW
        ax.add_patch(Rectangle((x, y), CW, CH, fc=USED if used else PAD, ec=INK, lw=1.5))
        label(ax, x + CW / 2, y + 18, head, size=12.5, fontweight="bold")
        if hint:
            label(ax, x + CW / 2, y + 41, hint, size=10, color=GREY, linespacing=1.1)
        label(ax, x + CW / 2, y - 14, f"byte {i}", size=10.5, color=GREY)
        label(ax, x + CW / 2, y + CH + 26, val, size=15, color=EX, fontfamily=MONO,
              fontweight="bold")
    label(ax, X0, y + CH + 62, note, size=12.5, ha="left")

label(ax, X0 - 30, 150 + CH + 26, "example", size=11.5, ha="right", color=AMBER)

footer(fig, ax, 710,
       "the three input reports COMET-Test sends, as declared in its HID report map. Windows reads "
       "the map when it pairs and from then on decodes every notification with it, "
       "which is how one Bluetooth device can be a keyboard, a mouse and an absolute pointer at the "
       "same time. Over Bluetooth LE the report ID is not in the bytes themselves: each report has "
       "its own GATT characteristic, tagged with its ID. The amber values are what the sketch "
       "actually sends.", size=14.5, line_h=31)
save(fig, "hid_report_layout.png")
