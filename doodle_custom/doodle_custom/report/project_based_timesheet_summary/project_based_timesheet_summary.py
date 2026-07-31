import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 250},
        {"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 250},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 180, "hidden": 1},
        {"label": _("Timesheet ID"), "fieldname": "name", "fieldtype": "Link", "options": "Timesheet", "width": 150},

        {"label": _("From Time"), "fieldname": "from_time", "fieldtype": "Datetime", "width": 150},
        {"label": _("To Time"), "fieldname": "to_time", "fieldtype": "Datetime", "width": 150},
        {"label": _("Hours"), "fieldname": "hours", "fieldtype": "Float", "width": 120},

        {"label": _("Project Hours"), "fieldname": "project_hours", "fieldtype": "Float", "width": 150},
        {"label": _("Total Used Project Hours"), "fieldname": "total_project_hours", "fieldtype": "Float", "width": 180},
        {"label": _("Remaining Project Hours"), "fieldname": "remaining_project_hours", "fieldtype": "Float", "width": 180},
    ]


def get_data(filters):
    main_conditions = ""
    total_conditions = ""
    values = {}

    # ---------------- Filters ----------------
    if filters.get("start_date"):
        main_conditions += " AND t.start_date >= %(start_date)s"
        values["start_date"] = filters.get("start_date")

    if filters.get("end_date"):
        main_conditions += " AND t.end_date <= %(end_date)s"
        values["end_date"] = filters.get("end_date")

    if filters.get("employee"):
        main_conditions += " AND t.employee = %(employee)s"
        values["employee"] = filters.get("employee")

    if filters.get("project"):
        main_conditions += " AND td.project = %(project)s"
        total_conditions += " AND td.project = %(project)s"
        values["project"] = filters.get("project")

    # ---------------- Project Status ----------------
    if filters.get("project_status"):
        statuses = filters.get("project_status")
        if isinstance(statuses, str):
            import json
            statuses = json.loads(statuses)

        if statuses:
            main_conditions += " AND p.status IN %(project_status)s"
            total_conditions += " AND p.status IN %(project_status)s"
            values["project_status"] = tuple(statuses)

    # ---------------- Department (FIXED) ----------------
    if filters.get("department"):
        main_conditions += " AND p.department = %(department)s"
        total_conditions += """
            AND td.project IN (
                SELECT name FROM `tabProject`
                WHERE department = %(department)s
            )
        """
        values["department"] = filters.get("department")

    # ---------------- MAIN QUERY ----------------
    data = frappe.db.sql(f"""
        SELECT 
            t.name,
            t.employee,
            t.employee_name,
            td.project,
            td.from_time,
            td.to_time,
            td.hours,
            p.department,
            COALESCE(p.custom_project_hours, 0) AS project_hours

        FROM `tabTimesheet` t
        LEFT JOIN `tabTimesheet Detail` td ON t.name = td.parent
        LEFT JOIN `tabProject` p ON p.name = td.project

        WHERE t.docstatus = 1
        {main_conditions}

        ORDER BY t.employee ASC, td.from_time ASC
    """, values, as_dict=True)

    # ---------------- TOTAL HOURS QUERY ----------------
    project_totals = frappe.db.sql(f"""
        SELECT 
            td.project,
            SUM(td.hours) as total_hours
        FROM `tabTimesheet Detail` td
        INNER JOIN `tabTimesheet` t ON t.name = td.parent
        LEFT JOIN `tabProject` p ON p.name = td.project
        WHERE t.docstatus = 1
        {total_conditions}
        GROUP BY td.project
    """, values, as_dict=True)

    project_map = {d.project: d.total_hours for d in project_totals}

    # ---------------- FINAL CALC ----------------
    for row in data:
        total = project_map.get(row.project, 0) or 0
        budget = row.project_hours or 0

        row["total_project_hours"] = round(total, 2)
        row["remaining_project_hours"] = round(budget - total, 2)

    return data