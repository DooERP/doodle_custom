import frappe
from urllib.parse import urlencode


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 350},
        {"label": "Project Hours", "fieldname": "project_hours", "fieldtype": "Float", "width": 200},
        {"label": "Used Hours", "fieldname": "used_hours", "fieldtype": "Float", "width": 200},
        {"label": "Remaining Hours", "fieldname": "remaining_hours", "fieldtype": "Float", "width": 200},
        {"label": "Timesheet Summary", "fieldname": "timesheet_link", "fieldtype": "Data", "width": 200},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("project"):
        conditions += " AND td.project = %(project)s"
        values["project"] = filters.get("project")
    if filters.get("department"):
        conditions += " AND p.department = %(department)s"
        values["department"] = filters["department"]
    if filters.get("from_date"):
        conditions += " AND ts.start_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND ts.end_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    if filters.get("project_status"):
        statuses = filters.get("project_status")

        if isinstance(statuses, str):
            statuses = frappe.parse_json(statuses)

        if statuses:
            conditions += " AND p.status IN %(project_status)s"
            values["project_status"] = tuple(statuses)
    # ✅ MAIN FIX: aggregate ONLY from Timesheet Detail
    result = frappe.db.sql(f"""
        SELECT
            td.project AS project,
            p.department,
            COALESCE(p.custom_project_hours, 0) AS project_hours,

            ROUND(SUM(td.hours), 2) AS used_hours,

            ROUND(
                COALESCE(p.custom_project_hours, 0) - SUM(td.hours),
                2
            ) AS remaining_hours

        FROM `tabTimesheet Detail` td
        INNER JOIN `tabTimesheet` ts
            ON ts.name = td.parent
            AND ts.docstatus = 1

        LEFT JOIN `tabProject` p
            ON p.name = td.project

        WHERE 1=1
        {conditions}

        GROUP BY td.project, p.custom_project_hours

        ORDER BY td.project
    """, values, as_dict=True)

    # 🔗 Link
    for row in result:
        url = "/app/query-report/Project Based Timesheet Summary?" + urlencode({
            "project": row.project,
            "start_date": filters.get("from_date") or "",
            "end_date": filters.get("to_date") or "",
            "department": filters.get("department") or ""
        })

        row["timesheet_link"] = f'<a href="{url}" target="_blank">View Timesheet</a>'

    return result