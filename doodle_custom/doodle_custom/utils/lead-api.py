import frappe
import requests
from frappe.utils import now

@frappe.whitelist()
def auto_lead_creation():
        try:
            API_URL = "https://doodletech.ae/wp-json/contact-form/test/v3/data/"
            response = requests.get(API_URL)
            response.raise_for_status()
            leads_data = response.json()
            
            frappe.logger().info(f"Fetched data from API: {leads_data}")
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"Failed to fetch leads from API: {str(e)}", "API Lead Fetch Error")
            return

        for lead in leads_data:
            try:
                form_data = lead.get('form_data', {})
                form_type = lead.get('formtype', '')
                
                frappe.logger().info(f"Processing form type: {form_type} with data: {form_data}")
                
                if isinstance(form_data, dict):
                    # Handle each form type separately
                    if form_type == "Get A Free Quote":
                        process_get_a_free_quote(form_data)
                    elif form_type == "Contact Us":
                        process_contact_us(form_data)
                    elif form_type == "Enquire Now - Popup":
                        process_enquire_now_popup(form_data)
                    elif form_type == "Get a free quote - common":
                        process_get_a_free_quote_common(form_data)  # New form type handler
                    else:
                        frappe.log_error(f"Unsupported form type: {form_type}", "Unsupported Form Type Error")
                else:
                    frappe.log_error(f"form_data is not a dictionary for form type: {form_type}", "Invalid form_data Error")
            except Exception as e:
                frappe.log_error(f"Error processing lead for form type: {form_type}. Error: {str(e)}", "Lead Processing Error")

# Function to process "Get A Free Quote" form type
def process_get_a_free_quote(form_data):
    try:
        email = form_data.get("your-email", "")
        if not email or frappe.db.exists("Lead", {"email_id": email}):
            frappe.logger().info(f"Lead already exists for email: {email}")
            return  # Skip lead creation if the email already exists

        name = form_data.get("your-name", "Unknown")
        phone = form_data.get("your-phone", "")
        services = form_data.get("service", [])
        company = form_data.get("company-name", "N/A")
        country = form_data.get("country-name", "N/A")
        state = form_data.get("state", "N/A")
        page_title = form_data.get("page_title", "")
        kc_captcha = form_data.get("kc_captcha", "")
        kc_honeypot = form_data.get("kc_honeypot", "")
        
        # Convert services to a string
        services_str = ", ".join(services) if services else "Others"
        
        # Prepare the lead data
        new_lead_data = {
            "doctype": "Lead",
            "lead_name": name,
            "email_id": email,
            "phone": phone,
            "company_name": company,
            "source": "Website Form Submission - Get A Free Quote",
            "status": "Lead",
            "company": "Doodle Technologies LLC",
            # "division": "Doodle Web - DTL",
            "lead_owner": frappe.session.user,
            "creation": now(),
            "page_title": page_title,
            "country_name": country,
            "state": state,
            "kc_captcha": kc_captcha,
            "kc_honeypot": kc_honeypot,
            "custom_new_services": services_str
        }

        new_lead = frappe.get_doc(new_lead_data)
        new_lead.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(f"New Lead Created: {new_lead.name} for 'Get A Free Quote'")
    except Exception as e:
        frappe.log_error(f"Failed to create lead for 'Get A Free Quote'. Error: {str(e)}", "Lead Creation Error")

# Function to process "Contact Us" form type
def process_contact_us(form_data):
    try:
        email = form_data.get("your-email", "")
        if not email or frappe.db.exists("Lead", {"email_id": email}):
            frappe.logger().info(f"Lead already exists for email: {email}")
            return  # Skip lead creation if the email already exists

        name = form_data.get("your-name", "Unknown")
        phone = form_data.get("your-phone", "")
        services = form_data.get("service", [])
        company = form_data.get("company-name", "N/A")
        message = form_data.get("your-message", "")
        page_title = form_data.get("page_title", "")
        website = form_data.get("website", "")
        
        # Convert services to a string
        services_str = ", ".join(services) if services else "Others"
        
        # Prepare the lead data
        new_lead_data = {
            "doctype": "Lead",
            "lead_name": name,
            "email_id": email,
            "phone": phone,
            "company_name": company,
            "source": "Website Form Submission - Contact Us",
            "status": "Lead",
            "company": "Doodle Technologies LLC",
            # "division": "Doodle Web - DTL",
            "lead_owner": frappe.session.user,
            "creation": now(),
            "custom_message": message,
            "website": website,
            "page_title": page_title,
            "custom_new_services": services_str,
            "custom_services" : "Others"
        }

        new_lead = frappe.get_doc(new_lead_data)
        new_lead.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(f"New Lead Created: {new_lead.name} for 'Contact Us'")
    except Exception as e:
        frappe.log_error(f"Failed to create lead for 'Contact Us'. Error: {str(e)}", "Lead Creation Error")

# Function to process "Enquire Now - Popup" form type
def process_enquire_now_popup(form_data):
    try:
        email = form_data.get("your-email", "")
        if not email or frappe.db.exists("Lead", {"email_id": email}):
            frappe.logger().info(f"Lead already exists for email: {email}")
            return  # Skip lead creation if the email already exists

        name = form_data.get("your-name", "Unknown")
        phone = form_data.get("your-phone", "")
        services = form_data.get("service", [])
        message = form_data.get("your-message", "")
        page_title = form_data.get("page_title", "")
        website = form_data.get("website", "")
        
        # Convert services to a string
        services_str = ", ".join(services) if services else ""
        
        # Prepare the lead data
        new_lead_data = {
            "doctype": "Lead",
            "lead_name": name,
            "email_id": email,
            "phone": phone,
            "source": "Website Form Submission - Enquire Now - Popup",
            "status": "Lead",
            "company": "Doodle Technologies LLC",
            # "division": "Doodle Web - DTL",
            "lead_owner": frappe.session.user,
            "creation": now(),
            "custom_message": message,
            "website": website,
            "page_title": page_title,
            "custom_new_services": services_str
        }

        new_lead = frappe.get_doc(new_lead_data)
        new_lead.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(f"New Lead Created: {new_lead.name} for 'Enquire Now - Popup'")
    except Exception as e:
        frappe.log_error(f"Failed to create lead for 'Enquire Now - Popup'. Error: {str(e)}", "Lead Creation Error")

# Function to process "Get a free quote - common" form type
def process_get_a_free_quote_common(form_data):
    try:
        email = form_data.get("your-email", "")
        if not email or frappe.db.exists("Lead", {"email_id": email}):
            frappe.logger().info(f"Lead already exists for email: {email}")
            return  # Skip lead creation if the email already exists

        name = form_data.get("your-name", "Unknown")
        phone = form_data.get("your-phone", "")
        services = form_data.get("service", [])
        company = form_data.get("company-name", "N/A")
        message = form_data.get("your-message", "")
        country = form_data.get("country-name", "N/A")
        state = form_data.get("state", "N/A")
        page_title = form_data.get("page_title", "")

        # Convert services to a string
        services_str = ", ".join(services) if services else "Others"

        # Prepare the lead data
        new_lead_data = {
            "doctype": "Lead",
            "lead_name": name,
            "email_id": email,
            "phone": phone,
            "company_name": company,
            "source": "Website Form Submission - Get a free quote - common",
            "status": "Lead",
            "company": "Doodle Technologies LLC",
            "lead_owner": frappe.session.user,
            "creation": now(),
            "page_title": page_title,
            "custom_message": message,
            "country_name": country,
            "state": state,
            "custom_new_services": services_str
        }

        new_lead = frappe.get_doc(new_lead_data)
        new_lead.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(f"New Lead Created: {new_lead.name} for 'Get a free quote - common'")
    except Exception as e:
        frappe.log_error(f"Failed to create lead for 'Get a free quote - common'. Error: {str(e)}", "Lead Creation Error")

