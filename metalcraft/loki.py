from frappe.utils import get_site_path, get_files_path, random_string, encode
import json


@frappe.whitelist()
def attach_all_docs(document, method=None):
    """This function attaches drawings to the purchase order based on the items
    being ordered"""
document = json.loads(document)

current_attachments = []
for file_url in frappe.db.sql("""select file_url from `tabFile` where
                                  attached_to_doctype = %(doctype)s and
                                   attached_to_name = %(docname)s""", {
                                       'doctype': document["doctype"],
                                       'docname': document["name"]
                                       }, as_dict=True):
        current_attachments.append(file_url.file_url)
        count = 0
        for item_doc in document["items"]:
            # frappe.msgprint(item_doc)
            # Check to see if the quantity is = 1
            item = frappe.get_doc("Item", item_doc["item_code"])

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
                # Check to see if this file is attached to the one we are
                # looking for
                if attach not in current_attachments:
                    count = count + 1
                    save_url(attach, document["doctype"], document[
                             "name"], "Home/Attachments")
frappe.msgprint("Attached {0} files".format(count))


@frappe.whitelist()
def attach2(document):
    """This function attaches drawings
     to the purchase order based on
     the items being ordered"""
    document = json.loads(document)
    document2 = frappe._dict(document)

    current_attachments = []

    for file_url in frappe.db.sql("""select file_url from `tabFile` where
                                  attached_to_doctype = %(doctype)s and
                                  attached_to_name = %(docname)s""", {
                                    'doctype': document2.doctype,
                                    'docname': document2.name
                                    }, as_dict=True):
        current_attachments.append(file_url.file_url)

    # add the directly linked drawings
    items = []
    for item in document["items"]:
        # frappe.msgprint(str(item))
        items.append(item["item_code"])

        # add the child documents (from boms)
        items = add_bom_items(items, item["item_code"])

    count = 0
    for item_doc in items:
        # frappe.msgprint(item_doc)
        item = frappe.get_doc("Item", item_doc)

        attachments = []
        # Get the path for the attachments
        if item.drawing_attachment:
            attachments.append(item.drawing_attachment)

        for attach in attachments:
            # Check to see if this file is attached to the one we are looking
            # for
            if attach not in current_attachments:
                count = count + 1
                myFile = save_url(attach, attach, document2.doctype,
                                  document2.name, "Home/Attachments")
                myFile.file_name = attach
                myFile.save()
                current_attachments.append(attach)

    frappe.msgprint("Attached {0} files".format(count))
