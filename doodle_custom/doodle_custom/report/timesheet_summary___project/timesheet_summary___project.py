# # Copyright (c) 2025, doodle tech and contributors
# # For license information, please see license.txt

# import frappe
# import importlib
# from frappe.utils.xlsxutils import make_xlsx
# from frappe import _

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data

# def get_columns():
#     return [
#         {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 120},
#         {"label": _("Timesheet ID"), "fieldname": "name", "fieldtype": "Link", "options": "Timesheet", "width": 120},
#         {"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
#         {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
#         {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 120, "hidden":1},
#         {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 120, "hidden":1},
#         {"label": _("Total Hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 120, "hidden":1},
#         {"label": _("From Time"), "fieldname": "from_time", "fieldtype": "Datetime", "width": 120},
#         {"label": _("To Time"), "fieldname": "to_time", "fieldtype": "Datetime", "width": 120},
#         {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
#         # {"label": _("Normal Time"), "fieldname": "custom_normal_hrs", "fieldtype": "Time", "width": 120,},
#         {"label": _("Hours"), "fieldname": "hours", "fieldtype": "Float", "width": 120},
#         # {"label": _("OT on Holiday"), "fieldname": "custom_ot_on_holiday", "fieldtype": "Float", "width": 120},
#         {"label": _("OT Hours"), "fieldname": "custom_ot_hours", "fieldtype": "Float", "width": 120},
#     ]

# def get_data(filters):
#     conditions = ""
#     values = {}

#     if filters.get("start_date"):
#         conditions += " AND t.start_date >= %(start_date)s"
#         values["start_date"] = filters.get("start_date")

#     if filters.get("end_date"):
#         conditions += " AND t.end_date <= %(end_date)s"
#         values["end_date"] = filters.get("end_date")

#     if filters.get("employee"):
#         conditions += " AND t.employee = %(employee)s"
#         values["employee"] = filters.get("employee")

#     if filters.get("project"):
#         conditions += " AND td.project = %(project)s"
#         values["project"] = filters.get("project")

#     return frappe.db.sql(f"""
#         SELECT 
#             t.name,
#             t.employee,
#             t.employee_name,
#             t.total_hours,
#             t.start_date,
#             t.end_date,
#             t.status,
#             td.from_time,
#             td.to_time,
#             td.project,
#             td.custom_normal_hrs,
#             td.custom_ot_on_holiday,
#             td.hours,
#             t.custom_ot_hours
#         FROM `tabTimesheet` t
#         LEFT JOIN `tabTimesheet Detail` td ON t.name = td.parent
#         WHERE 1=1 {conditions}
#         ORDER BY t.employee ASC, td.from_time ASC
#     """, values, as_dict=True)

# baugette_custom/baugette_custom/report/timesheet_summary_project/timesheet_summary_project.py

import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    
    columns = [
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 120},
        {"label": _("Timesheet ID"), "fieldname": "name", "fieldtype": "Link", "options": "Timesheet", "width": 120},
        {"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 120, "hidden":1},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 120, "hidden":1},
        {"label": _("Total Hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 120, "hidden":1},
        {"label": _("From Time"), "fieldname": "from_time", "fieldtype": "Datetime", "width": 120},
        {"label": _("To Time"), "fieldname": "to_time", "fieldtype": "Datetime", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": _("Hours"), "fieldname": "hours", "fieldtype": "Float", "width": 120},
        {"label": _("OT Hours"), "fieldname": "custom_ot_hours", "fieldtype": "Float", "width": 120},
    ]
    
    # Build SQL filters
    conditions = ""
    values = {}
    if filters.get("start_date"):
        conditions += " AND t.start_date >= %(start_date)s"
        values["start_date"] = filters.get("start_date")
    if filters.get("end_date"):
        conditions += " AND t.end_date <= %(end_date)s"
        values["end_date"] = filters.get("end_date")
    if filters.get("employee"):
        conditions += " AND t.employee = %(employee)s"
        values["employee"] = filters.get("employee")
    if filters.get("project"):
        conditions += " AND td.project = %(project)s"
        values["project"] = filters.get("project")
    
    data = frappe.db.sql(f"""
        SELECT 
            t.name, t.employee, t.employee_name, t.total_hours, t.start_date, t.end_date, t.status,
            td.from_time, td.to_time, td.project, td.custom_normal_hrs, td.custom_ot_on_holiday, td.hours, t.custom_ot_hours
        FROM `tabTimesheet` t
        LEFT JOIN `tabTimesheet Detail` td ON t.name = td.parent
        WHERE 1=1 {conditions}
        ORDER BY t.employee ASC, td.from_time ASC
    """, values, as_dict=True)
    
    return columns, data
