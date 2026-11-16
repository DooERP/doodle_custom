import frappe
from datetime import date, datetime, timedelta
import requests
import json
from frappe.utils import add_to_date

@frappe.whitelist()
def on_sales_invoice_after_submit(doc, handler=""):
    if doc.auto_repeat_frequency == 'Daily':

        new_si = frappe.new_doc("Sales Invoice")
        for i in doc.items:
            after_1_days = add_to_date(datetime.now(), days=1, as_string=True)
            new_si.append("items",{
                                    'item_code':i.item_code,
                                    'item_name':i.item_name,
                                    'description':i.description,
                                    'from_date':datetime.now(),
                                    'plan_frequency':i.plan_frequency, 
                                    'to_date':after_1_days,
                                    'qty':i.qty,
                                    'rate':i.rate,  
                                    'amount':i.amount,
                                    'uom':i.uom,
                                    'cost_center':i.cost_center
                                })
        new_si.customer = doc.customer
        new_si.cost_center = doc.cost_center
        new_si.po = doc.po
        new_si.vat_no = doc.vat_no
        new_si.auto_repeat_frequency = doc.auto_repeat_frequency
        new_si.flags.ignore_permissions  = True
        new_si.save()
    
    if doc.auto_repeat_frequency == 'Monthly':

        new_si = frappe.new_doc("Sales Invoice")
        for i in doc.items:
            after_30_days = add_to_date(datetime.now(), months=1, as_string=True)
            new_si.append("items",{
                                    'item_code':i.item_code,
                                    'item_name':i.item_name,
                                    'description':i.description,
                                    'from_date':datetime.now(),
                                    'plan_frequency':i.plan_frequency, 
                                    'to_date':after_30_days,
                                    'qty':i.qty,
                                    'rate':i.rate,  
                                    'amount':i.amount,
                                    'uom':i.uom,
                                    'cost_center':i.cost_center
                                })
        new_si.customer = doc.customer
        new_si.cost_center = doc.cost_center
        new_si.po = doc.po
        new_si.vat_no = doc.vat_no
        new_si.auto_repeat_frequency = doc.auto_repeat_frequency
        new_si.flags.ignore_permissions  = True
        new_si.save()

    elif doc.auto_repeat_frequency == 'Quarterly':

        new_si = frappe.new_doc("Sales Invoice")
        for i in doc.items:
            after_3_month = add_to_date(datetime.now(), months=3, as_string=True)
            new_si.append("items",{
                                    'item_code':i.item_code,
                                    'item_name':i.item_name,
                                    'description':i.description,
                                    'from_date':datetime.now(),
                                    'plan_frequency':i.plan_frequency, 
                                    'to_date':after_3_month,
                                    'qty':i.qty,
                                    'rate':i.rate,  
                                    'amount':i.amount,
                                    'uom':i.uom,
                                    'cost_center':i.cost_center
                                })
        new_si.customer = doc.customer
        new_si.cost_center = doc.cost_center
        new_si.po = doc.po
        new_si.vat_no = doc.vat_no
        new_si.auto_repeat_frequency = doc.auto_repeat_frequency
        new_si.flags.ignore_permissions  = True
        new_si.save()

    elif doc.auto_repeat_frequency == 'Half-yearly':

        new_si = frappe.new_doc("Sales Invoice")
        for i in doc.items:
            after_Half_Years = add_to_date(datetime.now(), months=6, as_string=True)
            new_si.append("items",{
                                    'item_code':i.item_code,
                                    'item_name':i.item_name,
                                    'description':i.description,
                                    'from_date':datetime.now(),
                                    'plan_frequency':i.plan_frequency, 
                                    'to_date':after_Half_Years,
                                    'qty':i.qty,
                                    'rate':i.rate,  
                                    'amount':i.amount,
                                    'uom':i.uom,
                                    'cost_center':i.cost_center
                                })
        new_si.customer = doc.customer
        new_si.cost_center = doc.cost_center
        new_si.po = doc.po
        new_si.vat_no = doc.vat_no
        new_si.auto_repeat_frequency = doc.auto_repeat_frequency
        new_si.flags.ignore_permissions  = True
        new_si.save()

    elif doc.auto_repeat_frequency == 'Yearly':

        new_si = frappe.new_doc("Sales Invoice")
        for i in doc.items:
            after_1_Years = add_to_date(datetime.now(), months=12, as_string=True)
            new_si.append("items",{
                                    'item_code':i.item_code,
                                    'item_name':i.item_name,
                                    'description':i.description,
                                    'from_date':datetime.now(),
                                    'plan_frequency':i.plan_frequency, 
                                    'to_date':after_1_Years,
                                    'qty':i.qty,
                                    'rate':i.rate,  
                                    'amount':i.amount,
                                    'uom':i.uom,
                                    'cost_center':i.cost_center
                                })
        new_si.customer = doc.customer
        new_si.cost_center = doc.cost_center
        new_si.po = doc.po
        new_si.vat_no = doc.vat_no
        new_si.auto_repeat_frequency = doc.auto_repeat_frequency
        new_si.flags.ignore_permissions  = True
        new_si.save()
            

    else:
        pass

def validate_sales_invoice(doc, method):
    """
    Enforces that Sales Invoice must have a linked Sales Order.
    """
    if doc.is_return:
        return
    if not any(item.sales_order for item in doc.items):
        frappe.throw("Sales Order is mandatory for Sales Invoice.")