from figstyle import *

H = 1070
fig, ax = canvas(H)
title(ax, "COMET-Test timing, one demo cycle")

X0, X1, TMAX = 300, 1430, 11500.0
def px(t):
    return X0 + t * (X1 - X0) / TMAX

SQ_END, ABS_T, KEY_T, KEY_UP, NEXT = 632, 2632, 4632, 4662, 10662

rows = [("Relative mouse", "report ID 2", 235),
        ("Absolute pointer", "report ID 3", 330),
        ("Keyboard", "report ID 1", 425),
        ("Serial Monitor", "status lines", 520)]
LOW, HIGH = 22, -22

for name, sub, y in rows:
    label(ax, X0 - 30, y - 9, name, size=13.5, ha="right", fontweight="bold")
    label(ax, X0 - 30, y + 13, sub, size=11.5, ha="right", color=GREY)

# shaded bands where reports go out
for a, b in [(0, SQ_END), (NEXT, NEXT + SQ_END)]:
    ax.add_patch(Rectangle((px(a), 190), px(b) - px(a), 360, fc=BAND, ec="none", zorder=1))

# relative mouse: 80 notifications, drawn as ticks
y = rows[0][2]
line(ax, [(X0, y + LOW), (X1, y + LOW)], color=AMBER, lw=2.2)
for start in (0, NEXT):
    for k in range(80):
        t = start + k * 8
        if t <= TMAX:
            ax.plot([px(t), px(t)], [y + LOW, y + HIGH], color=AMBER, lw=0.9)
label(ax, px(SQ_END) + 12, y - 4, "80 reports, 8 ms apart (125 Hz)", size=12, ha="left", color=AMBER)

# absolute pointer: one report
y = rows[1][2]
line(ax, [(X0, y + LOW), (X1, y + LOW)], color=AMBER, lw=2.2)
ax.plot([px(ABS_T)] * 2, [y + LOW, y + HIGH], color=AMBER, lw=2.4)
label(ax, px(ABS_T) + 12, y - 4, "one report: x = y = 16384, centre of the screen", size=12,
      ha="left", color=AMBER)

# keyboard: Page Down press and release
y = rows[2][2]
line(ax, [(X0, y + LOW), (px(KEY_T), y + LOW), (px(KEY_T), y + HIGH), (px(KEY_UP), y + HIGH),
          (px(KEY_UP), y + LOW), (X1, y + LOW)], color=AMBER, lw=2.2)
label(ax, px(KEY_UP) + 12, y - 4, "Page Down held 30 ms, then released", size=12, ha="left",
      color=AMBER)

# serial markers
y = rows[3][2]
line(ax, [(X0, y), (X1, y)], color=LIGHT, lw=1.5, dashed=True)
for t, s in [(0, "1/3"), (ABS_T, "2/3"), (KEY_T, "3/3"), (NEXT, "1/3")]:
    ax.plot(px(t), y, marker="o", ms=8, color=INK)
    label(ax, px(t), y + 22, s, size=11.5, color=GREY)

# dimension bars above
def dim(a, b, yy, text, above=True):
    line(ax, [(px(a), yy), (px(b), yy)], lw=1.3)
    for t in (a, b):
        line(ax, [(px(t), yy - 7), (px(t), yy + 7)], lw=1.3)
    label(ax, (px(a) + px(b)) / 2, yy - 24 if above else yy + 20, text, size=11.5,
          linespacing=1.25)

dim(SQ_END, ABS_T, 150, "PAUSE_AFTER_SQUARE\n2000 ms")
dim(ABS_T, KEY_T, 150, "PAUSE_AFTER_CENTRE\n2000 ms")
dim(KEY_UP, NEXT, 150, "PAUSE_AFTER_KEY\n6000 ms")

# time axis
AY = 590
line(ax, [(X0, AY), (X1, AY)], lw=1.3)
for t in (0, SQ_END, ABS_T, KEY_T, NEXT):
    line(ax, [(px(t), AY), (px(t), AY + 8)], lw=1.3)
    label(ax, px(t), AY + 24, f"{t}", size=11.5, color=GREY)
label(ax, (X0 + X1) / 2, AY + 50, "time after the demo starts (ms)", size=12, color=GREY)
dim(0, NEXT, 680, "one cycle = 10662 ms, about 10.7 s, then it repeats", above=False)

# inset: cursor path during the burst
IX, IY, S = 360, 760, 110
label(ax, IX - 30, IY - 20, "Cursor path during the burst", size=13, ha="left", fontweight="bold")
pts = [(IX, IY + 20), (IX + S, IY + 20), (IX + S, IY + 20 + S), (IX, IY + 20 + S), (IX, IY + 20)]
for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
    arrow(ax, xa, ya, xb, yb, color=AMBER, lw=2.4, head=16)
ax.plot(IX, IY + 20, marker="o", ms=7, color=INK)
label(ax, IX + S / 2, IY + 8, "right", size=11, color=GREY)
label(ax, IX + S + 12, IY + 20 + S / 2, "down", size=11, color=GREY, ha="left")
label(ax, IX + S / 2, IY + 36 + S, "left", size=11, color=GREY)
label(ax, IX - 12, IY + 20 + S / 2, "up", size=11, color=GREY, ha="right")
label(ax, IX + S + 70, IY + 40, "20 steps of 5 px per side", size=12, ha="left")
label(ax, IX + S + 70, IY + 66, "= 100 px square, ending where it began", size=12, ha="left",
      color=GREY)
label(ax, IX + S + 70, IY + 100, "Before the first cycle: SETTLE_TIME 3000 ms after", size=12,
      ha="left")
label(ax, IX + S + 70, IY + 126, "connecting, so Windows finishes setting up the HID service",
      size=12, ha="left", color=GREY)

footer(fig, ax, 960,
       "what the test sketch sends once it is connected, drawn from the firmware constants and a "
       "host simulation of the sketch, not from a scope. On 2 October all three report types worked "
       "on my laptop over Bluetooth LE.", size=15)
save(fig, "comet_test_timing.png")
