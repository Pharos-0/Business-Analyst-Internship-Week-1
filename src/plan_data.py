"""Structured content of the Week 1 Business Analysis Plan (Nykaa, Click, Collect & Return programme).

Every table and figure in the report, the CSV tables in outputs/tables and the Excel workbook are
generated from this module, so they always agree with each other.

Company facts come from data/nykaa_public_metrics.csv, which records the public filing, slide or
section behind each figure. Everything about the programme itself (scope, stakeholders' roles in it,
activities, effort, targets) is a proposal made for this internship case study. It is not a plan
published or endorsed by the company.
"""
import csv
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --------------------------------------------------------------------------- sources
SOURCES = {
    "S1": "FSN E-Commerce Ventures Limited (2026). Investor Presentation: quarter and full year ended "
          "March 31, 2026. Filed with NSE and BSE on 21 May 2026. https://www.nykaa.com/investor-relations/lp",
    "S2": "FSN E-Commerce Ventures Limited (2026). Business Responsibility and Sustainability Report "
          "FY2025-26 (part of the Integrated Report 2025-26). "
          "https://www.nykaa.com/media/wysiwyg/uiTools/2026-8/BRSR-FY2025-26.pdf",
    "S3": "Ministry of Consumer Affairs, Food and Public Distribution, Government of India (2020). "
          "Consumer Protection (E-Commerce) Rules, 2020.",
    "S4": "Government of India (2023). Digital Personal Data Protection Act, 2023; Ministry of Electronics "
          "and Information Technology (2025). Digital Personal Data Protection Rules, 2025 (notified "
          "November 2025).",
    "S5": "International Institute of Business Analysis (2015). A Guide to the Business Analysis Body of "
          "Knowledge (BABOK Guide), version 3. Toronto: IIBA.",
    "S6": "IIBA and Agile Alliance (2017). Agile Extension to the BABOK Guide, version 2. Toronto: IIBA.",
    "S7": "Mendelow, A. (1991). Stakeholder mapping. Proceedings of the 2nd International Conference on "
          "Information Systems, Cambridge, MA.",
    "S8": "Agile Business Consortium (2014). The DSDM Agile Project Framework (MoSCoW prioritisation).",
}


def load_metrics():
    with open(DATA / "nykaa_public_metrics.csv", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


METRICS = load_metrics()


def m(key):
    """Numeric value of a public metric."""
    return float(METRICS[key]["value"])


def cite(key):
    """Short citation for a public metric, e.g. 'S1, slide 38'."""
    row = METRICS[key]
    return f"{row['source']}, {row['location']}"


def growth(new_key, old_key):
    return (m(new_key) / m(old_key) - 1) * 100


# --------------------------------------------------------------------------- calendar
PROJECT_START = datetime.date(2027, 1, 4)  # assumed: a Monday after the festive and year-end sale peaks
TOTAL_WEEKS = 28
DPDP_CORE_DATE = datetime.date(2027, 5, 13)  # 18 months after the DPDP Rules were notified


def week_start(week):
    return PROJECT_START + datetime.timedelta(weeks=week - 1)


def week_of(date):
    return (date - PROJECT_START).days // 7 + 1


# --------------------------------------------------------------------------- programme
PROGRAMME = {
    "name": "Click, Collect & Return (CCR) programme",
    "short": "CCR",
    "pilot": "20 Nykaa stores in two metro cities",
    "vertical": "Beauty (Nykaa website and app)",
    "vision": "Customers can buy Beauty products online and collect them at a nearby Nykaa store, return "
              "eligible online orders at any participating store, and order any item from the full online "
              "range with the help of store staff.",
}

EVIDENCE = [
    ("Store network", f"{m('stores_fy26'):.0f} stores in {m('cities_fy26'):.0f} cities at 31 March 2026, up from "
     f"{m('stores_fy25'):.0f} a year earlier ({m('new_stores_fy26'):.0f} opened in FY26)", cite("stores_fy26"),
     "A larger store estate can act as pickup, return and stock points for online orders."),
    ("Online demand", f"{m('orders_beauty_fy26'):.1f} million Beauty orders in FY26 "
     f"(+{growth('orders_beauty_fy26', 'orders_beauty_fy25'):.0f}%) from {m('autc_beauty_fy26'):.1f} million annual "
     "unique transacting customers", cite("orders_beauty_fy26"),
     "Even a small share of orders moved to collection is a large volume, so store processes must scale."),
    ("Fulfilment cost", f"Fulfilment expense of ₹{m('fulfil_fy26'):,.0f} crore in FY26, "
     f"{m('fulfil_pct_fy26'):.1f}% of revenue from operations ({m('fulfil_pct_fy25'):.1f}% in FY25); it grew "
     f"{growth('fulfil_fy26', 'fulfil_fy25'):.0f}% against revenue growth of {growth('rev_fy26', 'rev_fy25'):.0f}%",
     cite("fulfil_fy26"),
     "Collected orders and store returns avoid a last-mile trip or a reverse pickup; the pilot must measure "
     "how much this saves."),
    ("Service quality", f"{m('complaints_fy26'):,.0f} consumer complaints received in FY26 against "
     f"{m('complaints_fy25'):,.0f} in FY25, all closed", cite("complaints_fy26"),
     "Complaints fell while orders grew. New journeys must not reverse this, so complaint handling is "
     "designed in from the start."),
    ("Stock network", f"{m('warehouses_fy26'):.0f} warehouses and {m('rapid_stores_fy26'):.0f} rapid stores among "
     f"{m('locations_fy26'):.0f} operating locations, alongside the retail stores", cite("warehouses_fy26"),
     "Stock sits in three kinds of location; online customers need one reliable view of store stock."),
    ("Regulation", "Main obligations of the DPDP Rules, 2025 apply from May 2027; e-commerce entities must "
     "acknowledge consumer complaints within 48 hours and resolve them within one month", "S3; S4",
     "Pickup codes, identity checks, notifications and refunds must comply from the first day of the pilot."),
]

OBJECTIVES = [
    ("O1", "Offer a convenient pickup option for online Beauty orders",
     "Click & collect share of eligible online Beauty orders from customers within 10 km of a pilot store",
     "Measured in discovery (A06)", "4% or more by pilot week 6"),
    ("O2", "Lower the cost of serving online orders",
     "Fulfilment cost per collected order compared with a home-delivered order in the same catchment",
     "Finance cost model (A06)", "At least 25% lower"),
    ("O3", "Make returns quicker and easier",
     "Share of eligible online Beauty returns in pilot catchments made in store; median time from store "
     "drop-off to refund initiation", "Current reverse-pickup data (A06)", "25% or more; 30 minutes or less"),
    ("O4", "Bring online customers into stores",
     "Share of collecting customers who buy at least one more item in store (attach rate)",
     "New measure", "15% or more"),
    ("O5", "Protect customer experience",
     "Satisfaction score for collect and return journeys; complaints per 10,000 CCR orders",
     "Current online CSAT and complaint rate (A06)", "4.3 out of 5 or more; no higher than the online rate"),
]

IN_SCOPE = [
    ("Store stock visibility", "Show store-level availability of Beauty products on the app and website for "
     "pilot stores."),
    ("Click & collect", "Prepaid online orders reserved from store stock and collected in store with a one-time "
     "pickup code; status notifications; unclaimed-order handling."),
    ("Return to store", "Return of eligible online Beauty orders at any pilot store, with refund initiation at "
     "the counter and stock re-entry or disposal."),
    ("Assisted ordering (endless aisle)", "Store staff order out-of-stock items for home delivery from the store "
     "app."),
    ("Store staff tools", "Changes to the store app and point of sale for handover, returns and assisted "
     "ordering."),
    ("Policies and rules", "Collection window, unclaimed orders, return eligibility, refunds, and revenue "
     "attribution between online and store results."),
    ("Measurement", "KPI definitions, pilot dashboard and benefits tracking."),
]

OUT_OF_SCOPE = [
    "Fashion vertical and Nykaa Fashion app (candidate for a later phase)",
    "Superstore by Nykaa (eB2B) and House of Nykaa brand websites",
    "Rapid delivery (Nykaa Now) network design",
    "Orders placed on third-party marketplaces",
    "Cash on delivery for click & collect orders during the pilot",
    "Replacement of the warehouse management, payment gateway or loyalty platforms",
    "International (GCC) operations and new store openings",
]

ASSUMPTIONS = [
    ("A1", "Assumption", "Store stock for each product is available from the point-of-sale and inventory "
     "systems at least every 15 minutes; its accuracy is confirmed in discovery."),
    ("A2", "Assumption", "Each pilot store can give space to a pickup shelf and a returns bin."),
    ("A3", "Assumption", "A product owner, two delivery squads and a QA lead are assigned for the full 28 weeks."),
    ("A4", "Assumption", "Return eligibility follows the current online policy for Beauty products (for example, "
     "unopened items only), to be confirmed with Legal and Category teams."),
    ("C1", "Constraint", "The pilot must avoid major sale events and the October-November festive peak."),
    ("C2", "Constraint", f"Core DPDP Rules obligations apply from {DPDP_CORE_DATE:%d %B %Y} (project week "
     f"{week_of(DPDP_CORE_DATE)}), before pilot launch."),
    ("C3", "Constraint", "The BA team is a lead business analyst, a business analyst and a part-time process "
     "analyst from Retail Operations (weeks 3-11)."),
    ("C4", "Constraint", "Store system changes can only be released in the monthly store-IT release window."),
    ("D1", "Dependency", "Inventory synchronisation interface from the point-of-sale system (Engineering)."),
    ("D2", "Dependency", "Order management system changes for store-reserved orders (Engineering)."),
    ("D3", "Dependency", "Logistics partner interface to cancel reverse pickups when items are returned in store."),
    ("D4", "Dependency", "Finance decision on how online and store results share CCR revenue."),
    ("D5", "Dependency", "Store operating procedures and training updated by Retail Operations."),
]

# --------------------------------------------------------------------------- approach
APPROACH_OPTIONS = [
    # criterion, predictive, adaptive, hybrid
    ("Requirements stability", "Suits stable, well-known needs", "Suits needs that emerge with feedback",
     "Rules and policies fixed early; screens refined in sprints"),
    ("Policy, legal and finance decisions", "Strong: decisions signed off before build",
     "Weak: decisions can drift sprint to sprint", "Decided and baselined at Gate 2"),
    ("Integration with order, store and logistics systems", "Strong: interfaces specified up front",
     "Risky without an agreed interface baseline", "Interfaces specified up front"),
    ("Early feedback from stores and customers", "Weak: feedback only at testing",
     "Strong: every sprint review", "Sprint reviews with store champions"),
    ("Documentation for audit and handover", "Strong", "Light", "Baselined package at each gate"),
    ("Fit with a 28-week, 20-store pilot", "Slow to react to pilot learning", "Hard to govern across many teams",
     "Selected approach"),
]

PHASES = [
    # id, name, start, end, colour slot
    ("P0", "Initiate and plan", 1, 2),
    ("P1", "Discover", 3, 6),
    ("P2", "Define requirements", 7, 11),
    ("P3", "Support build", 12, 19),
    ("P4", "Test and transition", 16, 21),
    ("P5", "Pilot and evaluate", 22, 28),
    ("P6", "Ongoing", 1, 28),
]

GATES = [
    ("G0", 2, "BA plan approved"),
    ("G1", 6, "Current state and options agreed"),
    ("G2", 11, "Requirements baseline approved"),
    ("G3", 21, "UAT signed off, pilot ready"),
    ("G4", 22, "Pilot launched"),
    ("G5", 28, "Scale-up decision"),
]

# --------------------------------------------------------------------------- stakeholders
# id, role, group, interest in CCR, power 1-10, interest 1-10, attitude, short label for the grid
STAKEHOLDERS = [
    ("SH01", "Executive sponsor (Business Head, Beauty)", "Leadership", "Business case, pilot results, brand partner relationships", 10, 8, "Supportive", "Sponsor"),
    ("SH02", "Product owner, omnichannel", "Technology", "Backlog value, scope and release dates", 8, 10, "Supportive", "Product owner"),
    ("SH03", "Head of Retail Operations", "Retail", "Store workload, space, store P&L credit", 9, 9, "Supportive, cautious", "Retail Ops head"),
    ("SH04", "Store managers (20 pilot stores)", "Retail", "Staff time, targets, handover process", 5, 9, "Mixed", "Store managers"),
    ("SH05", "Store beauty advisors (pilot stores)", "Retail", "Ease of use, training, incentives", 3, 8, "Neutral", "Beauty advisors"),
    ("SH06", "Head of Supply Chain and Fulfilment", "Operations", "Stock allocation, returns flow, replenishment", 8, 7, "Neutral", "Supply chain head"),
    ("SH07", "Warehouse and rapid store leads", "Operations", "Return consolidation, transfers to stores", 4, 6, "Neutral", "Warehouse leads"),
    ("SH08", "Head of Customer Care (grievance officer)", "Service", "Contact volumes, refund timelines, complaints", 5, 8, "Supportive", "Customer care head"),
    ("SH09", "Marketing and CRM lead", "Marketing", "Launch messages, app notifications, offers", 5, 6, "Supportive", "Marketing lead"),
    ("SH10", "Finance controller", "Finance", "Revenue attribution, refunds, tax on returns", 8, 5, "Sceptical", "Finance controller"),
    ("SH11", "Engineering leads (app, OMS, POS, inventory)", "Technology", "Feasibility, integration effort, release windows", 7, 8, "Neutral", "Engineering leads"),
    ("SH12", "Information security and data protection lead", "Risk", "DPDP compliance, identity checks, data minimisation", 7, 5, "Neutral", "Security & privacy"),
    ("SH13", "Legal and compliance", "Risk", "Consumer law, policy wording, complaint timelines", 7, 4, "Neutral", "Legal"),
    ("SH14", "QA and test lead", "Technology", "Testable requirements, UAT planning", 4, 7, "Supportive", "QA lead"),
    ("SH15", "Business intelligence team", "Technology", "KPI definitions and data feeds", 3, 6, "Supportive", "BI team"),
    ("SH16", "Brand partners (selected Beauty brands)", "External", "Brand presentation, selective distribution terms", 6, 4, "Neutral", "Brand partners"),
    ("SH17", "Logistics partners", "External", "Changes in reverse pickup volumes", 5, 3, "Neutral", "Logistics partners"),
    ("SH18", "Customers (online and store)", "External", "Convenience, speed of refunds, trust", 5, 7, "Not yet known", "Customers"),
    ("SH19", "Project manager", "Delivery", "Schedule, dependencies, budget", 7, 9, "Supportive", "Project manager"),
]

SPLIT = 5.5  # power and interest scores above this line count as "high"

QUADRANTS = [
    ("Manage closely", "high power, high interest",
     "Fortnightly steering committee; decisions taken at gates; early sight of every package; one-to-one "
     "check-ins with the lead BA."),
    ("Keep satisfied", "high power, lower interest",
     "Short, targeted reviews of the decisions they own (attribution, privacy, policy wording, brand terms); "
     "no routine meetings."),
    ("Keep informed and involved", "lower power, high interest",
     "Workshops, observation, sprint reviews and UAT; a store champion network; monthly store bulletin; "
     "customer research."),
    ("Monitor", "lower power, lower interest",
     "Briefings at Gates 1, 2 and 3; consulted on the interfaces that affect them."),
]


def quadrant_of(stakeholder):
    power, interest = stakeholder[4], stakeholder[5]
    if power > SPLIT:
        return "Manage closely" if interest > SPLIT else "Keep satisfied"
    return "Keep informed and involved" if interest > SPLIT else "Monitor"


def engagement():
    """Engagement approach per quadrant, with the stakeholders that fall in it (computed from the scores)."""
    rows = []
    for name, description, approach in QUADRANTS:
        members = [sh[0] for sh in STAKEHOLDERS if quadrant_of(sh) == name]
        rows.append((f"{name} ({description})", ", ".join(members), approach))
    return rows


RACI_ROLES = ["Lead BA", "BA", "Sponsor", "PO", "Retail", "Supply", "Eng.", "Privacy", "Legal", "Care",
              "Finance", "QA"]
RACI = [
    ("BA plan (this document)", "R", "C", "A", "C", "C", "I", "C", "I", "I", "I", "I", "I"),
    ("Stakeholder register and map", "A", "R", "I", "C", "C", "I", "I", "I", "I", "I", "I", "I"),
    ("Current-state process maps", "A", "R", "I", "C", "C", "C", "I", "I", "I", "C", "I", "I"),
    ("Business rules and policy decisions", "R", "C", "A", "C", "C", "C", "I", "C", "C", "C", "C", "I"),
    ("Business requirements document", "A", "R", "C", "C", "C", "C", "C", "C", "C", "C", "C", "I"),
    ("Product backlog and user stories", "C", "R", "I", "A", "C", "C", "C", "I", "I", "C", "I", "C"),
    ("Non-functional and privacy requirements", "A", "R", "I", "C", "I", "I", "C", "C", "C", "I", "I", "C"),
    ("Requirements traceability matrix", "A", "R", "I", "C", "I", "I", "C", "I", "I", "I", "I", "C"),
    ("UAT scenarios and sign-off", "R", "R", "I", "A", "C", "C", "C", "I", "I", "C", "I", "C"),
    ("Transition requirements", "A", "R", "I", "C", "C", "C", "C", "I", "I", "C", "C", "I"),
    ("Pilot evaluation report", "R", "C", "A", "C", "C", "C", "I", "I", "I", "C", "C", "I"),
]

# --------------------------------------------------------------------------- activities
# id, phase, activity, start week, end week, effort person-days, owner, techniques, outputs
ACTIVITIES = [
    ("A01", "P0", "Confirm business need, objectives and scope", 1, 2, 4, "Lead BA",
     "Document analysis; interviews; scope modelling", "Scope statement; context diagram"),
    ("A02", "P0", "Identify and analyse stakeholders", 1, 2, 3, "BA",
     "Stakeholder list, map and personas", "Stakeholder register; power-interest grid; RACI"),
    ("A03", "P0", "Plan BA approach, activities, governance and information", 1, 2, 5, "Lead BA",
     "Estimation; planning workshop", "BA plan v1.0"),
    ("A04", "P0", "Kick-off workshop and BA plan walkthrough", 2, 2, 1.5, "Lead BA",
     "Workshop", "Agreed ways of working; Gate 0 sign-off"),
    ("A05", "P1", "Map current order, store sale and return processes", 3, 6, 10, "Process analyst",
     "Observation in 4 stores and 1 warehouse; process modelling (BPMN)", "Current-state process maps; pain-point log"),
    ("A06", "P1", "Analyse order, return and stock data; set KPI baselines", 3, 6, 6, "BA",
     "Data analysis; metrics and KPIs", "Baseline KPI pack"),
    ("A07", "P1", "Customer research: survey and 12 interviews", 3, 6, 6, "BA",
     "Survey; interviews", "Customer needs and pain points"),
    ("A08", "P1", "Analyse systems and interfaces", 3, 6, 6, "Lead BA",
     "Interface analysis; data flow diagrams", "Interface inventory; data flows"),
    ("A09", "P1", "Review policies and compliance obligations", 3, 4, 3, "Lead BA",
     "Document analysis; interviews with Legal and Privacy", "Policy and compliance requirements"),
    ("A10", "P1", "Gap analysis and future-state options; Gate 1 package", 5, 6, 5, "Lead BA",
     "Gap analysis; decision analysis", "Options paper; current-state package"),
    ("A11", "P2", "Requirements workshops on four themes", 7, 9, 9, "Lead BA",
     "Workshops; prototyping (wireframes)", "Workshop outputs; agreed journeys"),
    ("A12", "P2", "Define business rules and policy decisions", 7, 10, 5, "Lead BA",
     "Business rules analysis; decision modelling", "Business rules catalogue; decision log"),
    ("A13", "P2", "Write business and solution requirements and user stories", 7, 11, 14, "BA",
     "User stories; acceptance criteria; use cases", "Business requirements document; product backlog"),
    ("A14", "P2", "Specify non-functional requirements", 8, 9, 3, "BA",
     "Non-functional requirements analysis", "Performance, security, privacy and accessibility requirements"),
    ("A15", "P2", "Define data, reporting and KPI requirements", 8, 10, 4, "Process analyst",
     "Data modelling; data dictionary", "KPI definitions; report specifications"),
    ("A16", "P2", "Prioritise requirements and plan releases", 10, 11, 3, "Lead BA",
     "MoSCoW; backlog management", "Prioritised backlog; release plan"),
    ("A17", "P2", "Review, validate and baseline requirements; Gate 2 package", 10, 11, 5, "Lead BA",
     "Reviews; walkthroughs; traceability", "Requirements baseline v1.0; traceability matrix"),
    ("A18", "P3", "Refine backlog and support four sprints", 12, 19, 26, "BA",
     "Backlog refinement; acceptance criteria", "Ready stories for each sprint"),
    ("A19", "P3", "Assess change requests (impact analysis)", 12, 25, 6, "Lead BA",
     "Impact analysis; traceability", "Change impact assessments"),
    ("A20", "P3", "Clarify requirements, review designs, join sprint reviews", 12, 19, 8, "Lead BA",
     "Reviews; demonstrations", "Design review notes; accepted stories"),
    ("A21", "P4", "Prepare UAT scenarios and test data with QA", 16, 18, 5, "BA",
     "Acceptance and evaluation criteria", "UAT scenarios traced to requirements"),
    ("A22", "P4", "Facilitate UAT with stores and customer care; triage defects", 20, 21, 8, "Lead BA",
     "Workshops; defect triage", "UAT results; sign-off"),
    ("A23", "P4", "Define transition requirements; Gate 3 package", 19, 21, 6, "BA",
     "Transition requirements; training needs analysis", "Readiness checklist; training needs"),
    ("A24", "P5", "Pilot hypercare: issue log and daily stand-ups", 22, 24, 8, "BA",
     "Issue tracking; root cause analysis", "Issue log; fix backlog"),
    ("A25", "P5", "Measure pilot KPIs against targets", 23, 28, 7, "BA",
     "Metrics and KPIs; survey", "Pilot KPI tracker"),
    ("A26", "P5", "Evaluate the solution and recommend scale-up; Gate 5 package", 27, 28, 5, "Lead BA",
     "Solution evaluation; lessons learned", "Pilot evaluation report"),
    ("A27", "P6", "Stakeholder communication and status reporting", 1, 28, 14, "Lead BA",
     "Status reporting", "Weekly status notes; steering committee packs"),
    ("A28", "P6", "Monitor BA performance and update this plan", 1, 28, 4, "Lead BA",
     "Metrics; retrospectives", "BA performance report; plan updates"),
]

ACTIVITY_SHORT = {  # labels for the timeline chart
    "A01": "Confirm need, objectives and scope", "A02": "Identify and analyse stakeholders",
    "A03": "Plan approach, governance, information", "A04": "Kick-off and plan walkthrough",
    "A05": "Map current processes", "A06": "Analyse data; set KPI baselines", "A07": "Customer research",
    "A08": "Analyse systems and interfaces", "A09": "Review policies and compliance",
    "A10": "Gap analysis and options; Gate 1", "A11": "Requirements workshops",
    "A12": "Business rules and policy decisions", "A13": "Write requirements and user stories",
    "A14": "Non-functional requirements", "A15": "Data, reporting and KPI requirements",
    "A16": "Prioritise and plan releases", "A17": "Validate and baseline; Gate 2",
    "A18": "Refine backlog; support sprints", "A19": "Change impact analysis",
    "A20": "Clarify requirements; design reviews", "A21": "Prepare UAT scenarios",
    "A22": "Facilitate UAT; triage defects", "A23": "Transition requirements; Gate 3", "A24": "Pilot hypercare",
    "A25": "Measure pilot KPIs", "A26": "Evaluate and recommend; Gate 5",
    "A27": "Communication and status reporting", "A28": "Monitor BA performance",
}

CONTINGENCY = 0.15
AVAILABILITY = 0.85  # share of each person's time available for planned BA work
TEAM = [
    # role, FTE, first week, last week
    ("Lead BA", 1.0, 1, 28),
    ("BA", 1.0, 1, 21),
    ("BA", 0.5, 22, 28),  # half released to Fashion phase-2 discovery once the pilot starts
    ("Process analyst", 0.5, 3, 11),
]
DAY_RATE = {"Lead BA": 22000, "BA": 15000, "Process analyst": 12000}  # assumed fully loaded cost, Rs per day


def total_effort():
    return sum(a[5] for a in ACTIVITIES)


def effort_by_phase():
    result = {p[0]: 0 for p in PHASES}
    for a in ACTIVITIES:
        result[a[1]] += a[5]
    return result


def effort_by_owner():
    result = {}
    for a in ACTIVITIES:
        result[a[6]] = result.get(a[6], 0) + a[5]
    return result


def weekly_demand():
    """Planned effort per week, spreading each activity evenly over its weeks; by phase."""
    demand = {p[0]: [0.0] * TOTAL_WEEKS for p in PHASES}
    for a in ACTIVITIES:
        weeks = a[4] - a[3] + 1
        for week in range(a[3], a[4] + 1):
            demand[a[1]][week - 1] += a[5] / weeks
    return demand


def weekly_capacity():
    capacity = [0.0] * TOTAL_WEEKS
    for role, fte, first, last in TEAM:
        for week in range(first, last + 1):
            capacity[week - 1] += fte * 5 * AVAILABILITY
    return capacity


def total_capacity():
    return sum(weekly_capacity())


def ba_cost():
    """Cost of planned effort plus contingency, at the assumed day rates."""
    by_owner = effort_by_owner()
    planned = sum(DAY_RATE[o] * d for o, d in by_owner.items())
    return planned, planned * (1 + CONTINGENCY)


# Stakeholder time requested over the 28 weeks (hours for the most involved person) - checked against availability.
TIME_REQUESTS = [
    ("Executive sponsor", "Kick-off 2 h; 14 steering meetings x 1 h; 5 gate reviews x 1.5 h", 23.5, "About 1 h a week"),
    ("Product owner", "Daily collaboration with the BA team, about 4 h a week", 112, "Assigned to CCR"),
    ("Head of Retail Operations", "14 steering meetings x 1 h; 4 workshops x 3 h; 5 gate reviews x 1.5 h", 33.5, "About 1.2 h a week"),
    ("Store manager (each of 20)", "Briefing 1 h; workshop 3 h (6 managers); UAT 4 h (6 managers); training 2 h", 10, "Outside peak trading hours"),
    ("Beauty advisor (each, pilot stores)", "Observation 2 h (8 advisors); UAT 4 h (8 advisors); training 2 h", 8, "Planned with store rosters"),
    ("Head of Supply Chain", "14 steering meetings x 1 h; 2 workshops x 3 h; 2 reviews x 2 h", 24, "About 0.9 h a week"),
    ("Engineering leads (each of 4)", "Interface sessions 6 h; design reviews 8 h; refinement 16 h", 30, "Inside sprint ceremonies"),
    ("Security and privacy lead", "Workshop 3 h; 2 reviews x 2 h; 2 gate reviews x 1.5 h", 10, "Booked in advance"),
    ("Legal and compliance", "Policy workshop 3 h; 2 reviews x 2 h", 7, "Booked in advance"),
    ("Head of Customer Care", "Workshop 3 h; UAT 6 h; 2 reviews x 2 h", 13, "About 0.5 h a week"),
    ("Finance controller", "Attribution workshop 3 h; 2 reviews x 2 h; 3 gate reviews x 1.5 h", 11.5, "Booked in advance"),
]

# --------------------------------------------------------------------------- governance
DECISIONS = [
    ("Priority of requirements within the agreed scope", "Product owner", "Lead BA, Engineering leads, Retail Ops",
     "Steering committee"),
    ("Change to scope, budget or a gate date", "Steering committee (change control board)",
     "Lead BA impact analysis, project manager", "Executive sponsor"),
    ("Store process and staffing rules", "Head of Retail Operations", "Store managers, Lead BA",
     "Steering committee"),
    ("Return, refund and collection policies", "Head of Customer Care with Legal", "Category teams, Finance",
     "Executive sponsor"),
    ("Use of customer personal data", "Security and data protection lead", "Legal, Product owner",
     "Executive sponsor"),
    ("Revenue attribution between online and stores", "Finance controller", "Retail Ops, Sponsor",
     "Executive sponsor"),
    ("Technical design trade-offs", "Engineering leads", "Product owner, Lead BA", "Steering committee"),
    ("Changes to this BA plan", "Lead BA", "Project manager, Product owner (sponsor informed)",
     "Steering committee"),
]

CHANGE_STEPS = [
    "Anyone can raise a change request; the BA logs it with an ID, requester, date and reason.",
    "Within three working days the BA assesses impact on scope, effort, schedule, cost, risk, compliance and traced requirements.",
    "Minor changes (three person-days or less, no policy or gate-date impact) go to the product owner.",
    "Other changes go to the change control board, which meets fortnightly with the steering committee or "
    "within two working days if urgent.",
    "The decision and its reason are recorded; the requirements baseline, traceability matrix and plan are "
    "updated and versioned.",
    "Affected stakeholders are told within one working day; the change appears in the weekly status note.",
]

APPROVAL_LEVELS = [
    ("Working drafts (0.x)", "Peer review by the other BA", "No sign-off"),
    ("Gate packages (1.0)", "Review by the owners named in the RACI, then a gate review meeting",
     "Accountable owner and sponsor"),
    ("Minor revisions (1.x)", "Product owner review", "Product owner"),
    ("Major revisions (2.0)", "Full gate-style review", "Change control board"),
]

# --------------------------------------------------------------------------- communication
# id, communication, audience, purpose / content, format and channel, timing, owner, weeks (for the calendar)
COMMUNICATIONS = [
    ("CM01", "Kick-off and BA plan walkthrough", "All core stakeholders", "Objectives, scope, roles, plan, ways of working",
     "Workshop with slides; recording on the project wiki", "Week 2", "Lead BA", [2]),
    ("CM02", "Weekly BA status note", "Core team, sponsor", "Progress against plan, decisions, risks, changes, next steps",
     "One-page note on the wiki, link posted in the team channel", "Every Friday", "Lead BA", list(range(1, 29))),
    ("CM03", "Steering committee pack", "Sponsor and steering committee", "Status, decisions needed, risks, change requests",
     "Slides plus decision log", "Fortnightly", "Lead BA with PM", list(range(2, 29, 2))),
    ("CM04", "Gate review", "Accountable owners per RACI", "Approve the gate package or record conditions",
     "Meeting with package circulated 3 working days before", "Weeks 2, 6, 11, 21, 28", "Lead BA",
     [2, 6, 11, 21, 28]),
    ("CM05", "Requirements review sessions", "Subject matter experts per theme", "Walk through requirements and rules; collect corrections",
     "Workshop or walkthrough with review comments in the wiki", "Weekly in weeks 8-11", "BA", [8, 9, 10, 11]),
    ("CM06", "Sprint review demonstrations", "Product owner, store champions, Customer Care", "Show working features; confirm acceptance",
     "Live demo, recorded", "End of each sprint", "Product owner with BA", [13, 15, 17, 19]),
    ("CM07", "Store network bulletin", "Store managers and advisors in pilot stores", "What is changing, when, training, how to give feedback",
     "Short bulletin on the store app and team channel", "Monthly", "BA with Retail Ops", [4, 8, 12, 16, 20, 24, 28]),
    ("CM08", "Partner briefings", "Brand and logistics partners", "Changes that affect them; interface and process needs",
     "Email briefing and call", "Weeks 6, 11, 21", "Lead BA with partner managers", [6, 11, 21]),
    ("CM09", "Customer research", "Panel of online and store customers", "Needs and pain points; pilot satisfaction",
     "Online survey and interviews", "Weeks 4-5 and 25", "BA", [4, 5, 25]),
    ("CM10", "Pilot readiness and training briefings", "Pilot store teams, Customer Care", "Process, scripts, escalation contacts",
     "Training sessions and quick-reference guide", "Weeks 20-21", "BA with Retail Ops", [20, 21]),
    ("CM11", "Hypercare stand-ups", "Pilot stores, Engineering, Customer Care", "Issues, fixes, decisions during launch",
     "15-minute video call", "Daily in weeks 22-24", "BA", [22, 23, 24]),
    ("CM12", "Escalation notice", "Sponsor and decision owner", "Issue, impact, options and a recommendation",
     "Email and call", "Within 24 hours of an issue", "Lead BA", []),
]

ESCALATION = [
    ("Level 1", "Lead BA and the stakeholder concerned", "2 working days"),
    ("Level 2", "Project manager and product owner", "2 further working days"),
    ("Level 3", "Steering committee or executive sponsor", "Next steering meeting or 3 working days if urgent"),
]

# --------------------------------------------------------------------------- information management
INFORMATION = [
    ("BA plan, packages, decision log", "Project wiki space 'CCR - Business Analysis'", "Lead BA",
     "0.x drafts, 1.0 at gate, 1.x minor"),
    ("Requirements and user stories", "Backlog tool (one item per requirement, linked to epics)", "BA",
     "Item history; baseline label at Gate 2"),
    ("Process models", "Modelling tool, exported to the wiki", "Process analyst", "Version in file name"),
    ("Traceability matrix", "Backlog tool links, exported to the wiki at each gate", "BA", "Snapshot per gate"),
    ("Workshop and interview notes", "Wiki, one page per session", "BA", "Final within 2 working days"),
    ("Change requests", "Change log in the backlog tool", "Lead BA", "Status workflow"),
    ("Customer research data", "Research repository with restricted access", "BA",
     "Anonymised; raw data deleted after 90 days"),
]

NAMING = [
    ("Business requirement", "CCR-BR-nnn", "CCR-BR-004 Customers can collect prepaid orders in store"),
    ("Functional requirement / user story", "CCR-FR-nnn", "CCR-FR-031 Show store availability on product page"),
    ("Non-functional requirement", "CCR-NFR-nnn", "CCR-NFR-007 Pickup code check under 2 seconds"),
    ("Business rule", "CCR-RULE-nn", "CCR-RULE-03 Orders are held for 5 days"),
    ("Transition requirement", "CCR-TR-nn", "CCR-TR-02 Train advisors before launch"),
    ("Change request", "CCR-CR-nnn", "CCR-CR-012 Add exchanges to store returns"),
    ("Document", "CCR_<type>_v<major.minor>", "CCR_BRD_v1.0"),
]

ATTRIBUTES = ["ID", "Title and statement", "Type", "Source (stakeholder or document)", "Owner", "Objective (O1-O5)",
              "Priority (MoSCoW)", "Status", "Version", "Acceptance criteria", "Dependencies", "Risk", "Rationale"]

# --------------------------------------------------------------------------- business analysis package
PACKAGE = [
    ("Gate 0 (week 2)", "Plan and scope", "BA plan; scope statement; context diagram; stakeholder register; RACI",
     "Sponsor, steering committee", "Slide summary plus wiki pages", "Executive sponsor"),
    ("Gate 1 (week 6)", "Current state and options", "Process maps; pain points; baseline KPIs; interface inventory; "
     "compliance obligations; options paper", "Steering committee, process owners", "Wiki pages; options paper",
     "Executive sponsor"),
    ("Gate 2 (week 11)", "Requirements baseline", "Business requirements document; prioritised backlog; business rules; "
     "non-functional and privacy requirements; KPI definitions; traceability matrix", "Product owner, Engineering, "
     "Retail Ops, Legal, Privacy, Finance", "Requirements document (PDF export) plus backlog baseline",
     "Product owner and sponsor"),
    ("Gate 3 (week 21)", "Transition and readiness", "UAT results; open defects; transition requirements; training "
     "materials; readiness checklist", "Steering committee, Retail Ops, Customer Care", "Readiness pack",
     "Head of Retail Operations and product owner"),
    ("Gate 5 (week 28)", "Pilot evaluation", "KPI results against O1-O5; customer feedback; issues and fixes; "
     "lessons learned; scale-up recommendation", "Sponsor, steering committee", "Evaluation report",
     "Executive sponsor"),
]

PACKAGE_STEPS = [
    ("Assemble", "Collect the approved work products for the gate and check every item against the gate checklist."),
    ("Quality check", "Peer review: complete, consistent, traced to objectives, testable, nothing left unfinished."),
    ("Tailor", "Add a one-page summary for leaders; keep the detail for owners; use plain language."),
    ("Circulate", "Share three working days before the gate review, with the questions reviewers must answer."),
    ("Review and sign off", "Record approvals, conditions and dissent in the decision log."),
    ("Baseline and publish", "Freeze version 1.0, label the backlog baseline and announce it in the status note."),
]

# --------------------------------------------------------------------------- risks
# id, risk, likelihood 1-5, impact 1-5, response, owner
RISKS = [
    ("R01", "Store managers and advisors cannot attend workshops and UAT during busy trading periods", 4, 3,
     "Book sessions outside peak hours; use store champions; record short demos", "Lead BA"),
    ("R02", "Store stock data is less accurate than needed for click & collect", 3, 5,
     "Measure accuracy in discovery (A06); add a stock-check step before confirming orders", "Supply chain head"),
    ("R03", "Integration across app, order management, point of sale and logistics takes longer than planned", 3, 4,
     "Specify interfaces by Gate 2; agree release windows early; spike risky interfaces first", "Engineering leads"),
    ("R04", "Privacy requirements found late delay the pilot", 2, 5,
     "Privacy lead in requirements workshops; privacy checklist at Gates 2 and 3", "Privacy lead"),
    ("R05", "Online and store teams disagree on revenue attribution", 4, 3,
     "Finance-led workshop in week 8; options paper; decision at Gate 2", "Finance controller"),
    ("R06", "Scope grows (for example, Fashion or exchanges) before the pilot", 3, 3,
     "Out-of-scope list; change control; park ideas in the phase 2 backlog", "Product owner"),
    ("R07", "Key subject matter expert leaves or moves", 2, 3,
     "Record decisions and models on the wiki; name a deputy for each theme", "Project manager"),
    ("R08", "Some brands' selective distribution terms limit store collection of their products", 2, 3,
     "Check brand terms in discovery; exclude products by rule if needed", "Sponsor"),
    ("R09", "Logistics partner interface cannot cancel reverse pickups automatically", 3, 2,
     "Manual cancellation fallback for the pilot", "Supply chain head"),
    ("R10", "Customers do not notice or trust the new options", 3, 4,
     "Clear app messages, store signage and launch offers; measure in pilot surveys", "Marketing lead"),
]


def risk_score(risk):
    return risk[2] * risk[3]


def risk_band(score):
    if score >= 15:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


# --------------------------------------------------------------------------- BA performance
BA_METRICS = [
    ("Gate packages approved at the first review", "80% or more", "Decision log", "Each gate"),
    ("Requirements with acceptance criteria and a traced objective before baseline", "100%", "Backlog report", "Gate 2"),
    ("UAT defects caused by missing or wrong requirements", "10% of defects or fewer", "Defect log root cause", "UAT"),
    ("Change impact assessments completed within 3 working days", "90% or more", "Change log", "Monthly"),
    ("Stakeholder satisfaction with BA work (pulse survey, 1-5)", "4.0 or more", "Survey after each gate", "Each gate"),
    ("BA effort compared with plan", "Within 10%", "Timesheets against the activity plan", "Fortnightly"),
    ("Requirements changed after baseline (volatility)", "15% or fewer", "Backlog history", "Monthly"),
]

GLOSSARY = [
    ("AOV", "Average order value: GMV divided by the number of orders."),
    ("AUTC", "Annual unique transacting customers: customers who placed at least one order in the last 12 months."),
    ("BA", "Business analyst or business analysis."),
    ("BABOK", "A Guide to the Business Analysis Body of Knowledge, published by IIBA."),
    ("BPMN", "Business Process Model and Notation, a standard notation for process maps."),
    ("CCR", "Click, Collect & Return, the programme proposed in this plan."),
    ("Click & collect", "Ordering online and collecting the order in a store."),
    ("CSAT", "Customer satisfaction score."),
    ("DPDP", "Digital Personal Data Protection Act, 2023 and the related Rules, 2025."),
    ("Endless aisle", "Store staff ordering items from the full online range for a customer in the store."),
    ("Gate", "A planned review point where a package is approved before the next phase."),
    ("GMV", "Gross merchandise value: value of orders before returns, cancellations and discounts."),
    ("MoSCoW", "Prioritisation into Must have, Should have, Could have and Won't have this time."),
    ("OMS", "Order management system."),
    ("POS", "Point of sale (store till) system."),
    ("RACI", "Responsible, Accountable, Consulted, Informed."),
    ("SteerCo", "Steering committee for the programme."),
    ("UAT", "User acceptance testing."),
]
