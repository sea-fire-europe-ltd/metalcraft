# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "metalcraft"
app_title = "Metalcraft"
app_publisher = "Metalcraft"
app_description = "app for customizations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "cpurbaugh@sea-fire.com"
app_license = "MIT"

# Includes in <head>
# ------------------

@frappe.whitelist()
def attach_all_docs(document, method=None):
    """This function attaches drawings to the purchase order based on the items being ordered"""
    document = json.loads(document)

    current_attachments = []
    for file_url in frappe.db.sql("""select file_url from `tabFile` where attached_to_doctype = %(doctype)s and     attached_to_name = %(docname)s""", {'doctype': document["doctype"], 'docname': document["name"]}, as_dict=True ):
        current_attachments.append(file_url.file_url)
        count = 0
        for item_doc in document["items"]:
            #frappe.msgprint(item_doc)
            # Check to see if the quantity is = 1
            item = frappe.get_doc("Item",item_doc["item_code"])

            attachments = []
            # Get the path for the attachments
            if item.drawing_attachment:
                attachments.append(item.drawing_attachment)
            if item.stp_attachment:
                attachments.append(item.stp_attachment)
            if item.dxf_attachment:
                attachments.append(item.dxf_attachment)
            if item.x_t_attachment:
                attachments.append(item.x_t_attachment)

            for attach in attachments:
                # Check to see if this file is attached to the one we are looking for
                if not attach in current_attachments:
                    count = count + 1
                    save_url(attach, document["doctype"], document["name"], "Home/Attachments")
    frappe.msgprint("Attached {0} files".format(count))

# include js, css files in header of desk.html
# app_include_css = "/assets/metalcraft/css/metalcraft.css"
# app_include_js = "/assets/metalcraft/js/metalcraft.js"

# include js, css files in header of web template
# web_include_css = "/assets/metalcraft/css/metalcraft.css"
# web_include_js = "/assets/metalcraft/js/metalcraft.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "metalcraft.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "metalcraft.install.before_install"
# after_install = "metalcraft.install.after_install"


# Fixtures
# --------
fixtures = ["Custom Field", "Custom Script"]

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "metalcraft.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"metalcraft.tasks.all"
# 	],
# 	"daily": [
# 		"metalcraft.tasks.daily"
# 	],
# 	"hourly": [
# 		"metalcraft.tasks.hourly"
# 	],
# 	"weekly": [
# 		"metalcraft.tasks.weekly"
# 	]
# 	"monthly": [
# 		"metalcraft.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "metalcraft.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "metalcraft.event.get_events"
# }

