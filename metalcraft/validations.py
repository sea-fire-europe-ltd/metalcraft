import frappe
import re

def check_serials_in_draft(doc, method):
    # check to see if current items are serialized
    print("!!!!! serials !!!!!")
    serial_items = any([row.serial_no for row in doc.items])
    if not serial_items:
        print("no serialized items")
        return
    # get serial numbers in current document
    sns_in_doc = []
    for row in doc.items:
        if not row.serial_no:
            continue
        elif row.serial_no:
            row_sns = [s.strip() for s in row.serial_no.split("\n")]
            sns_in_doc.extend(row_sns)
    # get serial numbers from open documents
    oustanding_sns = frappe.get_list("Delivery Note Item", filters={"docstatus": 0}, fields=["serial_no", "parent"])
    for sn in oustanding_sns:
        if sn["serial_no"] and sn["parent"] and doc.name != sn["parent"]:
            sn["serial_no"] = [s.strip() for s in sn["serial_no"].split("\n") if s not in ["", "\n", None]]
            print("dn", sn["parent"], "serial number ", sn["serial_no"])
    # check open documents against this document
    sns_in_use = []
    for dn in oustanding_sns:
        if not dn["serial_no"]:
            continue
        for sn in dn["serial_no"]:
            if sn in sns_in_doc:
                sns_in_use.append({"dn": dn["parent"], "sn": sn})
    if sns_in_use:
        dns_in_use =  "".join(["\xa0 \xa0 \xa0 \xa0" + use["dn"] + ": " + use["sn"] + "<br>" for use in sns_in_use])
        frappe.msgprint("The following serial numbers are already in use: <br>" + dns_in_use,
            title="Serial Number in Use", raise_exception=1, indicator='red')


def check_batch_qty(doc, method):
    pass
