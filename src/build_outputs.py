"""Build every Week 1 output from plan_data.py: figures, CSV tables and the Excel workbook.

Run from the repository root:  python src/build_outputs.py
"""
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill

import figures
import plan_data as d

ROOT = Path(__file__).resolve().parent.parent
TABLES = ROOT / "outputs" / "tables"
WORKBOOK = ROOT / "outputs" / "Week_1_BA_Plan_Workbook.xlsx"


def tables():
    week_dates = {w: d.week_start(w) for w in range(1, d.TOTAL_WEEKS + 1)}
    demand = d.weekly_demand()
    capacity = d.weekly_capacity()
    return {
        "evidence_from_public_data": pd.DataFrame(
            d.EVIDENCE, columns=["Topic", "Public evidence", "Source", "Implication for the programme"]),
        "objectives": pd.DataFrame(d.OBJECTIVES, columns=["ID", "Objective", "Measure", "Baseline", "Target"]),
        "scope": pd.DataFrame([("In scope", a, b) for a, b in d.IN_SCOPE] +
                              [("Out of scope", item, "") for item in d.OUT_OF_SCOPE],
                              columns=["Scope", "Item", "Description"]),
        "assumptions_constraints_dependencies": pd.DataFrame(d.ASSUMPTIONS, columns=["ID", "Type", "Statement"]),
        "stakeholder_register": pd.DataFrame(
            [(s[0], s[1], s[2], s[3], s[4], s[5], s[6], d.quadrant_of(s)) for s in d.STAKEHOLDERS],
            columns=["ID", "Stakeholder", "Group", "Interest in CCR", "Power (1-10)", "Interest (1-10)",
                     "Attitude", "Engagement quadrant"]),
        "engagement_approach": pd.DataFrame(d.engagement(), columns=["Quadrant", "Stakeholders", "Approach"]),
        "raci_matrix": pd.DataFrame(d.RACI, columns=["Deliverable"] + d.RACI_ROLES),
        "ba_activities": pd.DataFrame(
            [(a[0], a[1], a[2], a[3], a[4], week_dates[a[3]].isoformat(), week_dates[a[4]].isoformat(), a[5], a[6],
              a[7], a[8]) for a in d.ACTIVITIES],
            columns=["ID", "Phase", "Activity", "Start week", "End week", "Start date (Monday)",
                     "End week starts (Monday)", "Effort (person-days)", "Owner", "Techniques", "Outputs"]),
        "effort_and_capacity_by_week": pd.DataFrame(
            [(w + 1, week_dates[w + 1].isoformat(), round(sum(demand[p][w] for p in demand), 2), round(capacity[w], 2),
              round(sum(demand[p][w] for p in demand) / capacity[w] * 100, 1)) for w in range(d.TOTAL_WEEKS)],
            columns=["Week", "Week starts", "Planned effort (person-days)", "Capacity (person-days)",
                     "Utilisation (%)"]),
        "stakeholder_time_requests": pd.DataFrame(
            d.TIME_REQUESTS, columns=["Stakeholder", "What we ask for", "Hours per person (28 weeks)", "Availability"]),
        "decision_rights": pd.DataFrame(d.DECISIONS, columns=["Decision", "Decides", "Consulted", "Escalation"]),
        "approval_levels": pd.DataFrame(d.APPROVAL_LEVELS, columns=["Document status", "Review", "Approval"]),
        "communication_plan": pd.DataFrame(
            [cm[:7] + (", ".join(str(w) for w in cm[7]) if cm[7] else "As needed",) for cm in d.COMMUNICATIONS],
            columns=["ID", "Communication", "Audience", "Purpose and content", "Format and channel", "Timing",
                     "Owner", "Weeks"]),
        "escalation_path": pd.DataFrame(d.ESCALATION, columns=["Level", "Who", "Time to resolve before escalating"]),
        "information_management": pd.DataFrame(d.INFORMATION, columns=["Information", "Where it is kept", "Owner",
                                                                       "Version control"]),
        "naming_conventions": pd.DataFrame(d.NAMING, columns=["Item", "Format", "Example"]),
        "ba_package": pd.DataFrame(d.PACKAGE, columns=["Gate", "Package", "Contents", "Audience", "Format",
                                                       "Approver"]),
        "risk_register": pd.DataFrame(
            [(r[0], r[1], r[2], r[3], d.risk_score(r), d.risk_band(d.risk_score(r)), r[4], r[5]) for r in d.RISKS],
            columns=["ID", "Risk", "Likelihood (1-5)", "Impact (1-5)", "Score", "Rating", "Response", "Owner"]),
        "ba_performance_metrics": pd.DataFrame(d.BA_METRICS, columns=["Measure", "Target", "Source", "When"]),
        "public_sources": pd.DataFrame(sorted(d.SOURCES.items()), columns=["ID", "Source"]),
    }


def write_workbook(frames):
    header_fill = PatternFill("solid", fgColor="1F3A5F")
    with pd.ExcelWriter(WORKBOOK, engine="openpyxl") as writer:
        for name, frame in frames.items():
            sheet = name.replace("_", " ").title()
            for word, fixed in (("Ba ", "BA "), ("Raci", "RACI"), ("Kpi", "KPI")):
                sheet = sheet.replace(word, fixed)
            sheet = sheet[:31]
            frame.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]
            ws.freeze_panes = "A2"
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = header_fill
                cell.alignment = Alignment(vertical="center", wrap_text=True)
            for column in ws.columns:
                longest = max(len(str(cell.value or "")) for cell in column)
                ws.column_dimensions[column[0].column_letter].width = min(max(10, longest * 0.9), 60)
                for cell in column[1:]:
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
    wb = writer.book
    wb.properties.creator = "Pharos-0"
    wb.properties.lastModifiedBy = "Pharos-0"
    wb.properties.title = "Week 1 Business Analysis Plan workbook"
    wb.save(WORKBOOK)


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    figure_paths = figures.build_all()
    frames = tables()
    for name, frame in frames.items():
        frame.to_csv(TABLES / f"{name}.csv", index=False)
    write_workbook(frames)
    print(f"{len(figure_paths)} figures, {len(frames)} tables, workbook: {WORKBOOK.name}")


if __name__ == "__main__":
    main()
