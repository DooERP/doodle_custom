
# import frappe
# import requests
# import json
# from datetime import datetime

# def sync_desert_forest_leads():
#     """
#     Fetch Desert Forest leads and create missing ERPNext Leads.
#     Creates ONE Error Log per scheduler execution containing
#     detailed step-by-step debugging information.
#     """

#     debug_steps = []
#     def debug(step, message, data=None):
#         """
#         Add a detailed step to the execution debug log.
#         """
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         entry = f"[{timestamp}] [{step}] {message}"
#         if data is not None:
#             try:
#                 if isinstance(data, str):
#                     entry += f"\n{data}"
#                 else:
#                     entry += (
#                         "\n"
#                         + json.dumps(
#                             data,
#                             indent=2,
#                             default=str
#                         )
#                     )
#             except Exception:
#                 entry += f"\n{str(data)}"
#         debug_steps.append(entry)

#     def create_debug_error_log(title="Desert Forest Lead Sync - Execution Log"):
#         """
#         Create the final Error Log containing all execution steps.
#         """
#         try:
#             message = "\n\n".join(debug_steps)
#             frappe.log_error(
#                 title=title,
#                 message=message
#             )
#         except Exception:
#             # Do not allow logging failure to break scheduler
#             pass
#     # ==================================================
#     # START
#     # ==================================================
#     start_time = datetime.now()
#     debug(
#         "START",
#         "Desert Forest Lead Sync scheduler execution started."
#     )
#     debug(
#         "START TIME",
#         str(start_time)
#     )
#     # ==================================================
#     # COUNTERS
#     # ==================================================
#     page = 1
#     total_received = 0
#     created_count = 0
#     skipped_count = 0
#     failed_count = 0
#     debug(
#         "COUNTERS",
#         "Counters initialized.",
#         {
#             "page": page,
#             "total_received": total_received,
#             "created_count": created_count,
#             "skipped_count": skipped_count,
#             "failed_count": failed_count
#         }
#     )
#     try:
#         # ==================================================
#         # GET CONFIGURATION
#         # ==================================================
#         debug(
#             "CONFIG",
#             "Reading Desert Forest API configuration."
#         )
#         api_url = frappe.conf.get(
#             "doodle_leads_api"
#         )
#         api_token = frappe.conf.get(
#             "desert_forest_api_token"
#         )
#         if api_url:
#             debug(
#                 "CONFIG",
#                 "API URL found.",
#                 api_url
#             )
#         else:
#             debug(
#                 "CONFIG ERROR",
#                 "doodle_leads_api is missing."
#             )
#             frappe.log_error(
#                 title="Desert Forest API Configuration",
#                 message=(
#                     "doodle_leads_api is missing "
#                     "in site_config.json"
#                 )
#             )
#             create_debug_error_log(
#                 "Desert Forest Lead Sync - Configuration Error"
#             )
#             return {
#                 "status": "failed",
#                 "reason": "API URL missing"
#             }
#         if api_token:
#             api_token = str(api_token).strip()
#             debug(
#                 "CONFIG",
#                 "API token found."
#             )
#         else:
#             debug(
#                 "CONFIG ERROR",
#                 "desert_forest_api_token is missing."
#             )
#             frappe.log_error(
#                 title="Desert Forest API Configuration",
#                 message=(
#                     "desert_forest_api_token is missing "
#                     "in site_config.json"
#                 )
#             )
#             create_debug_error_log(
#                 "Desert Forest Lead Sync - Configuration Error"
#             )
#             return {
#                 "status": "failed",
#                 "reason": "API token missing"
#             }
#         # ==================================================
#         # CHECK CUSTOM FIELD
#         # ==================================================
#         debug(
#             "FIELD CHECK",
#             "Checking custom_desert_forest_lead_id field."
#         )
#         lead_meta = frappe.get_meta("Lead")
#         if not lead_meta.has_field(
#             "custom_desert_forest_lead_id"
#         ):
#             debug(
#                 "FIELD ERROR",
#                 "custom_desert_forest_lead_id does not exist in Lead."
#             )
#             frappe.log_error(
#                 title="Desert Forest Lead Field Missing",
#                 message=(
#                     "Custom field "
#                     "'custom_desert_forest_lead_id' "
#                     "does not exist in Lead."
#                 )
#             )
#             create_debug_error_log(
#                 "Desert Forest Lead Sync - Field Error"
#             )
#             return {
#                 "status": "failed",
#                 "reason": (
#                     "custom_desert_forest_lead_id field missing"
#                 )
#             }
#         debug(
#             "FIELD CHECK",
#             "custom_desert_forest_lead_id exists."
#         )
#         # ==================================================
#         # API HEADERS
#         # ==================================================
#         if api_token.lower().startswith("apikey "):
#             authorization = api_token
#         else:
#             authorization = f"ApiKey {api_token}"
#         headers = {
#             "Accept": "application/json",
#             "Authorization": authorization
#         }
#         debug(
#             "API",
#             "API headers prepared.",
#             {
#                 "Accept": "application/json",
#                 "Authorization": "ApiKey ********"
#             }
#         )
#         # ==================================================
#         # PAGINATION LOOP
#         # ==================================================
#         while True:
#             debug(
#                 "PAGE START",
#                 f"Processing page {page}."
#             )
#             # --------------------------------------------------
#             # API PARAMETERS
#             # --------------------------------------------------
#             params = {
#                 "page": page,
#                 "page_size": 25
#             }
#             debug(
#                 "API PARAMETERS",
#                 f"Parameters for page {page}.",
#                 params
#             )
#             # --------------------------------------------------
#             # CALL API
#             # --------------------------------------------------
#             debug(
#                 "API REQUEST",
#                 f"Sending GET request for page {page}."
#             )
#             try:
#                 response = requests.get(
#                     api_url,
#                     headers=headers,
#                     params=params,
#                     timeout=30
#                 )
#                 debug(
#                     "API RESPONSE",
#                     f"Received response for page {page}.",
#                     {
#                         "status_code": response.status_code,
#                         "url": response.url,
#                         "response_length": len(response.text)
#                     }
#                 )
#             except requests.exceptions.RequestException as e:
#                 debug(
#                     "API REQUEST ERROR",
#                     f"Request failed on page {page}.",
#                     {
#                         "error": str(e),
#                         "traceback": frappe.get_traceback()
#                     }
#                 )
#                 raise
#             # --------------------------------------------------
#             # HTTP ERROR
#             # --------------------------------------------------
#             if response.status_code != 200:
#                 debug(
#                     "HTTP ERROR",
#                     "Desert Forest API returned non-200 status.",
#                     {
#                         "status_code": response.status_code,
#                         "url": response.url,
#                         "response": response.text
#                     }
#                 )
#                 frappe.log_error(
#                     title="Desert Forest API HTTP Error",
#                     message=(
#                         f"URL: {response.url}\n\n"
#                         f"Status Code: {response.status_code}\n\n"
#                         f"Response:\n{response.text}"
#                     )
#                 )
#                 create_debug_error_log(
#                     "Desert Forest Lead Sync - HTTP Error"
#                 )
#                 return {
#                     "status": "failed",
#                     "http_status": response.status_code,
#                     "response": response.text
#                 }
#             # --------------------------------------------------
#             # PARSE JSON
#             # --------------------------------------------------
#             debug(
#                 "JSON",
#                 "Parsing API JSON response."
#             )
#             try:
#                 response_data = response.json()
#                 debug(
#                     "JSON",
#                     "JSON parsed successfully."
#                 )
#             except ValueError:
#                 debug(
#                     "JSON ERROR",
#                     "API response is not valid JSON.",
#                     response.text
#                 )
#                 frappe.log_error(
#                     title="Desert Forest Invalid JSON",
#                     message=(
#                         f"URL: {response.url}\n\n"
#                         f"Response:\n{response.text}"
#                     )
#                 )
#                 create_debug_error_log(
#                     "Desert Forest Lead Sync - JSON Error"
#                 )
#                 return {
#                     "status": "failed",
#                     "reason": "Invalid JSON response"
#                 }
#             # --------------------------------------------------
#             # VALIDATE API RESPONSE
#             # --------------------------------------------------
#             debug(
#                 "API VALIDATION",
#                 "Validating API response."
#             )
#             if (
#                 response_data.get("code") is not True
#                 or response_data.get("statusCode") != 200
#             ):
#                 debug(
#                     "API VALIDATION ERROR",
#                     "API returned an unsuccessful response.",
#                     response_data
#                 )
#                 frappe.log_error(
#                     title="Desert Forest API Response Error",
#                     message=frappe.as_json(
#                         response_data
#                     )
#                 )
#                 create_debug_error_log(
#                     "Desert Forest Lead Sync - API Response Error"
#                 )
#                 return {
#                     "status": "failed",
#                     "response": response_data
#                 }
#             debug(
#                 "API VALIDATION",
#                 "API response validation successful."
#             )
#             # --------------------------------------------------
#             # EXTRACT RESULT
#             # --------------------------------------------------
#             result = response_data.get(
#                 "result"
#             ) or {}
#             leads = result.get(
#                 "items"
#             ) or []
#             pagination = result.get(
#                 "pagination"
#             ) or {}
#             debug(
#                 "API DATA",
#                 f"Page {page} contains {len(leads)} leads.",
#                 {
#                     "lead_count": len(leads),
#                     "pagination": pagination
#                 }
#             )
#             total_received += len(leads)
#             # ==================================================
#             # PROCESS LEADS
#             # ==================================================
#             if not leads:
#                 debug(
#                     "LEADS",
#                     f"No leads returned on page {page}."
#                 )
#             for index, lead_data in enumerate(
#                 leads,
#                 start=1
#             ):
#                 debug(
#                     "LEAD START",
#                     f"Processing lead {index}/{len(leads)} on page {page}.",
#                     {
#                         "external_id": lead_data.get("id"),
#                         "first_name": lead_data.get("first_name"),
#                         "last_name": lead_data.get("last_name"),
#                         "phone_number": lead_data.get("phone_number"),
#                         "stage": lead_data.get("stage")
#                     }
#                 )
#                 try:
#                     status = create_erp_lead(
#                         lead_data,
#                         debug=debug
#                     )
#                     debug(
#                         "LEAD RESULT",
#                         f"Lead processing returned status: {status}.",
#                         {
#                             "external_id": lead_data.get("id"),
#                             "status": status
#                         }
#                     )
#                     if status == "created":
#                         created_count += 1
#                     elif status == "skipped":
#                         skipped_count += 1
#                     else:
#                         failed_count += 1
#                 except Exception as e:
#                     failed_count += 1
#                     debug(
#                         "LEAD ERROR",
#                         f"Exception while processing lead {index}.",
#                         {
#                             "error": str(e),
#                             "external_id": lead_data.get("id"),
#                             "lead_data": lead_data,
#                             "traceback": frappe.get_traceback()
#                         }
#                     )
#                     frappe.log_error(
#                         title="Desert Forest Lead Creation Error",
#                         message=(
#                             f"Lead Data:\n"
#                             f"{frappe.as_json(lead_data)}\n\n"
#                             f"Traceback:\n"
#                             f"{frappe.get_traceback()}"
#                         )
#                     )
#             # ==================================================
#             # PAGINATION
#             # ==================================================
#             has_next = pagination.get(
#                 "has_next"
#             )
#             debug(
#                 "PAGINATION",
#                 f"Page {page} completed.",
#                 {
#                     "has_next": has_next,
#                     "current_page": page
#                 }
#             )
#             if not has_next:
#                 debug(
#                     "PAGINATION",
#                     "No more pages. Pagination completed."
#                 )
#                 break
#             page += 1
#             debug(
#                 "PAGINATION",
#                 f"Moving to next page: {page}."
#             )
#             # --------------------------------------------------
#             # SAFETY LIMIT
#             # --------------------------------------------------
#             if page > 100:
#                 debug(
#                     "PAGINATION ERROR",
#                     "Page number exceeded safety limit of 100."
#                 )
#                 frappe.log_error(
#                     title="Desert Forest Pagination Error",
#                     message=(
#                         "Desert Forest lead sync stopped because "
#                         "page number exceeded 100."
#                     )
#                 )
#                 break
#         # ==================================================
#         # COMMIT
#         # ==================================================
#         debug(
#             "DATABASE",
#             "Committing database transaction."
#         )
#         frappe.db.commit()
#         debug(
#             "DATABASE",
#             "Database commit completed."
#         )
#         # ==================================================
#         # FINAL RESULT
#         # ==================================================
#         end_time = datetime.now()
#         sync_result = {
#             "status": "success",
#             "received": total_received,
#             "created": created_count,
#             "skipped": skipped_count,
#             "failed": failed_count,
#             "pages_processed": page,
#             "start_time": str(start_time),
#             "end_time": str(end_time)
#         }
#         debug(
#             "FINAL RESULT",
#             "Desert Forest lead sync completed successfully.",
#             sync_result
#         )
#         # ==================================================
#         # LOGGER
#         # ==================================================
#         frappe.logger(
#             "desert_forest"
#         ).info(
#             f"Desert Forest lead sync completed: "
#             f"{frappe.as_json(sync_result)}"
#         )
#         # ==================================================
#         # CREATE ONE COMPLETE ERROR LOG
#         # ==================================================
#         create_debug_error_log(
#             "Desert Forest Lead Sync - Execution Log"
#         )
#         return sync_result
#     # ==================================================
#     # REQUEST ERROR
#     # ==================================================
#     except requests.exceptions.RequestException as e:
#         debug(
#             "REQUEST EXCEPTION",
#             "Desert Forest API request exception occurred.",
#             {
#                 "error": str(e),
#                 "traceback": frappe.get_traceback()
#             }
#         )
#         try:
#             frappe.db.rollback()
#         except Exception:
#             pass
#         create_debug_error_log(
#             "Desert Forest Lead Sync - Request Exception"
#         )
#         return {
#             "status": "failed",
#             "reason": "API request exception",
#             "error": str(e)
#         }
#     # ==================================================
#     # UNEXPECTED ERROR
#     # ==================================================
#     except Exception as e:
#         debug(
#             "UNEXPECTED ERROR",
#             "Unexpected exception occurred during scheduler execution.",
#             {
#                 "error": str(e),
#                 "traceback": frappe.get_traceback()
#             }
#         )
#         try:
#             frappe.db.rollback()
#         except Exception:
#             pass
#         create_debug_error_log(
#             "Desert Forest Lead Sync - Unexpected Error"
#         )
#         frappe.log_error(
#             title="Desert Forest Sync Error",
#             message=frappe.get_traceback()
#         )
#         return {
#             "status": "failed",
#             "reason": "Unexpected exception",
#             "error": str(e)
#         }
# def create_erp_lead(lead_data, debug=None):
#     """
#     Create one ERPNext Lead from Desert Forest API data.
#     Returns:
#         created
#         skipped
#         failed
#     """
#     def log(step, message, data=None):
#         if debug:
#             debug(
#                 step,
#                 message,
#                 data
#             )
#     # ==================================================
#     # EXTERNAL LEAD ID
#     # ==================================================
#     log(
#         "LEAD ID",
#         "Reading external Desert Forest lead ID."
#     )
#     external_id = lead_data.get(
#         "id"
#     )
#     if not external_id:
#         log(
#             "LEAD ID ERROR",
#             "External lead ID is missing.",
#             lead_data
#         )
#         frappe.log_error(
#             title="Desert Forest Lead Missing ID",
#             message=frappe.as_json(
#                 lead_data
#             )
#         )
#         return "failed"
#     external_id = str(
#         external_id
#     ).strip()
#     log(
#         "LEAD ID",
#         f"External lead ID: {external_id}"
#     )
#     # ==================================================
#     # DUPLICATE CHECK
#     # ==================================================
#     log(
#         "DUPLICATE CHECK",
#         f"Checking existing Lead for external ID {external_id}."
#     )

#     deleted_record = frappe.db.exists(
#         "External Id Document",
#         {"external_id": external_id}
#     )

#     if deleted_record:
#         log(
#             "DELETED LEAD SKIPPED",
#             f"External ID {external_id} is in External Id Document. Skipping.",
#             {"external_id": external_id, "record": deleted_record}
#         )

#         frappe.logger("desert_forest").info(
#             f"Skipping previously deleted Desert Forest Lead {external_id}"
#         )

#         return "skipped"
    
#     existing_lead = frappe.db.exists(
#         "Lead",
#         {
#             "custom_desert_forest_lead_id": external_id
#         }
#     )
#     if existing_lead:
#         log(
#             "DUPLICATE",
#             f"Lead already exists: {existing_lead}. Skipping."
#         )
#         frappe.logger(
#             "desert_forest"
#         ).info(
#             f"Skipping existing Desert Forest Lead "
#             f"{external_id} -> {existing_lead}"
#         )
#         return "skipped"
#     log(
#         "DUPLICATE CHECK",
#         "No existing Lead found."
#     )
#     # ==================================================
#     # GET API VALUES
#     # ==================================================
#     first_name = str(
#         lead_data.get("first_name") or ""
#     ).strip()
#     last_name = str(
#         lead_data.get("last_name") or ""
#     ).strip()
#     phone_number = str(
#         lead_data.get("phone_number") or ""
#     ).strip()
#     email = str(
#         lead_data.get("email") or ""
#     ).strip()
#     summary = str(
#         lead_data.get("summary") or ""
#     ).strip()
#     stage = str(
#         lead_data.get("stage") or ""
#     ).strip()
#     created_at = lead_data.get(
#         "created_at"
#     )
#     updated_at = lead_data.get(
#         "updated_at"
#     )
#     log(
#         "API VALUES",
#         "API values extracted.",
#         {
#             "external_id": external_id,
#             "first_name": first_name,
#             "last_name": last_name,
#             "phone_number": phone_number,
#             "custom_summary": summary,
#             "stage": stage,
#             "created_at": created_at,
#             "updated_at": updated_at
#         }
#     )
#     # ==================================================
#     # GENERATE NAME
#     # ==================================================
#     lead_name = " ".join(
#         value
#         for value in [
#             first_name,
#             last_name
#         ]
#         if value
#     )
#     if not lead_name:
#         lead_name = (
#             phone_number
#             or "Desert Forest Lead"
#         )
#     if not first_name:
#         first_name = lead_name
#     log(
#         "NAME",
#         "ERPNext Lead name generated.",
#         {
#             "lead_name": lead_name,
#             "first_name": first_name,
#             "last_name": last_name
#         }
#     )
#     # ==================================================
#     # CREATE ERP LEAD
#     # ==================================================
#     log(
#         "CREATE",
#         "Creating new ERPNext Lead document."
#     )
#     lead = frappe.new_doc(
#         "Lead"
#     )
#     lead.first_name = first_name
#     if last_name:
#         lead.last_name = last_name
#     lead.lead_name = lead_name
#     if phone_number:
#         lead.mobile_no = phone_number
#     lead.custom_desert_forest_lead_id = external_id
#     lead.custom_services = (
#         "Others"
#     )
#     lead.source = "Desert Forest"
#     lead.email_id = email
#     lead.custom_summary = summary
#     log(
#         "CREATE",
#         "Lead fields populated.",
#         {
#             "first_name": lead.first_name,
#             "last_name": lead.last_name,
#             "lead_name": lead.lead_name,
#             "mobile_no": lead.mobile_no,
#             "custom_desert_forest_lead_id":
#                 lead.custom_desert_forest_lead_id,
#             "custom_services":
#                 lead.custom_services,
#             "custom_summary":
#                 lead.custom_summary
#         }
#     )
#     # ==================================================
#     # LEAD SOURCE
#     # ==================================================
#     log(
#         "SOURCE",
#         "Checking Lead Source: Website."
#     )
#     if frappe.db.exists(
#         "Lead Source",
#         "Website"
#     ):
#         lead.source = "Website"
#         log(
#             "SOURCE",
#             "Lead Source Website found and assigned."
#         )
#     else:
#         log(
#             "SOURCE",
#             "Lead Source Website does not exist. Source left blank."
#         )
#     # ==================================================
#     # INSERT
#     # ==================================================
#     log(
#         "INSERT",
#         "Inserting Lead into database."
#     )
#     lead.insert(
#         ignore_permissions=True
#     )
#     log(
#         "INSERT SUCCESS",
#         f"Lead created successfully: {lead.name}",
#         {
#             "lead_name": lead.lead_name,
#             "external_id": external_id
#         }
#     )
#     # ==================================================
#     # SEND EMAIL
#     # ==================================================
#     log(
#         "EMAIL",
#         f"Sending notification email to Shafik for Lead {lead.name}."
#     )
#     try:
#         frappe.sendmail(
#             recipients=[
#                 "shafik.m@doodletech.ae",
#                 "enquiry@doodletech.ae",
#                 "priyanka.venugopal@doodletech.ae",
#             ],
#             subject=(
#                 f"New Lead Created - "
#                 f"{lead.lead_name}"
#             ),
#             message=f"""
#                 <p>
#                     A new lead has been created from Desert Forest.
#                 </p>
#                 <p>
#                     <b>Lead:</b> {lead.lead_name}<br>
#                     <b>Lead ID:</b> {lead.name}<br>
#                     <b>First Name:</b> {lead.first_name}<br>
#                     <b>Last Name:</b> {lead.last_name or ""}<br>
#                     <b>Mobile:</b> {lead.mobile_no or ""}<br>
#                     <b>Source:</b> {lead.source or ""}<br>
#                     <b>Email:</b> {lead.email_id or ""}<br>
#                     <b>Summary:</b> {lead.custom_summary or ""}
#                 </p>
#                 <p>
#                     <a href="{frappe.utils.get_url()}/app/lead/{lead.name}">
#                         Open Lead
#                     </a>
#                 </p>
#             """,
#             now=True
#         )
#         log(
#             "EMAIL SUCCESS",
#             f"Notification email sent for Lead {lead.name}."
#         )
#     except Exception as e:
#         log(
#             "EMAIL ERROR",
#             f"Notification email failed for Lead {lead.name}.",
#             {
#                 "error": str(e),
#                 "traceback": frappe.get_traceback()
#             }
#         )
#         frappe.log_error(
#             title="Desert Forest Lead Notification Error",
#             message=frappe.get_traceback()
#         )

#     # ==================================================
#     # FINAL LEAD SUCCESS
#     # ==================================================
#     frappe.logger(
#         "desert_forest"
#     ).info(
#         f"Created ERPNext Lead {lead.name} "
#         f"from Desert Forest Lead {external_id}"
#     )
#     log(
#         "LEAD COMPLETE",
#         f"Successfully completed processing Lead {lead.name}.",
#         {
#             "erp_lead": lead.name,
#             "desert_forest_id": external_id
#         }
#     )
#     return "created"



import frappe
import requests
import json
from datetime import datetime
from html import escape
from urllib.parse import quote

# ============================================================
# CONFIGURATION
# ============================================================

BRANDS = (
    {
        "name": "Doodle",
        "config_key": "doodle_leads_api",
        "division": None
    },
    {
        "name": "Desert Forest",
        "config_key": "desert_forest_leads_api",
        "division": "Doodle Desert Forest - DTL"
    }
)

TOKEN_KEY = "desert_forest_api_token"
EXTERNAL_ID_FIELD = "custom_desert_forest_lead_id"
CONTACT_ID_FIELD = "custom_desert_forest_contact_id"
DIVISION_FIELD = "division"
NOTIFY = (
    "shafik.m@doodletech.ae",
    "enquiry@doodletech.ae",
    "priyanka.venugopal@doodletech.ae"
)

DESERT_FOREST_ADDITIONAL_NOTIFY = (
    "tom@doodletech.ae",
    "haritha@desertforest.ai",
    "anandhu.mohanan@doodletech.ae"
)

# ============================================================
# EXISTING SCHEDULER FUNCTION
# ============================================================

def sync_desert_forest_leads():
    """
    Synchronize Doodle and Desert Forest leads.

    Existing scheduler function name is preserved.
    """
    return sync_brand_leads()

# ============================================================
# MAIN SYNCHRONIZATION
# ============================================================

def sync_brand_leads():

    started = datetime.now()

    steps = []
    results = {}

    def debug(brand, stage, message, details=None):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = (
            f"[{timestamp}] "
            f"[{brand}] "
            f"[{stage}] "
            f"{message}"
        )

        if details is not None:
            line += "\n" + json.dumps(
                details,
                default=str,
                ensure_ascii=False
            )

        steps.append(line)

    try:

        # ====================================================
        # VALIDATE LEAD FIELDS
        # ====================================================

        lead_meta = frappe.get_meta("Lead")

        for field in (
            EXTERNAL_ID_FIELD,
            CONTACT_ID_FIELD,
            DIVISION_FIELD
        ):

            if not lead_meta.has_field(field):
                raise ValueError(
                    f"Required Lead field is missing: {field}"
                )

        # No custom_external_lead_brand field required.

        # ====================================================
        # VALIDATE EXTERNAL ID DOCUMENT
        # ====================================================

        if not frappe.db.exists(
            "DocType",
            "External Id Document"
        ):
            raise ValueError(
                "External Id Document DocType is missing"
            )

        deleted_meta = frappe.get_meta(
            "External Id Document"
        )

        if not deleted_meta.has_field("external_id"):
            raise ValueError(
                "External Id Document.external_id is missing"
            )

        # ====================================================
        # API TOKEN
        # ====================================================

        token = str(
            frappe.conf.get(TOKEN_KEY) or ""
        ).strip()

        if not token:
            raise ValueError(
                f"Missing site_config.json key: {TOKEN_KEY}"
            )

        if token.lower().startswith("apikey "):
            authorization = token
        else:
            authorization = f"ApiKey {token}"

        headers = {
            "Accept": "application/json",
            "Authorization": authorization
        }

        # ====================================================
        # PROCESS EACH BRAND
        # ====================================================

        for brand in BRANDS:

            brand_name = brand["name"]

            stats = {
                "received": 0,
                "created": 0,
                "updated": 0,
                "skipped": 0,
                "failed": 0,
                "pages": 0
            }

            results[brand_name] = stats

            # =================================================
            # GET BRAND API URL
            # =================================================

            api_url = frappe.conf.get(
                brand["config_key"]
            )

            if not api_url:

                stats["failed"] += 1

                debug(
                    brand_name,
                    "CONFIG ERROR",
                    "Missing API URL configuration.",
                    {
                        "config_key": brand["config_key"]
                    }
                )

                continue

            debug(
                brand_name,
                "START",
                "Starting Lead synchronization.",
                {
                    "api_url": api_url,
                    "division": brand["division"]
                }
            )

            try:

                # =============================================
                # PAGINATION
                # =============================================

                for page in range(1, 101):

                    params = {
                        "page": page,
                        "page_size": 25
                    }

                    debug(
                        brand_name,
                        "API REQUEST",
                        f"Fetching page {page}.",
                        params
                    )

                    response = requests.get(
                        api_url,
                        headers=headers,
                        params=params,
                        timeout=30
                    )

                    debug(
                        brand_name,
                        "API RESPONSE",
                        f"Response received for page {page}.",
                        {
                            "status_code": response.status_code
                        }
                    )

                    response.raise_for_status()

                    response_data = response.json()

                    # =========================================
                    # VALIDATE API RESPONSE
                    # =========================================

                    if (
                        not isinstance(response_data, dict)
                        or response_data.get("code") is not True
                        or response_data.get("statusCode") != 200
                    ):
                        raise ValueError(
                            "API returned unsuccessful response "
                            f"on page {page}: "
                            f"{str(response_data)[:500]}"
                        )

                    result = (
                        response_data.get("result") or {}
                    )

                    leads = (
                        result.get("items") or []
                    )

                    pagination = (
                        result.get("pagination") or {}
                    )

                    if not isinstance(leads, list):
                        raise ValueError(
                            "Invalid API items format."
                        )

                    stats["pages"] += 1
                    stats["received"] += len(leads)

                    debug(
                        brand_name,
                        "PAGE DATA",
                        f"Page {page} contains {len(leads)} leads."
                    )

                    # =========================================
                    # PROCESS LEADS
                    # =========================================

                    for lead_data in leads:

                        external_id = ""

                        if isinstance(lead_data, dict):
                            external_id = str(
                                lead_data.get("id") or ""
                            )

                        try:

                            frappe.db.savepoint(
                                "brand_lead_item"
                            )

                            status = create_erp_lead(
                                lead_data,
                                brand=brand,
                                debug=debug
                            )

                            stats[status] += 1

                        except Exception:

                            frappe.db.rollback(
                                save_point="brand_lead_item"
                            )

                            stats["failed"] += 1

                            debug(
                                brand_name,
                                "LEAD ERROR",
                                f"Failed external ID: {external_id}",
                                frappe.get_traceback()
                            )

                    # Save successfully processed leads.
                    frappe.db.commit()

                    # =========================================
                    # CHECK NEXT PAGE
                    # =========================================

                    if not pagination.get("has_next"):

                        debug(
                            brand_name,
                            "PAGINATION",
                            "No more pages."
                        )

                        break

                else:
                    raise ValueError(
                        "Pagination exceeded 100 pages."
                    )

            except Exception:

                stats["failed"] += 1

                debug(
                    brand_name,
                    "BRAND ERROR",
                    "Brand synchronization stopped.",
                    frappe.get_traceback()
                )

            debug(
                brand_name,
                "FINAL RESULT",
                "Brand synchronization completed.",
                stats
            )

    except Exception:

        debug(
            "ALL",
            "FATAL ERROR",
            "Synchronization failed before processing brands.",
            frappe.get_traceback()
        )

        results["error"] = (
            "Configuration or initialization error. "
            "Check Error Log."
        )

    finally:

        # ====================================================
        # FINAL EXECUTION LOG
        # ====================================================

        debug(
            "ALL",
            "END",
            "Lead synchronization execution completed.",
            {
                "start_time": str(started),
                "end_time": str(datetime.now()),
                "results": results
            }
        )

        try:

            frappe.log_error(
                title=(
                    "Doodle & Desert Forest Lead Sync "
                    "- Execution Log"
                ),
                message="\n\n".join(steps)[-60000:]
            )

            frappe.db.commit()

        except Exception:

            frappe.logger(
                "brand_leads"
            ).error(
                "Could not save Lead synchronization log."
            )

    return results


# ============================================================
# CREATE ERPNext LEAD
# ============================================================

def create_erp_lead(lead_data, brand, debug=None):

    brand_name = brand["name"]

    # ========================================================
    # VALIDATE LEAD DATA
    # ========================================================

    if not isinstance(lead_data, dict):
        raise ValueError(
            "Lead item must be a JSON object."
        )

    external_id = str(
        lead_data.get("id") or ""
    ).strip()

    contact_id = str(
        lead_data.get("contact_id") or ""
    ).strip()

    if not external_id:
        raise ValueError(
            "External Lead ID is missing."
        )

    # ========================================================
    # CHECK PREVIOUSLY DELETED LEADS
    # ========================================================

    deleted_record = frappe.db.exists(
        "External Id Document",
        {
            "external_id": external_id
        }
    )

    if deleted_record:

        if debug:
            debug(
                brand_name,
                "SKIPPED",
                f"Previously deleted Lead: {external_id}"
            )

        return "skipped"

    summary = str(
        lead_data.get("summary") or ""
    ).strip()

    if not contact_id:

        if debug:
            debug(
                brand_name,
                "SKIPPED",
                f"Contact ID missing: {external_id}"
            )

        return "skipped"

    # First check by Contact ID
    existing_lead = frappe.db.get_value(
        "Lead",
        {
            CONTACT_ID_FIELD: contact_id
        },
        ["name", "custom_summary"],
        as_dict=True
    )

    # Fallback: check External Lead ID
    # for records created before Contact ID was added
    if not existing_lead:

        existing_lead = frappe.db.get_value(
            "Lead",
            {
                EXTERNAL_ID_FIELD: external_id
            },
            ["name", "custom_summary"],
            as_dict=True
        )

        if existing_lead:

            # Populate missing Contact ID
            existing_contact_id = frappe.db.get_value(
                "Lead",
                existing_lead.name,
                CONTACT_ID_FIELD
            )

            if (
                existing_contact_id
                and existing_contact_id != contact_id
            ):
                raise ValueError(
                    "External Lead ID already belongs to "
                    f"another Contact ID: {existing_contact_id}"
                )

            if not existing_contact_id:

                frappe.db.set_value(
                    "Lead",
                    existing_lead.name,
                    CONTACT_ID_FIELD,
                    contact_id
                )

    # Update existing Lead summary
    if existing_lead:

        old_summary = (
            existing_lead.custom_summary or ""
        ).strip()

        if summary != old_summary:

            frappe.db.set_value(
                "Lead",
                existing_lead.name,
                "custom_summary",
                summary
            )

            if debug:
                debug(
                    brand_name,
                    "UPDATED",
                    f"Lead summary updated: {existing_lead.name}"
                )

            return "updated"

        if debug:
            debug(
                brand_name,
                "SKIPPED",
                f"Lead already exists: {existing_lead.name}"
            )

        return "skipped"


    # ========================================================
    # EXTRACT API VALUES
    # ========================================================

    first_name = str(
        lead_data.get("first_name") or ""
    ).strip()

    last_name = str(
        lead_data.get("last_name") or ""
    ).strip()

    phone_number = str(
        lead_data.get("phone_number") or ""
    ).strip()

    email = str(
        lead_data.get("email") or ""
    ).strip()

    summary = str(
        lead_data.get("summary") or ""
    ).strip()

    stage = str(
        lead_data.get("stage") or ""
    ).strip()

    created_at = lead_data.get("created_at")
    updated_at = lead_data.get("updated_at")

    # ========================================================
    # GENERATE LEAD NAME
    # ========================================================

    lead_name = " ".join(
        value
        for value in [
            first_name,
            last_name
        ]
        if value
    )

    if not lead_name:
        lead_name = (
            phone_number
            or f"{brand_name} Lead"
        )

    if not first_name:
        first_name = lead_name

    # ========================================================
    # CREATE LEAD DOCUMENT
    # ========================================================

    lead = frappe.new_doc("Lead")

    lead.first_name = first_name

    if last_name:
        lead.last_name = last_name

    lead.lead_name = lead_name

    if phone_number:
        lead.mobile_no = phone_number

    if email:
        lead.email_id = email

    lead.custom_summary = summary
    lead.custom_services = "Others"
    lead.source = "Desert Forest"

    # External API Lead ID
    lead.set(
        EXTERNAL_ID_FIELD,
        external_id
    )

    # External API Contact ID
    lead.set(
        CONTACT_ID_FIELD,
        contact_id
    )

    # ========================================================
    # DIVISION ASSIGNMENT
    # ========================================================

    # Doodle: division remains unset.
    # Desert Forest: assign configured division.

    if brand["division"]:

        lead.set(
            DIVISION_FIELD,
            brand["division"]
        )

    # ========================================================
    # LEAD SOURCE
    # ========================================================

    if frappe.db.exists(
        "Lead Source",
        "Website"
    ):
        lead.source = "Website"

    # ========================================================
    # INSERT LEAD
    # ========================================================

    lead.insert(
        ignore_permissions=True
    )

    if debug:

        debug(
            brand_name,
            "LEAD CREATED",
            f"Lead created successfully: {lead.name}",
            {
                "external_id": external_id,
                "contact_id": contact_id,
                "brand": brand_name,
                "division": brand["division"]
            }
        )

    # ========================================================
    # EMAIL NOTIFICATION
    # ========================================================

    try:

        lead_url = (
            f"{frappe.utils.get_url()}"
            f"/app/lead/{quote(lead.name, safe='')}"
        )

        message = f"""
            <p>
                A new lead has been created from
                {escape(brand_name)}.
            </p>

            <p>
                <b>Lead:</b>
                {escape(lead.lead_name or "")}<br>

                <b>Lead ID:</b>
                {escape(lead.name)}<br>

                <b>First Name:</b>
                {escape(lead.first_name or "")}<br>

                <b>Last Name:</b>
                {escape(lead.last_name or "")}<br>

                <b>Mobile:</b>
                {escape(lead.mobile_no or "")}<br>

                <b>Source:</b>
                {escape(lead.source or "")}<br>

                <b>Email:</b>
                {escape(lead.email_id or "")}<br>

                <b>Summary:</b>
                {escape(lead.custom_summary or "")}
            </p>

            <p>
                <a href="{escape(lead_url, quote=True)}">
                    Open Lead
                </a>
            </p>
        """

        recipients = list(NOTIFY)
        if lead.get(DIVISION_FIELD) == "Doodle Desert Forest - DTL":
            recipients.extend(DESERT_FOREST_ADDITIONAL_NOTIFY)

        frappe.sendmail(
            recipients=recipients,
            subject=(
                f"New {brand_name} Lead Created "
                f"- {lead.lead_name}"
            ),
            message=message,
            delayed=True
        )

        if debug:

            debug(
                brand_name,
                "EMAIL",
                f"Notification queued for {lead.name}"
            )

    except Exception:

        if debug:

            debug(
                brand_name,
                "EMAIL ERROR",
                f"Notification failed for {lead.name}",
                frappe.get_traceback()
            )

    return "created"
