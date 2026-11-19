"""Draw the Week 1 figures from plan_data.py into outputs/figures."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

import charts as c
import plan_data as d

OUT = Path(__file__).resolve().parent.parent / "outputs" / "figures"
PHASE_COLORS = {p[0]: c.SERIES[i] for i, p in enumerate(d.PHASES)}


def fig_public_growth():
    """Small multiples of three public indicators (one measure per panel, so no shared or dual axis)."""
    panels = [
        ("Revenue from operations (₹ crore)", ["FY23", "FY24", "FY25", "FY26"],
         [d.m(f"rev_fy{y}") for y in (23, 24, 25, 26)]),
        ("Beauty GMV (₹ crore)", ["FY23", "FY24", "FY25", "FY26"],
         [d.m(f"gmv_beauty_fy{y}") for y in (23, 24, 25, 26)]),
        ("Nykaa stores at year end", ["FY22", "FY23", "FY24", "FY25", "FY26"],
         [d.m(f"stores_fy{y}") for y in (22, 23, 24, 25, 26)]),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(c.cm(16), c.cm(5.6)))
    for ax, (title, labels, values) in zip(axes, panels):
        bars = ax.bar(labels, values, color=c.SERIES[0], width=0.62, edgecolor="white", linewidth=1.2)
        bars[-1].set_color(c.BLUE[650])
        ax.set_title(title, loc="left", fontsize=8.6, pad=8)
        c.hairline_grid(ax, "y")
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=7.5)
        top = max(values)
        ax.set_ylim(0, top * 1.18)
        for index in (0, len(values) - 1):
            ax.text(index, values[index] + top * 0.025, f"{values[index]:,.0f}", ha="center", va="bottom",
                    fontsize=7.5, color=c.INK, weight="bold" if index == len(values) - 1 else "normal")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    fig.tight_layout(w_pad=2.2)
    return c.save(fig, OUT / "fig1_1_public_growth.png")


def fig_context():
    fig, ax = c.canvas(16, 10.5)
    core = c.box(ax, 33, 33, 34, 34,
                 "CCR solution (proposed)\n\nStore stock visibility\nClick & collect\nReturn to store\n"
                 "Assisted ordering\nStore staff tools\nRules, policies and KPIs",
                 fill=c.TINT["blue"], edge=c.NAVY, size=8.2, lw=1.4)
    c.label(ax, 50, 63.5, "", size=8)
    entities = {
        "online": c.box(ax, 1, 70, 23, 12, "Online customer\n(app and website)", fill=c.TINT["grey"], edge=c.AXIS),
        "store_cust": c.box(ax, 1, 40, 23, 12, "Store customer", fill=c.TINT["grey"], edge=c.AXIS),
        "care": c.box(ax, 1, 10, 23, 12, "Customer Care\n(grievance officer)", fill=c.TINT["grey"], edge=c.AXIS),
        "staff": c.box(ax, 38.5, 86, 23, 12, "Store staff\n(store app and POS)", fill=c.TINT["grey"], edge=c.AXIS),
        "oms": c.box(ax, 76, 70, 23, 12, "Order management\nsystem", fill=c.TINT["grey"], edge=c.AXIS),
        "inv": c.box(ax, 76, 40, 23, 12, "Inventory and\nPOS systems", fill=c.TINT["grey"], edge=c.AXIS),
        "logistics": c.box(ax, 76, 10, 23, 12, "Logistics partners", fill=c.TINT["grey"], edge=c.AXIS),
        "pay": c.box(ax, 38.5, 2, 23, 11, "Payments and refunds", fill=c.TINT["grey"], edge=c.AXIS),
    }
    flows = [
        (c.anchor(entities["online"], "r"), (33, 58), "orders, pickup choice\nstore stock, pickup code"),
        (c.anchor(entities["store_cust"], "r"), (33, 46), "returns, assisted orders"),
        (c.anchor(entities["care"], "r"), (33, 38), "case and refund status"),
        (c.anchor(entities["staff"], "b"), (50, 67), "handover, returns, tasks"),
        (c.anchor(entities["oms"], "l"), (67, 58), "store-reserved orders,\nstatus"),
        (c.anchor(entities["inv"], "l"), (67, 46), "store stock feed"),
        (c.anchor(entities["logistics"], "l"), (67, 38), "cancel reverse pickup"),
        (c.anchor(entities["pay"], "t"), (50, 33), "refund initiation"),
    ]
    label_at = {0: (20.5, 64.5), 4: (79.5, 64.5)}
    for index, (start, end, text) in enumerate(flows):
        tx, ty = label_at.get(index, ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2))
        c.arrow(ax, start, end, both=True, text=text, text_xy=(tx, ty), size=6.6)
    return c.save(fig, OUT / "fig1_2_context_diagram.png")


ID_OFFSETS = {  # points (dx, dy) for the ID label next to each marker
    "SH01": (-4, 6), "SH02": (-4, 6), "SH03": (-4, 6), "SH06": (-4, 6), "SH11": (-4, 6), "SH19": (-4, 6),
    "SH10": (-4, 6), "SH12": (-4, 6), "SH13": (-4, 6), "SH16": (-4, 6), "SH04": (-4, -7), "SH08": (-4, -7),
    "SH18": (-4, -7), "SH09": (-4, -7), "SH07": (-4, -7), "SH14": (-4, -7), "SH15": (-4, -7), "SH05": (-4, -7),
    "SH17": (-4, -7),
}


def fig_power_interest():
    fig = plt.figure(figsize=(c.cm(16), c.cm(9.6)))
    ax = fig.add_axes([0.07, 0.12, 0.56, 0.84])
    key = fig.add_axes([0.66, 0.06, 0.34, 0.92])
    key.axis("off")
    points = []
    for sh in d.STAKEHOLDERS:
        dx, dy = ID_OFFSETS[sh[0]]
        points.append({"label": sh[0], "x": sh[5], "y": sh[4], "dx": dx, "dy": dy, "ha": "left"})
    c.quadrant(ax, points, "Interest in the CCR programme (1-10)", "Power over the outcome (1-10)",
               ["KEEP SATISFIED", "MANAGE CLOSELY", "MONITOR", "KEEP INFORMED"],
               xlim=(0.5, 10.9), ylim=(0.5, 11.4), split=(d.SPLIT, d.SPLIT), size=6.6)
    y = 0.99
    for name, _, _ in d.QUADRANTS:
        members = [sh for sh in d.STAKEHOLDERS if d.quadrant_of(sh) == name]
        key.text(0.0, y, name, fontsize=7.4, weight="bold", color=c.NAVY, va="top", transform=key.transAxes)
        y -= 0.052
        for sh in members:
            key.text(0.0, y, f"{sh[0]}  {sh[7]}", fontsize=6.9, color=c.INK, va="top", transform=key.transAxes)
            y -= 0.040
        y -= 0.022
    return c.save(fig, OUT / "fig1_3_power_interest_grid.png")


def fig_timeline():
    rows = [{"label": f"{a[0]} {d.ACTIVITY_SHORT[a[0]]}", "start": a[3], "end": a[4], "group": a[1]}
            for a in d.ACTIVITIES]
    fig, ax = plt.subplots(figsize=(c.cm(16), c.cm(15.5)))
    c.gantt(ax, rows, d.TOTAL_WEEKS, PHASE_COLORS, milestones=[(g[1], g[0]) for g in d.GATES], label_size=6.6)
    c.legend_patches(ax, [(f"{p[0]} {p[1]}", PHASE_COLORS[p[0]]) for p in d.PHASES], bbox=(0.38, -0.035), ncol=4,
                     size=6.8)
    ax.set_xlabel("Project week (week 1 starts 4 January 2027)", fontsize=7.2, labelpad=6)
    ax.xaxis.set_label_position("top")
    return c.save(fig, OUT / "fig1_4_ba_activity_timeline.png")


def fig_capacity():
    demand = d.weekly_demand()
    capacity = d.weekly_capacity()
    total = [sum(demand[p][w] for p in demand) for w in range(d.TOTAL_WEEKS)]
    weeks = list(range(1, d.TOTAL_WEEKS + 1))
    colors = [c.SERIES[1] if t / cap >= 0.95 else c.SERIES[0] for t, cap in zip(total, capacity)]
    fig, ax = plt.subplots(figsize=(c.cm(16), c.cm(6.8)))
    ax.bar(weeks, total, color=colors, width=0.72, edgecolor="white", linewidth=1.0, zorder=2)
    step_x = [0.5] + [w + 0.5 for w in weeks]
    ax.step(step_x, [capacity[0]] + capacity, where="pre", color=c.NAVY, lw=1.6, zorder=3)
    c.hairline_grid(ax, "y")
    ax.set_xlim(0.4, d.TOTAL_WEEKS + 0.6)
    ax.set_ylim(0, 12.5)
    ax.set_xticks(weeks)
    ax.tick_params(axis="x", labelsize=7)
    ax.set_xlabel("Project week", fontsize=7.5)
    ax.set_ylabel("Person-days per week", fontsize=7.5)
    ax.spines["left"].set_visible(False)
    peak = max(range(d.TOTAL_WEEKS), key=lambda w: total[w] / capacity[w])
    ax.annotate(f"Peak {total[peak] / capacity[peak] * 100:.0f}% of capacity",
                (peak + 1, total[peak]), xytext=(peak + 5.2, 11.6), fontsize=7.2, color=c.INK,
                arrowprops=dict(arrowstyle="-", color=c.INK2, lw=0.7))
    handles = [Rectangle((0, 0), 1, 1, fc=c.SERIES[0]), Rectangle((0, 0), 1, 1, fc=c.SERIES[1]),
               plt.Line2D([0], [0], color=c.NAVY, lw=1.6)]
    ax.legend(handles, ["Planned BA effort", "Weeks at 95% of capacity or more", "Available BA capacity"],
              loc="upper right", fontsize=7, ncol=3, bbox_to_anchor=(1.0, 1.14))
    return c.save(fig, OUT / "fig1_5_effort_vs_capacity.png")


def diamond(ax, cx, cy, w, h, text, size=7.4):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True,
                         fc=c.TINT["yellow"], ec=c.SERIES[3], lw=0.9, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, color=c.INK, zorder=3, linespacing=1.25)


def fig_change_control():
    fig, ax = c.canvas(16, 8.2)
    steps = [(0.5, "1. Change request raised\n(any stakeholder)"), (20.5, "2. Logged in change log\n(ID, requester, reason)"),
             (40.5, "3. BA impact analysis\nwithin 3 working days")]
    boxes = [c.box(ax, x, 62, 18.5, 20, t, size=6.9) for x, t in steps]
    diamond(ax, 67.5, 72, 17, 30, "4. Minor?\n3 days or less,\nno policy or\ngate-date impact", size=6.4)
    po = c.box(ax, 80, 76, 16, 14, "Product owner\ndecides", fill=c.TINT["aqua"], edge=c.SERIES[2], size=7.0)
    ccb = c.box(ax, 80, 44, 16, 20, "Change control\nboard (fortnightly,\nor within 2 days\nif urgent)",
                fill=c.TINT["orange"], edge=c.SERIES[1], size=6.6)
    record = c.box(ax, 63, 8, 26, 20, "5. Decision recorded;\nbaseline, traceability\nand plan updated", size=6.9)
    tell = c.box(ax, 27, 8, 26, 20, "6. Stakeholders told within\n1 working day; shown in\nweekly status note", size=6.9)
    c.arrow(ax, c.anchor(boxes[0], "r"), c.anchor(boxes[1], "l"))
    c.arrow(ax, c.anchor(boxes[1], "r"), c.anchor(boxes[2], "l"))
    c.arrow(ax, c.anchor(boxes[2], "r"), (59, 72))
    c.path_arrow(ax, [(76, 72), (78, 72), (78, 83), (80, 83)], text="Yes", text_xy=(78, 77.5), size=6.8)
    c.path_arrow(ax, [(67.5, 57), (67.5, 54), (80, 54)], text="No", text_xy=(73.5, 54), size=6.8)
    c.path_arrow(ax, [(96, 83), (99, 83), (99, 18), (89, 18)])
    c.arrow(ax, c.anchor(ccb, "b", offset=-2), (86, 28))
    c.arrow(ax, c.anchor(record, "l"), c.anchor(tell, "r"))
    c.label(ax, 50, 98, "Every request is assessed for scope, effort, schedule, cost, risk, compliance and traced "
            "requirements", size=7.0, color=c.INK2, style="italic")
    return c.save(fig, OUT / "fig1_6_change_control.png")


def fig_comms_calendar():
    items = [cm for cm in d.COMMUNICATIONS if cm[7]]
    weeks = list(range(1, d.TOTAL_WEEKS + 1))
    colors, text, text_colors = [], [], []
    gate_weeks = {g[1]: g[0] for g in d.GATES}
    for cm in items:
        row_colors, row_text, row_tc = [], [], []
        for w in weeks:
            on = w in cm[7]
            row_colors.append(c.BLUE[450] if on else ("#f4f4f1" if w not in gate_weeks else "#ebebe6"))
            row_text.append("")
            row_tc.append("white")
        colors.append(row_colors)
        text.append(row_text)
        text_colors.append(row_tc)
    fig, ax = plt.subplots(figsize=(c.cm(16), c.cm(7.6)))
    c.heatmap(ax, [[0] * len(weeks) for _ in items], [f"{cm[0]} {cm[1]}" for cm in items],
              [str(w) for w in weeks], colors, text, text_colors, gap=1.2)
    for week, gate in gate_weeks.items():
        ax.text(week - 0.5, -0.55, gate, ha="center", va="center", fontsize=6.8, color=c.NAVY, weight="bold")
    ax.set_ylim(-1.0, len(items))
    ax.tick_params(axis="y", labelsize=7)
    ax.tick_params(axis="x", labelsize=6.6)
    ax.text(-0.3, -0.55, "Gates", ha="right", va="center", fontsize=6.8, color=c.NAVY, weight="bold")
    return c.save(fig, OUT / "fig1_7_communication_calendar.png")


def fig_package():
    fig, ax = c.canvas(16, 9.2)
    ax.plot([3, 97], [70, 70], color=c.AXIS, lw=1.2, zorder=0)
    xs = [9, 27.5, 46, 64.5, 83]
    for x, pack in zip(xs, d.PACKAGE):
        ax.scatter([x + 5.5], [70], s=60, color=c.NAVY, zorder=3)
        c.label(ax, x + 5.5, 78, pack[0], size=7.4, weight="bold", color=c.NAVY)
        c.box(ax, x - 1.5, 40, 14, 24, f"{pack[1]}\n\nApprover:\n{pack[5]}", wrap_at=17, size=6.5,
              fill=c.TINT["blue"], edge=c.BLUE[400])
    c.label(ax, 50, 92, "Business analysis package released at each gate", size=8.4, weight="bold")
    chevron_y, chevron_h = 8, 18
    width = 15.2
    for index, (name, _) in enumerate(d.PACKAGE_STEPS):
        x = 2 + index * (width + 1)
        ax.add_patch(Polygon([(x, chevron_y), (x + width - 2.2, chevron_y), (x + width, chevron_y + chevron_h / 2),
                              (x + width - 2.2, chevron_y + chevron_h), (x, chevron_y + chevron_h),
                              (x + 2.2, chevron_y + chevron_h / 2)], closed=True, fc=c.TINT["aqua"],
                             ec=c.SERIES[2], lw=0.8))
        c.label(ax, x + width / 2 + 0.6, chevron_y + chevron_h / 2, f"{index + 1}. {name}", size=6.6, wrap_at=14)
    c.label(ax, 50, 31, "How each package is prepared", size=7.6, weight="bold", color=c.INK2)
    return c.save(fig, OUT / "fig1_8_ba_package.png")


def fig_risk_heatmap():
    bands = {"Low": c.STATUS["good"], "Medium": c.STATUS["warning"], "High": c.STATUS["serious"],
             "Critical": c.STATUS["critical"]}
    fig, ax = plt.subplots(figsize=(c.cm(11.5), c.cm(9)))
    for likelihood in range(1, 6):
        for impact in range(1, 6):
            band = d.risk_band(likelihood * impact)
            ax.add_patch(Rectangle((likelihood - 0.5, impact - 0.5), 1, 1, fc=bands[band], alpha=0.30, ec="white",
                                   lw=2))
    cells = {}
    for risk in d.RISKS:
        cells.setdefault((risk[2], risk[3]), []).append(risk[0])
    for (likelihood, impact), ids in cells.items():
        ax.text(likelihood, impact, "\n".join(ids), ha="center", va="center", fontsize=7.4, color=c.INK,
                weight="bold", linespacing=1.2)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xticklabels(["1 Rare", "2 Unlikely", "3 Possible", "4 Likely", "5 Almost\ncertain"], fontsize=6.8)
    ax.set_yticklabels(["1 Minimal", "2 Minor", "3 Moderate", "4 Major", "5 Severe"], fontsize=6.8)
    ax.set_xlabel("Likelihood", fontsize=7.5)
    ax.set_ylabel("Impact", fontsize=7.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    handles = [Rectangle((0, 0), 1, 1, fc=color, alpha=0.30) for color in bands.values()]
    ax.legend(handles, [f"{name} ({rng})" for name, rng in zip(bands, ["1-4", "5-9", "10-14", "15-25"])],
              loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=4, fontsize=6.8, handlelength=1.0)
    return c.save(fig, OUT / "fig1_9_risk_heat_map.png")


ALL = [fig_public_growth, fig_context, fig_power_interest, fig_timeline, fig_capacity, fig_change_control,
       fig_comms_calendar, fig_package, fig_risk_heatmap]


def build_all():
    return [function() for function in ALL]


if __name__ == "__main__":
    for path in build_all():
        print(path.name)
