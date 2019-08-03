# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "metalcraft"
app_title = "Metalcraft"
app_publisher = "Metalcraft, Inc."
app_description = "Metalcraft, Inc. internal app for customizations."
app_icon = "fa fa-fire-extinguisher"
app_color = "red"
app_email = "cpurbaugh@sea-fire.com"
app_license = "MIT"

# Includes in <head>
# ------------------


# include js, css files in header of desk.html
# app_include_css = "/assets/metalcraft/css/metalcraft.css"
app_include_js = "/assets/js/metalcraft.min.js"

# website_context = {
#     "favicon": "/files/favicon.ico",
#     "splash_image": "http://www.sea-fire.com/wp-content/uploads/2012/07/copy-seafireLogo.png"
# }


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

# Jinja Filters
# ---------------
# Methods accessible to print template
jenv = {
    "methods": [
    'get_qrcode:metalcraft.jinja_filters.get_qrcode'
    ]
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Delivery Note": {
		"validate": "metalcraft.validations.check_serials_in_draft",
		# "validate": "metalcraft.validations.check_batch_qty",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
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
# 	],
    "cron": {
        "0,5,11,17,23,29,35,41,47,53 * * * *": [
          "erpnext.stock.reorder_item.reorder_item"
        ]
    }
#
# 	]
}

# Testing
# -------

# before_tests = "metalcraft.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "metalcraft.event.get_events"
# }
