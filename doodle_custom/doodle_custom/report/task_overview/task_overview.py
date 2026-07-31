import frappe
from urllib.parse import urlencode


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


# ---------------- COLUMNS ----------------
def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 220},
        {
            "label": "Employee",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 200,
            "hidden": 1
        },
        {"label": "Expected Hours", "fieldname": "expected_hours", "fieldtype": "Float", "width": 100},
        {"label": "Actual Hours", "fieldname": "actual_hours", "fieldtype": "Float", "width": 100},
        {"label": "Remaining Hours", "fieldname": "remaining_hours", "fieldtype": "Float", "width": 100},

        {"label": "Working Tasks", "fieldname": "working", "fieldtype": "Int" ,"width": 100},
        {"label": "Open Tasks", "fieldname": "open", "fieldtype": "Int" ,"width": 100},
        {"label": "Pending Review", "fieldname": "pending_review", "fieldtype": "Int" ,"width": 100},
        {"label": "On Hold", "fieldname": "on_hold", "fieldtype": "Int" ,"width": 100},
        {"label": "Overdue", "fieldname": "overdue", "fieldtype": "Int" ,"width": 100},
        {"label": "To Be Done", "fieldname": "to_be_done", "fieldtype": "Int" ,"width": 100},

        {"label": "Task Report", "fieldname": "report_link", "fieldtype": "Data", "width": 250},
    ]


# ---------------- DATA ----------------
def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("start_date"):
        conditions += " AND t.creation >= %(start_date)s"
        values["start_date"] = filters["start_date"]
    if filters.get("project"):
        conditions += " AND t.project = %(project)s"
        values["project"] = filters["project"]
    if filters.get("end_date"):
        conditions += " AND t.creation <= %(end_date)s"
        values["end_date"] = filters["end_date"]
    if filters.get("employee"):
        conditions += " AND t.custom_task_assign_to = %(employee)s"
        values["employee"] = filters["employee"]

    if filters.get("department"):
        conditions += " AND t.department = %(department)s"
        values["department"] = filters["department"]

    if filters.get("project_status"):
        statuses = tuple(filters.get("project_status"))

        # handle single value case
        if len(statuses) == 1:
            conditions += " AND p.status = %(project_status)s"
            values["project_status"] = statuses[0]
        else:
            conditions += " AND p.status IN %(project_status)s"
            values["project_status"] = statuses
    conditions += " AND t.status NOT IN ('Completed', 'Cancelled')"

    rows = frappe.db.sql(f"""
        SELECT
            t.custom_task_assign_to AS employee,
            e.employee_name,
            t.department,
            t.status,
            t.project,
            p.status AS project_status,
            COALESCE(t.expected_time, 0) AS expected_hours,

            COALESCE((
                SELECT SUM(td.hours)
                FROM `tabTimesheet Detail` td
                INNER JOIN `tabTimesheet` ts
                    ON ts.name = td.parent
                WHERE td.task = t.name
                AND ts.docstatus = 1
            ), 0) AS actual_hours

        FROM `tabTask` t
        LEFT JOIN `tabEmployee` e
            ON e.name = t.custom_task_assign_to
        LEFT JOIN `tabProject` p
            ON p.name = t.project

        WHERE t.docstatus < 2
        {conditions}
    """, values, as_dict=True)

    emp_map = {}

    for r in rows:
        if not r.employee:
            continue

        emp = r.employee

        if emp not in emp_map:
            emp_map[emp] = {
                "employee": emp,
                "expected_hours": 0,
                "actual_hours": 0,
                "employee_name": r.employee_name , 
                "working": 0,
                "open": 0,
                "pending_review": 0,
                "on_hold": 0,
                "overdue": 0,
                "to_be_done": 0,
            }

        emp_map[emp]["expected_hours"] += r.expected_hours or 0
        emp_map[emp]["actual_hours"] += r.actual_hours or 0

        status = (r.status or "").strip()

        if status == "Working":
            emp_map[emp]["working"] += 1
        elif status == "Open":
            emp_map[emp]["open"] += 1
        elif status == "Pending Review":
            emp_map[emp]["pending_review"] += 1
        elif status == "On Hold":
            emp_map[emp]["on_hold"] += 1
        elif status == "Overdue":
            emp_map[emp]["overdue"] += 1
        elif status in ("To Do", "To be Done", "Template"):
            emp_map[emp]["to_be_done"] += 1

    result = []

    base_url = "https://v15doodle.doodletech.ae/app/query-report/Task%20Based%20Timesheet%20Summary"

    for emp, d in emp_map.items():
        d["remaining_hours"] = round(
            (d["expected_hours"] or 0) - (d["actual_hours"] or 0),
            2
        )

        # clickable report link
        params = {"employee": emp, "department": filters.get("department") or ""}
        link = base_url + "?" + urlencode(params)

        d["report_link"] = f'<a href="{link}" target="_blank">View Report</a>'

        result.append(d)

    return result