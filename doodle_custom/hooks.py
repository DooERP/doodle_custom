from . import __version__ as app_version

app_name = "doodle_custom"
app_title = "Doodle Custom"
app_publisher = "Doodle Tech"
app_description = "Doodle Tech"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "helpdesk@doodletech.ae"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/doodle_custom/css/doodle_custom.css"
# app_include_js = "/assets/doodle_custom/js/doodle_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/doodle_custom/css/doodle_custom.css"
# web_include_js = "/assets/doodle_custom/js/doodle_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "doodle_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Process Statement Of Accounts" : "public/js/process_statement_of_accounts_custom.js"},
doctype_js = {"Asset" : "public/js/asset.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "doodle_custom.install.before_install"
# after_install = "doodle_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "doodle_custom.uninstall.before_uninstall"
# after_uninstall = "doodle_custom.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "doodle_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }
override_doctype_class = {
	"Process Statement Of Accounts": "doodle_custom.doodle_custom.utils.process_statement_of_accounts.ProcessStatementOfAccountsCustom"
}

override_doctype_class = {
	'Customize Form': 'doodle_custom.custom.customize_form.CustomCustomizeForm',
	'Lead': 'doodle_custom.doodle_custom.doctype.lead.lead.CustomLead',
	'Subscription':'doodle_custom.doodle_custom.doctype.subscription.subscription.CustomSubscription',
	'Sales Order':'doodle_custom.doodle_custom.doctype.sales_order.sales_order.CustomSalesOrder'
}
# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Sales Invoice": {
# 		"on_submit": "doodle_custom.doodle_custom.doctype.sales_invoice.sales_invoice_custom.on_sales_invoice_after_submit"
# 	}
# }
doc_events = {
	"Opportunity":{
		"after_insert":"doodle_custom.doodle_custom.doctype.opportunity.opportunity_custom.opportunity_comment"
	},
    "Sales Invoice": {
        "validate": "doodle_custom.doodle_custom.doctype.sales_invoice.sales_invoice_custom.validate_sales_invoice"
    },
    "Delivery Note": {
        "validate": "doodle_custom.doodle_custom.doctype.delivery_note.delivery_note.validate_delivery_note"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "doodle_custom.tasks.daily",
        "doodle_custom.doodle_custom.utils.cleanup.call_cleanup_endpoint"
    ],
	"hourly": [
        "doodle_custom.doodle_custom.doctype.zktecho_check_in_logs.zktecho_check_in_logs.enqueue_fetch_and_process_data"
    ],
    "cron": {
        "0 8 * * *": [
            "doodle_custom.tasks.cron"
        ],
        "*/5 * * * *": [
            "doodle_custom.doodle_custom.utils.lead-api.auto_lead_creation"
        ],
		"10 22 * * *": [
			"doodle_custom.custom.zkteco.enqueue_sync_zkteco_logs"
		],
		"* * * * *": [
            "doodle_custom.custom.zkteco.sync_morning_checkins"
        ],
    }
}
 

# Testing
# -------

# before_tests = "doodle_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "doodle_custom.event.get_events"
# }
whitelist = ['doodle_custom.doodle_custom.utils.process_statement_of_accounts.download_statements']
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "doodle_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["doodle_custom.utils.before_request"]
# after_request = ["doodle_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["doodle_custom.utils.before_job"]
# after_job = ["doodle_custom.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"doodle_custom.auth.validate"
# ]

