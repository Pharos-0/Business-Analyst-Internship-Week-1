"""Chart and diagram helpers shared by the figure scripts (matplotlib).

Colour rules:
- Categorical identity uses a fixed hue order (blue, orange, aqua, yellow, magenta, green, violet, red),
  assigned in that order and never cycled.
- Magnitude uses one hue (a light-to-dark blue ramp).
- Status colours (good, warning, serious, critical) are only used for states such as risk severity,
  and always appear with a text label.
- Text stays in ink colours; gridlines and axes are solid hairlines.
"""
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
BLUE = {100: "#cde2fb", 150: "#b7d3f6", 200: "#9ec5f4", 250: "#86b6ef", 300: "#6da7ec", 350: "#5598e7",
        400: "#3987e5", 450: "#2a78d6", 500: "#256abf", 550: "#1c5cab", 600: "#184f95", 650: "#104281",
        700: "#0d366b"}
STATUS = {"good": "#0ca30c", "warning": "#fab219", "serious": "#ec835a", "critical": "#d03b3b"}
TINT = {"blue": "#e9f1fc", "orange": "#fdeee7", "aqua": "#e2f5ee", "yellow": "#fdf3dd", "magenta": "#fcedf3",
        "green": "#e3f1e3", "violet": "#ecebfa", "red": "#fbe8e8", "grey": "#f2f2ef"}
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
NAVY = "#1f3a5f"
DPI = 220

plt.rcParams.update({
    "font.family": ["Arial", "DejaVu Sans"],
    "font.size": 8.5,
    "axes.edgecolor": AXIS,
    "axes.linewidth": 0.8,
    "axes.labelcolor": INK2,
    "axes.titlesize": 9.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "legend.frameon": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def cm(value):
    return value / 2.54


def save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.06, facecolor="white", metadata={"Software": None})
    plt.close(fig)
    return path


def wrap(text, width):
    return "\n".join(textwrap.fill(part, width) if part else "" for part in str(text).split("\n"))


def canvas(width_cm, height_cm, xlim=(0, 100), ylim=(0, 100)):
    """A blank drawing area with data coordinates 0-100 on both axes."""
    fig, ax = plt.subplots(figsize=(cm(width_cm), cm(height_cm)))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def box(ax, x, y, w, h, text, fill=TINT["blue"], edge=BLUE[550], size=8, weight="normal", color=INK,
        wrap_at=None, align="center", lw=0.9, radius=1.0, ls="-", zorder=2):
    """Rounded box with centred (or left-aligned) text. Returns the geometry for anchors."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}", fc=fill, ec=edge,
                           lw=lw, ls=ls, zorder=zorder)
    ax.add_patch(patch)
    if wrap_at:
        text = wrap(text, wrap_at)
    if align == "center":
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color,
                weight=weight, linespacing=1.3, zorder=zorder + 1)
    else:
        ax.text(x + 1.2, y + h / 2, text, ha="left", va="center", fontsize=size, color=color,
                weight=weight, linespacing=1.3, zorder=zorder + 1)
    return {"x": x, "y": y, "w": w, "h": h}


def anchor(b, side, offset=0.0):
    """Mid-point of a box side: 'l', 'r', 't' or 'b'; offset shifts along the side."""
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return {"l": (x, y + h / 2 + offset), "r": (x + w, y + h / 2 + offset),
            "t": (x + w / 2 + offset, y + h), "b": (x + w / 2 + offset, y)}[side]


def arrow(ax, start, end, color=INK2, lw=0.9, rad=0.0, text=None, text_xy=None, size=7, ls="-",
          both=False, zorder=1):
    style = "<|-|>" if both else "-|>"
    patch = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=8, color=color, lw=lw,
                            connectionstyle=f"arc3,rad={rad}", linestyle=ls, shrinkA=0, shrinkB=0,
                            zorder=zorder)
    ax.add_patch(patch)
    if text:
        tx, ty = text_xy or ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(tx, ty, text, ha="center", va="center", fontsize=size, color=INK2, zorder=zorder + 2,
                bbox=dict(fc="white", ec="none", pad=0.8))


def path_arrow(ax, points, color=INK2, lw=0.9, text=None, text_xy=None, size=7, ls="-"):
    """Orthogonal connector through `points`, with an arrow head on the last segment."""
    xs, ys = zip(*points[:-1])
    ax.plot(list(xs) + [points[-1][0]], list(ys) + [points[-1][1]], color=color, lw=lw, ls=ls, zorder=1,
            solid_capstyle="butt")
    arrow(ax, points[-2], points[-1], color=color, lw=lw, ls=ls)
    if text:
        ax.text(*(text_xy or points[len(points) // 2]), text, ha="center", va="center", fontsize=size,
                color=INK2, bbox=dict(fc="white", ec="none", pad=0.8), zorder=4)


def label(ax, x, y, text, size=8, color=INK, weight="normal", ha="center", va="center", wrap_at=None,
          style="normal"):
    if wrap_at:
        text = wrap(text, wrap_at)
    ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color, weight=weight, linespacing=1.3,
            style=style)


def hairline_grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def quadrant(ax, points, xlabel, ylabel, quad_labels, xlim=(0, 10), ylim=(0, 10), split=(5, 5),
             marker_color=SERIES[0], size=7.5):
    """2x2 grid (e.g. power/interest). points: dicts with label, x, y and optional dx, dy, ha."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axvline(split[0], color=AXIS, lw=0.8, zorder=0)
    ax.axhline(split[1], color=AXIS, lw=0.8, zorder=0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(AXIS)
    corners = [(xlim[0] + 0.15, ylim[1] - 0.2, "left"), (xlim[1] - 0.15, ylim[1] - 0.2, "right"),
               (xlim[0] + 0.15, ylim[0] + 0.25, "left"), (xlim[1] - 0.15, ylim[0] + 0.25, "right")]
    for (cx, cy, ha), text in zip(corners, quad_labels):
        va = "top" if cy > split[1] else "bottom"
        ax.text(cx, cy, text, ha=ha, va=va, fontsize=8, color=MUTED, weight="bold")
    for point in points:
        ax.scatter(point["x"], point["y"], s=34, color=point.get("color", marker_color), zorder=3,
                   edgecolors="white", linewidths=1.2)
        ax.annotate(point["label"], (point["x"], point["y"]),
                    xytext=(point.get("dx", 5), point.get("dy", 0)), textcoords="offset points",
                    ha=point.get("ha", "left"), va="center", fontsize=size, color=INK)


def gantt(ax, rows, total_weeks, group_colors, milestones=(), row_height=0.62, label_size=7.6):
    """rows: dicts with label, start, end (inclusive weeks) and group. Earliest row at the top."""
    for index, row in enumerate(rows):
        y = len(rows) - 1 - index
        ax.barh(y, row["end"] - row["start"] + 1, left=row["start"] - 0.5, height=row_height,
                color=group_colors[row["group"]], edgecolor="white", linewidth=1.2, zorder=2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([row["label"] for row in rows][::-1], fontsize=label_size)
    ax.set_xlim(0.5, total_weeks + 0.5)
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.set_xticks(range(1, total_weeks + 1))
    ax.set_xticklabels([str(w) for w in range(1, total_weeks + 1)], fontsize=7)
    ax.xaxis.tick_top()
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    for week, text in milestones:
        ax.axvline(week + 0.5, color=NAVY, lw=0.9, zorder=3)
        ax.text(week + 0.5, -0.75, text, rotation=0, ha="center", va="bottom", fontsize=6.8, color=NAVY,
                weight="bold", bbox=dict(fc="white", ec="none", pad=0.4), zorder=4)


def heatmap(ax, matrix, row_labels, col_labels, colors, text=None, text_colors=None, size=7.2, gap=1.0,
            col_rotation=0):
    """Cell grid. colors/text/text_colors are matrices of the same shape as `matrix` (lists of lists)."""
    n_rows, n_cols = len(matrix), len(matrix[0])
    for r in range(n_rows):
        for c in range(n_cols):
            ax.add_patch(Rectangle((c, n_rows - 1 - r), 1, 1, fc=colors[r][c], ec="white", lw=gap))
            if text and text[r][c]:
                ax.text(c + 0.5, n_rows - 1 - r + 0.5, text[r][c], ha="center", va="center", fontsize=size,
                        color=(text_colors[r][c] if text_colors else INK))
    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_xticks([c + 0.5 for c in range(n_cols)])
    ax.set_xticklabels(col_labels, fontsize=7.2, rotation=col_rotation, ha="left" if col_rotation else "center",
                       rotation_mode="anchor")
    ax.set_yticks([n_rows - 1 - r + 0.5 for r in range(n_rows)])
    ax.set_yticklabels(row_labels, fontsize=7.4)
    ax.xaxis.tick_top()
    for spine in ax.spines.values():
        spine.set_visible(False)


def legend_patches(ax, items, loc="upper center", bbox=(0.5, -0.02), ncol=None, size=7.5):
    handles = [Rectangle((0, 0), 1, 1, fc=color, ec="none") for _, color in items]
    ax.legend(handles, [name for name, _ in items], loc=loc, bbox_to_anchor=bbox, ncol=ncol or len(items),
              fontsize=size, handlelength=1.0, handleheight=0.9, columnspacing=1.4, borderaxespad=0)
