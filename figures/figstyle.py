"""Shared drawing helpers matching the turn signal blog diagrams:
cream rounded frame, monospace caps title, amber traces, 'What it shows:' footer."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

W = 1500
FRAME = "#e3dccb"
TITLE = "#5b5346"
INK = "#1e1a16"
GREY = "#6b665e"
LIGHT = "#d8d2c2"
AMBER = "#b5651d"
BAND = "#f2f2f2"
SANS = "DejaVu Sans"
MONO = "DejaVu Sans Mono"


def canvas(h):
    fig = plt.figure(figsize=(W / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((3, 3), W - 6, h - 6, boxstyle="round,pad=0,rounding_size=14",
                                fc="white", ec=FRAME, lw=2.5))
    return fig, ax


def title(ax, text):
    ax.text(32, 48, text.upper(), fontfamily=MONO, fontweight="bold", fontsize=17,
            color=TITLE, va="center", ha="left")


def text_width(fig, ax, s, **kw):
    t = ax.text(0, 0, s, **kw)
    fig.canvas.draw()
    w = t.get_window_extent().width
    t.remove()
    return w


def footer(fig, ax, y, body, lead="What it shows: ", size=15, line_h=33, maxw=1436):
    ax.plot([32, 1468], [y, y], color=LIGHT, lw=1.5)
    y += 38
    kw_b = dict(fontfamily=SANS, fontsize=size, fontweight="bold", color=INK, va="center")
    kw_n = dict(fontfamily=SANS, fontsize=size, color=GREY, va="center")
    lead_w = text_width(fig, ax, lead, **kw_b)
    ax.text(32, y, lead, **kw_b)
    space = text_width(fig, ax, "a b", **kw_n) - text_width(fig, ax, "ab", **kw_n)
    x0 = 32 + lead_w
    line = ""
    for word in body.split():
        trial = (line + " " + word).strip()
        if x0 + text_width(fig, ax, trial, **kw_n) > 32 + maxw:
            ax.text(x0, y, line, **kw_n)
            y += line_h
            x0 = 32
            line = word
        else:
            line = trial
    ax.text(x0, y, line, **kw_n)
    return y + 30


def box(ax, cx, cy, w, h, head, sub=None, fc="white", ec=INK, lw=2, head_size=15,
        sub_size=12, dashed=False, sub_color=GREY):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=10", fc=fc, ec=ec, lw=lw,
                                ls="--" if dashed else "-"))
    if sub:
        n = sub.count("\n") + 1
        block = 24 + n * sub_size * 1.9
        top = cy - block / 2
        ax.text(cx, top + 10, head, ha="center", va="center", fontfamily=SANS,
                fontweight="bold", fontsize=head_size, color=INK)
        ax.text(cx, top + 26, sub, ha="center", va="top", fontfamily=SANS,
                fontsize=sub_size, color=sub_color, linespacing=1.35)
    else:
        ax.text(cx, cy, head, ha="center", va="center", fontfamily=SANS,
                fontweight="bold", fontsize=head_size, color=INK)


def diamond(ax, cx, cy, w, h, text, size=13):
    ax.add_patch(Polygon([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
                         closed=True, fc="white", ec=INK, lw=2))
    ax.text(cx, cy, text, ha="center", va="center", fontfamily=SANS, fontsize=size,
            color=INK, linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=2, dashed=False, rad=0.0, head=18):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=head,
                                shrinkA=0, shrinkB=0, ls="--" if dashed else "-",
                                connectionstyle=f"arc3,rad={rad}"))


def line(ax, pts, color=INK, lw=2, dashed=False):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls="--" if dashed else "-", solid_capstyle="butt")


def label(ax, x, y, s, size=13, color=INK, ha="center", va="center", **kw):
    kw.setdefault("fontfamily", SANS)
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color, **kw)


def save(fig, path):
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)
