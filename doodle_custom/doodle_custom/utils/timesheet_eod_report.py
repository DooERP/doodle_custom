import frappe
from frappe.utils import getdate, nowdate, add_days, formatdate


def get_active_employees():
    return frappe.get_all(
        "Employee",
        filters={
            "status": "Active"
        },
        fields=[
            "name",
            "employee_name",
            "user_id",
        ],
    )


def is_employee_on_leave(employee, date):
    """
    Check approved leave for employee on given date.
    """

    return frappe.db.exists(
        "Leave Application",
        {
            "employee": employee,
            "from_date": ["<=", date],
            "to_date": [">=", date],
            "status": "Approved",
            "docstatus": 1,
        },
    )


def get_employee_timesheet_details(employee, date):
    """
    Check Timesheet created on given date
    and calculate total hours + maximum task hours.
    """

    timesheets = frappe.get_all(
        "Timesheet",
        filters={
            "employee": employee,
            "creation": [
                "between",
                [
                    f"{date} 00:00:00",
                    f"{date} 20:00:00",
                ],
            ],
            "docstatus": ["!=", 2],
        },
        fields=[
            "name",
            "total_hours",
        ],
    )

    total_hours = 0
    max_task_hours = 0
    max_task = ""

    for timesheet in timesheets:

        total_hours += float(
            timesheet.total_hours or 0
        )

        time_logs = frappe.get_all(
            "Timesheet Detail",
            filters={
                "parent": timesheet.name,
                "parenttype": "Timesheet",
                "parentfield": "time_logs",
            },
            fields=[
                "hours",
                "activity_type",
                "task",
                "project",
                "description",
            ],
        )

        for log in time_logs:

            hours = float(log.hours or 0)

            if hours > max_task_hours:

                max_task_hours = hours

                max_task = (
                    log.task
                    or log.activity_type
                    or log.description
                    or "N/A"
                )

    return {
        "timesheet_count": len(timesheets),
        "total_hours": round(total_hours, 2),
        "max_task_hours": round(max_task_hours, 2),
        "max_task": max_task,
    }


def get_daily_report(date=None):

    date = getdate(date or nowdate())

    employees = get_active_employees()

    report = {
        "date": date,
        "added": [],
        "missing": [],
        "on_leave": [],
    }

    for employee in employees:

        employee_name = (
            employee.employee_name
            or employee.name
        )

        # Leave check first
        if is_employee_on_leave(
            employee.name,
            date
        ):

            report["on_leave"].append(
                {
                    "employee": employee.name,
                    "employee_name": employee_name,
                }
            )

            continue

        details = get_employee_timesheet_details(
            employee.name,
            date
        )

        if details["timesheet_count"] > 0:

            report["added"].append(
                {
                    "employee": employee.name,
                    "employee_name": employee_name,
                    "total_hours": details["total_hours"],
                    "max_task_hours": details["max_task_hours"],
                    "max_task": details["max_task"],
                }
            )

        else:

            report["missing"].append(
                {
                    "employee": employee.name,
                    "employee_name": employee_name,
                }
            )

    return report


def generate_daily_html(report):

    date = formatdate(
        report["date"],
        "dd-mm-yyyy"
    )

    html = f"""
    <h2>Daily Timesheet Report</h2>

    <p>
        <b>Date:</b> {date}
    </p>

    <h3>Timesheet Added</h3>

    <table border="1"
           cellpadding="6"
           cellspacing="0"
           style="border-collapse:collapse;width:100%;">

        <tr>
            <th>Employee</th>
            <th>Total Hours</th>
            <th>Max Task Hours</th>
            <th>Task</th>
        </tr>
    """

    for row in report["added"]:

        html += f"""
        <tr>
            <td>{row["employee_name"]}</td>
            <td>{row["total_hours"]}</td>
            <td>{row["max_task_hours"]}</td>
            <td>{row["max_task"]}</td>
        </tr>
        """

    if not report["added"]:

        html += """
        <tr>
            <td colspan="4">
                No timesheets added.
            </td>
        </tr>
        """

    html += """
    </table>

    <br>

    <h3>Timesheet Not Added</h3>

    <table border="1"
           cellpadding="6"
           cellspacing="0"
           style="border-collapse:collapse;width:100%;">

        <tr>
            <th>Employee</th>
            <th>Status</th>
        </tr>
    """

    for row in report["missing"]:

        html += f"""
        <tr>
            <td>{row["employee_name"]}</td>
            <td>Timesheet Not Added</td>
        </tr>
        """

    if not report["missing"]:

        html += """
        <tr>
            <td colspan="2">
                Everyone has added timesheet.
            </td>
        </tr>
        """

    html += """
    </table>

    <br>

    <h3>Employees On Leave</h3>

    <table border="1"
           cellpadding="6"
           cellspacing="0"
           style="border-collapse:collapse;width:100%;">

        <tr>
            <th>Employee</th>
            <th>Status</th>
        </tr>
    """

    for row in report["on_leave"]:

        html += f"""
        <tr>
            <td>{row["employee_name"]}</td>
            <td>On Leave</td>
        </tr>
        """

    if not report["on_leave"]:

        html += """
        <tr>
            <td colspan="2">
                No employees are on leave.
            </td>
        </tr>
        """

    html += """
    </table>
    """

    return html


def get_weekly_missing_report(date=None):

    date = getdate(date or nowdate())

    # Monday of current week
    monday = add_days(
        date,
        -date.weekday()
    )

    employees = get_active_employees()

    report = []

    for employee in employees:

        missing_days = []

        current_date = monday

        while current_date <= date:

            # Don't count leave as missing
            if is_employee_on_leave(
                employee.name,
                current_date
            ):

                current_date = add_days(
                    current_date,
                    1
                )

                continue

            details = get_employee_timesheet_details(
                employee.name,
                current_date
            )

            if details["timesheet_count"] == 0:

                missing_days.append(
                    current_date
                )

            current_date = add_days(
                current_date,
                1
            )

        if missing_days:

            report.append(
                {
                    "employee": employee.name,
                    "employee_name": (
                        employee.employee_name
                        or employee.name
                    ),
                    "missing_days": missing_days,
                }
            )

    return report


def generate_weekly_html(report):

    html = """
    <h2>Weekly Missing Timesheet Report</h2>

    <table border="1"
           cellpadding="6"
           cellspacing="0"
           style="border-collapse:collapse;width:100%;">

        <tr>
            <th>Employee</th>
            <th>Missing Timesheet Dates</th>
        </tr>
    """

    for row in report:

        dates = ", ".join(
            formatdate(
                date,
                "dd-mm-yyyy"
            )
            for date in row["missing_days"]
        )

        html += f"""
        <tr>
            <td>{row["employee_name"]}</td>
            <td>{dates}</td>
        </tr>
        """

    if not report:

        html += """
        <tr>
            <td colspan="2">
                No missing timesheets this week.
            </td>
        </tr>
        """

    html += """
    </table>
    """

    return html


def send_email(subject, html):

    recipients = [
        "shivam.rathod@doodletech.ae"
        
    ]

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=html,
        # add_css=False,
    )


def generate_whatsapp_message(report):

    date = formatdate(
        report["date"],
        "dd-mm-yyyy"
    )

    message = (
        f"*Daily Timesheet Report*\n"
        f"Date: {date}\n\n"
        f"*Timesheet Added:* "
        f"{len(report['added'])}\n"
        f"*Timesheet Missing:* "
        f"{len(report['missing'])}\n"
        f"*On Leave:* "
        f"{len(report['on_leave'])}\n\n"
    )

    message += "*Timesheet Added:*\n"

    for row in report["added"]:

        message += (
            f"• {row['employee_name']} - "
            f"{row['total_hours']} hrs\n"
        )

    message += "\n*Timesheet Missing:*\n"

    for row in report["missing"]:

        message += (
            f"• {row['employee_name']}\n"
        )

    message += "\n*On Leave:*\n"

    for row in report["on_leave"]:

        message += (
            f"• {row['employee_name']}\n"
        )

    return message


def send_eod_timesheet_report():
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

    today = getdate()

    # -----------------------------
    # DAILY REPORT
    # -----------------------------

    daily_report = get_daily_report(
        today
    )

    daily_html = generate_daily_html(
        daily_report
    )

    send_email(
        subject=(
            f"Daily Timesheet Report - "
            f"{formatdate(today, 'dd-mm-yyyy')}"
        ),
        html=daily_html,
    )

    whatsapp_message = (
        generate_whatsapp_message(
            daily_report
        )
    )

    # ----------------------------------
    # WHATSAPP API CALL WILL COME HERE
    # ----------------------------------

    # Example:
    #
    # send_whatsapp_message(
    #     whatsapp_message
    # )


    # -----------------------------
    # FRIDAY WEEKLY REPORT
    # -----------------------------

    # Python weekday:
    # Monday = 0
    # Tuesday = 1
    # Wednesday = 2
    # Thursday = 3
    # Friday = 4

    if today.weekday() == 4:

        weekly_report = (
            get_weekly_missing_report(
                today
            )
        )

        weekly_html = (
            generate_weekly_html(
                weekly_report
            )
        )

        send_email(
            subject=(
                f"Weekly Missing Timesheet Report - "
                f"{formatdate(today, 'dd-mm-yyyy')}"
            ),
            html=weekly_html,
        )