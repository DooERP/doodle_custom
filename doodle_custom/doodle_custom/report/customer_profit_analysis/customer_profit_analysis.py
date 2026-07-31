# Copyright (c) 2026, Doodle Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 250,
		},
		{
			"label": _("Invoice Amount"),
			"fieldname": "invoice_amount",
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"label": _("Delivery Cost Amount"),
			"fieldname": "delivery_cost_amount",
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"label": _("Difference"),
			"fieldname": "difference",
			"fieldtype": "Currency",
			"width": 180,
		}
	]


def get_data(filters):
	conditions_si = ""
	conditions_dn = ""

	if filters.get("from_date"):
		conditions_si += " AND posting_date >= %(from_date)s"
		conditions_dn += " AND dn.posting_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions_si += " AND posting_date <= %(to_date)s"
		conditions_dn += " AND dn.posting_date <= %(to_date)s"

	if filters.get("customer"):
		conditions_si += " AND customer = %(customer)s"
		conditions_dn += " AND dn.customer = %(customer)s"

	if filters.get("delivery_note_status"):
		conditions_dn += " AND dn.status = %(delivery_note_status)s"

	invoice_data = frappe.db.sql(
		f"""
		SELECT
			customer,
			SUM(base_net_total) AS invoice_amount
		FROM `tabSales Invoice`
		WHERE
			docstatus = 1
			AND cost_center = 'Dooprint - DTL'
			{conditions_si}
		GROUP BY customer
		""",
		filters,
		as_dict=True,
	)

	delivery_data = frappe.db.sql(
		f"""
		SELECT
			dn.customer,
			SUM(dni.incoming_rate * dni.qty) AS delivery_cost_amount
		FROM `tabDelivery Note` dn
		INNER JOIN `tabDelivery Note Item` dni
			ON dni.parent = dn.name
		WHERE
			dn.docstatus IN (0, 1)
			AND dni.cost_center = 'Dooprint - DTL'
			{conditions_dn}
		GROUP BY dn.customer
		""",
		filters,
		as_dict=True,
	)

	result = {}

	for row in invoice_data:
		result[row.customer] = {
			"customer": row.customer,
			"invoice_amount": row.invoice_amount or 0,
			"delivery_cost_amount": 0,
		}

	for row in delivery_data:
		if row.customer not in result:
			result[row.customer] = {
				"customer": row.customer,
				"invoice_amount": 0,
				"delivery_cost_amount": 0,
			}

		result[row.customer]["delivery_cost_amount"] = (
			row.delivery_cost_amount or 0
		)

		data = []
		for row in result.values():
			row["difference"] = (row.get("invoice_amount") or 0) - (row.get("delivery_cost_amount") or 0)
			data.append(row)

		return sorted(data, key=lambda x: x["customer"])