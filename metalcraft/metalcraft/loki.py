from __future__ import unicode_literals

import frappe
import os, base64
from frappe import _, throw
from frappe.utils import flt
from frappe.utils.file_manager import save_url, save_file, get_file_name
from frappe.utils import get_site_path, get_files_path, random_string, encode
from frappe.utils import cstr, flt, getdate, new_line_sep, nowdate, add_days
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_indented_qty
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.production_order.production_order import get_item_details

from six import string_types

import json

@frappe.whitelist()
def make_stock_entry_receipt(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		qty = flt(flt(obj.stock_qty) - flt(obj.ordered_qty))/ target.conversion_factor \
			if flt(obj.stock_qty) > flt(obj.ordered_qty) else 0
		target.qty = qty
		target.transfer_qty = qty * obj.conversion_factor
		target.conversion_factor = obj.conversion_factor
		target.t_warehouse = obj.warehouse

	def set_missing_values(source, target):
		target.purpose = source.material_request_type
		target.run_method("calculate_rate_and_amount")

	doclist = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["in", ["Material Receipt"]]
			}
		},
		"Material Request Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "material_request_item",
				"parent": "material_request",
				"uom": "stock_uom",
			},
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

	return doclist
