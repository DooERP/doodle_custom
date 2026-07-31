import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # 1. Dynamically build the WHERE clause based on active filters
    conditions = ""
    if filters.get("employee"):
        conditions += " AND ts.employee = %(employee)s"
    if filters.get("project"):
        conditions += " AND ts.parent_project = %(project)s"
    if filters.get("approval_status"):
        conditions += " AND ts.workflow_state = %(approval_status)s"
    if filters.get("from_date"):
        conditions += " AND DATE(tsd.from_time) >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND DATE(tsd.from_time) <= %(to_date)s"

    # 2. Define your columns cleanly
    columns = [
        {"fieldname": "project_name", "label": "Project Name", "fieldtype": "Link", "options": "Project", "width": 150},
        {"fieldname": "user_name", "label": "User Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 110},
        {"fieldname": "task", "label": "Task", "fieldtype": "Link", "options": "Task", "width": 150},
        {"fieldname": "description", "label": "Activity Description", "fieldtype": "Data", "width": 250},
        {"fieldname": "hours", "label": "Hours Entered", "fieldtype": "Float", "width": 100},
        {"fieldname": "approval_status", "label": "Approval Status", "fieldtype": "Data", "width": 120}
    ]

    # 3. Execute the Query (Injecting the dynamic conditions)
    data = frappe.db.sql(f"""
        SELECT
            ts.parent_project AS project_name,
            ts.employee_name AS user_name,
            tsd.from_time AS date,
            tsd.task AS task,
            tsd.description AS description,
            tsd.hours AS hours,
            ts.workflow_state AS approval_status
        FROM
            `tabTimesheet` ts
        JOIN
            `tabTimesheet Detail` tsd ON tsd.parent = ts.name
        WHERE
            ts.docstatus < 2 
            {conditions}
        ORDER BY 
            tsd.from_time DESC
    """, filters, as_dict=True)

    return columns, data