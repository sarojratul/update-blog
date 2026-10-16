from figstyle import *
H = 950
fig, ax = canvas(H)
title(ax, "Timing diagram, LEFT sweep, two cycles")
X0, X1, T = 260, 1370, 3376.0
px = lambda t: X0 + t * (X1 - X0) / T
for a, b in [(900, 1688), (2588, 3376)]:
    ax.add_patch(Rectangle((px(a), 200), px(b) - px(a), 370, fc=BAND, ec="none", zorder=1))
rows = [("A · GPIO3", None, 250, [(0, 0), (900, 1), (1688, 0), (2588, 1), (3376, 1)]),
        ("B · GPIO4", None, 345, [(0, 0), (450, 1), (1688, 0), (2138, 1), (3376, 1)]),
        ("C · GPIO5", None, 440, [(0, 1), (3376, 1)]),
        ("D · GPIO6", "unused for LEFT", 535, None)]
for name, sub, y, wave in rows:
    label(ax, X0 - 30, y - (8 if sub else 0), name, size=13.5, ha="right", fontfamily=MONO)
    if sub:
        label(ax, X0 - 30, y + 14, sub, size=11, ha="right", color=GREY)
    if wave is None:
        line(ax, [(X0, y + 18), (X1, y + 18)], color=GREY, lw=1.5, dashed=True)
        continue
    pts = []
    for i, (t, v) in enumerate(wave):
        yy = y + (-20 if v else 20)
        if i and pts[-1][1] != yy:
            pts.append((px(t), pts[-1][1]))
        pts.append((px(t), yy))
    line(ax, pts, color=AMBER, lw=2.6)
label(ax, X1 + 8, 420, "always on", size=11.5, color=AMBER, ha="left")
ax.plot([px(1688)] * 2, [150, 600], color=GREY, lw=1.3, ls=(0, (4, 4)))
label(ax, px(1688) + 10, 165, "cycle repeats", size=11.5, color=GREY, ha="left")
def dim(a, b, yy, text, dy=-18):
    line(ax, [(px(a), yy), (px(b), yy)], lw=1.3)
    for t in (a, b):
        line(ax, [(px(t), yy - 7), (px(t), yy + 7)], lw=1.3)
    label(ax, (px(a) + px(b)) / 2, yy + dy, text, size=12.5)
dim(0, 450, 150, "STEP_MS 450 ms")
dim(900, 1688, 120, "HOLD_MS 788 ms")
AY = 610
line(ax, [(X0, AY), (X1, AY)], lw=1.3)
for t in (0, 450, 900, 1688, 2138, 2588, 3376):
    line(ax, [(px(t), AY), (px(t), AY + 8)], lw=1.3)
    label(ax, px(t), AY + 25, str(t), size=11.5, color=GREY)
label(ax, (X0 + X1) / 2, AY + 52, "time (ms)", size=12, color=GREY)
dim(0, 1688, 705, "CYCLE_MS 1688 ms (0.59 Hz)", dy=22)
footer(fig, ax, 770, "segments join centre-out and accumulate (C, then C+B, then C+B+A) and stay lit together "
       "until the 1688 ms cycle wraps straight back to C with no blank gap. C is on whenever a direction is held, "
       "since it is part of every step; only B and A toggle. The shaded band is the 788 ms HOLD_MS full-arrow "
       "phase. RIGHT mirrors this as B, B+C, B+C+D, with A dark. BRIGHTNESS = 255, so high means full PWM duty. "
       "Measured on an Analog Discovery 2 on 20 September 2026: STEP_MS 446.9 ms, CYCLE_MS 1689 ms.", size=14.5, line_h=31)
save(fig, "sweep_timing_diagram.png")
