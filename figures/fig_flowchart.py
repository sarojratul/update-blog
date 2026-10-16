from figstyle import *

H = 1225
fig, ax = canvas(H)
title(ax, "COMET-Test firmware flowchart")

MX, BX, CX = 400, 760, 1215

label(ax, MX, 100, "main: setup() once, then loop() forever", size=13, color=GREY)
box(ax, MX, 150, 300, 50, "Power on / reset", head_size=14, fc="#f7f4ec")
arrow(ax, MX, 175, MX, 205)
box(ax, MX, 237, 360, 64, "init_serial()", "USB serial, 115200 baud")
arrow(ax, MX, 269, MX, 305)
box(ax, MX, 360, 420, 110, "init_ble()",
    "Just Works pairing + bonding\nHID service built from REPORT_MAP\nadvertise as \"COMET-Test\"")
arrow(ax, MX, 415, MX, 438)

box(ax, MX, 470, 360, 64, "now = millis()", "read the time once per pass")
arrow(ax, MX, 502, MX, 530)
diamond(ax, MX, 595, 280, 130, "event flag\nset?")
arrow(ax, MX + 140, 595, BX - 170, 595)
label(ax, MX + 165, 580, "yes", size=12, color=GREY)
box(ax, BX, 595, 340, 112, "task_events()",
    "print it, clear the flag\nafter a disconnect: restart\nadvertising, demo back to IDLE")
line(ax, [(BX, 651), (BX, 690), (MX, 690)])
arrow(ax, MX, 660, MX, 735)
label(ax, MX - 22, 676, "no", size=12, color=GREY)

diamond(ax, MX, 800, 280, 130, "PC\nconnected?")
arrow(ax, MX + 140, 800, BX - 170, 800)
label(ax, MX + 165, 785, "no", size=12, color=GREY)
box(ax, BX, 800, 340, 86, "task_heartbeat()", "print \"advertising, waiting\"\nevery 5 s")
arrow(ax, MX, 865, MX, 904)
label(ax, MX - 25, 882, "yes", size=12, color=GREY)
box(ax, MX, 960, 420, 112, "task_demo(now)",
    "advance one phase when its time is up:\nsquare, centre jump, Page Down\n(see the timing diagram)")

line(ax, [(MX, 1016), (MX, 1042), (150, 1042), (150, 470)])
arrow(ax, 150, 470, MX - 180, 470)
line(ax, [(BX, 843), (BX, 1042), (MX, 1042)])
label(ax, 132, 760, "next pass", size=12, color=GREY, rotation=90)

ax.add_patch(FancyBboxPatch((1000, 395), 430, 560, boxstyle="round,pad=0,rounding_size=12",
                            fc="#fbfaf6", ec=LIGHT, lw=2))
label(ax, CX, 422, "BLE callbacks", size=15, fontweight="bold")
label(ax, CX, 462, "run in the NimBLE stack's task,\ntreated like an ISR: set flags, return",
      size=12, color=GREY)
box(ax, CX, 560, 380, 106, "onConnect",
    "connectMark_g = millis()\nconnectedFlag_g = 1\nconnectEvent_g = 1", sub_size=11.5)
box(ax, CX, 700, 380, 90, "onAuthenticationComplete",
    "store encrypted / bonded\nauthEvent_g = 1", sub_size=11.5, head_size=14)
box(ax, CX, 840, 380, 106, "onDisconnect",
    "connectedFlag_g = 0\nstore the reason code\ndisconnectEvent_g = 1", sub_size=11.5)
arrow(ax, 1000, 595, BX + 172, 595, color=AMBER, dashed=True, lw=2.2)
label(ax, 966, 570, "flags", size=12.5, color=AMBER)
label(ax, CX, 928, "the Bluetooth stack calls these, never main", size=11.5, color=GREY)

footer(fig, ax, 1085,
       "the sketch has no delay() anywhere. Each pass of loop() reads the time once and runs three "
       "short tasks, and each task checks its own timestamp, the non-blocking pattern from CME 331's "
       "Lab 2. The Bluetooth callbacks only set volatile flags; main does the printing and restarts "
       "advertising. Rectangles do something and continue, diamonds decide.")
save(fig, "comet_test_flowchart.png")
