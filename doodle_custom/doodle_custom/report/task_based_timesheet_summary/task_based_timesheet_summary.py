import frappe


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


# ---------------- COLUMNS ----------------
def get_columns():
    return [
        {"label": "Task", "fieldname": "task", "fieldtype": "Link", "options": "Task", "width": 160},
        {"label": "Subject", "fieldname": "subject", "fieldtype": "Data", "width": 280},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 200},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 180},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200, "hidden": 1},
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 150, "hidden": 1},

        {"label": "Expected Hours", "fieldname": "expected_hours", "fieldtype": "Float"},
        {"label": "Actual Hours", "fieldname": "actual_hours", "fieldtype": "Float"},
        {"label": "Remaining Hours", "fieldname": "remaining_hours", "fieldtype": "Float"},
    ]


# ---------------- DATA ----------------
def get_data(filters):
    conditions = ""
    values = {}

    # Task
    if filters.get("task"):
        conditions += " AND t.name = %(task)s"
        values["task"] = filters["task"]

    # Project
    if filters.get("project"):
        conditions += " AND t.project = %(project)s"
        values["project"] = filters["project"]

    # Employee
    if filters.get("employee"):
        conditions += " AND t.custom_task_assign_to = %(employee)s"
        values["employee"] = filters["employee"]

    # Department
    if filters.get("department"):
        conditions += " AND t.department = %(department)s"
        values["department"] = filters["department"]

    # Project Status (MULTISELECT FIXED)
    if filters.get("project_status"):
        statuses = filters.get("project_status")  # ✅ NO JSON LOAD
        if statuses:
            conditions += " AND t.status IN %(statuses)s"
            values["statuses"] = statuses

    # Dates
    if filters.get("start_date"):
        conditions += " AND t.creation >= %(start_date)s"
        values["start_date"] = filters["start_date"]

    if filters.get("end_date"):
        conditions += " AND t.creation <= %(end_date)s"
        values["end_date"] = filters["end_date"]
    if filters.get("task_status"):
        statuses = filters.get("task_status")

        if statuses:
            conditions += " AND t.status IN %(task_status)s"
            values["task_status"] = statuses
    data = frappe.db.sql(f"""
        SELECT
            t.name AS task,
            t.project,
            t.subject,
            t.department,
            t.custom_task_assign_to AS employee,
            e.employee_name,
            e.department,

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

        WHERE t.docstatus < 2
        AND t.status NOT IN ('Completed', 'Cancelled')
        {conditions}

        ORDER BY t.name
    """, values, as_dict=True)

    for row in data:
        row["remaining_hours"] = round(
            (row["expected_hours"] or 0) - (row["actual_hours"] or 0),
            2
        )

    return data