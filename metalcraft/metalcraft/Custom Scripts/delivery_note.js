//------------------------------------------------------------------------------START OF DELIVERY NOTE CODE
cur_frm.add_fetch('customer', 'sps', 'sps');

frappe.ui.form.on("Delivery Note", {
	onload: function(frm){
		if (frm.doc.__islocal) {
			frm.set_value("accounting_contacted", 0);
	}
},
	refresh: function(frm) {
		if( frm.doc.delivery_note_workflow_state === "Shipped") {
			if(frm.doc.docstatus === 0) {
				frm.set_value("delivery_note_workflow_state", "Needs Review");
			frm.save();
			location.reload();
			}
		}
	},
  validate: function(frm) {
    str = "SPS Commerce";
    link = str.link("http://commerce.spscommerce.com/auth/login/");
    if ( frm.doc.sps) {
      if (user_roles.indexOf("Shipping User")!== -1) {
        msgprint("Customer uses SPS. An ASN must be completed for the shipment in " + link);
      }
    }
  }
});

//++++++++++++++++++++++++++++++++++++++++++++++++++++++END OF SPS CUSTOM SCRIPT
frappe.ui.form.on("Delivery Note", {
	refresh: function(frm) {
		if (frm.doc.customer) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Customer",
					filters: {
						name: frm.doc.customer
					},
					fieldname: ["credit_limit"]
				},
				callback: function(r) {
					credit_limit = r.message.credit_limit;
				}
			});
			frappe.call({
				method: "erpnext.accounts.utils.get_balance_on",
				args: {
					party_type: "Customer",
					party: cur_frm.doc.customer
				},
				callback: function(r) {
					if(r.message == null){
						accounts_receivable = 0;
					} else {
					accounts_receivable = r.message;
				}
			}
			});
		if (!frm.doc.__islocal) {
			
			frappe.call({
				"method": "frappe.client.get_value",
				"args": {
					"doctype": "Customer",
					"filters": {
						"name": frm.doc.customer
					},
					"fieldname": "on_hold"
				},
				callback: function(r) {
					frm.set_value("so_on_hold", r.message.on_hold);
					console.log(r.message.on_hold);
				}
			});
		}
	}
	},
	so_on_hold: function(frm) {
		if (frm.doc.so_on_hold !== 0 && frm.doc.delivery_note_workflow_state !== ("In Process" || "Packing Complete")) {
			msgprint("This customer is on credit hold.  This order will not be able to be advanced past the Packing Complete status.");
		}
		if (frm.doc.so_on_hold === 0 && !frm.doc.__islocal) {
			msgprint("This customer has been cleared.");
		}
	},
	validate: function(frm) {
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Customer",
				filters: {
					name: frm.doc.customer
				},
				fieldname: ["credit_limit"]
			},
			callback: function(r) {
				credit_limit = r.message.credit_limit;
				console.log("Credit Limit: " + r.message.credit_limit );
			}
		});
		frappe.call({
			method: "erpnext.accounts.utils.get_balance_on",
			args: {
				party_type: "Customer",
				party: cur_frm.doc.customer
			},
			callback: function(r) {
				if(r.message == null){
					accounts_receivable = 0;
				} else {
				accounts_receivable = r.message;
			}
		}
		});



		if(!frm.doc.__islocal) {
			if (frm.doc.so_on_hold) {
				msgprint("Customer is on hold.");
				if (frm.doc.workflow_state !== "Draft") {
					msgprint("This order cannot be advanced.");
					validated = false;
				}
			}	else {
				if (!frm.doc.accounting_contacted) {
				if (credit_limit === 0) {
					console.log("credit limit === 0, function aborted.");
				} else if (accounts_receivable > credit_limit) {
					console.log("AR > CL");
					msgprint("This customer has exceeded their credit limit.  Accounting has been contacted to place this customer on credit hold.");
					doc = {
						"doctype": "Communication",
						"subject": ("@Accounting Customer " + frm.doc.customer + " has exceeded their credit limit.  Please place on hold if necessary."),
						"content": ("@Accounting Customer " + frm.doc.customer + " has exceeded their credit limit.  Please place on hold if necessary."),
						"communication_type": "Comment",
						"reference_doctype": "Delivery Note",
						"reference_name": frm.doc.name,
						"reference_owner": "Administrator",
						"purchase_order": frm.doc.name,
						"user": "Administrator"
					};
					frappe.call({
						"method": "frappe.client.insert",
						"args": {
							"doc": doc
						}
					});
					frm.set_value("accounting_contacted",1);
				} else if (accounts_receivable + frm.doc.grand_total > credit_limit) {
					console.log("AR + GT > CL");
					msgprint("This customer will exceed their credit limit if this order is shipped. Accounting has been contacted to place this customer on credit hold.");
					doc = {
						"doctype": "Communication",
						"subject": ("@Accounting Customer " + frm.doc.customer + " will exceed their credit limit if this order is shipped.  Please place on hold if necessary."),
						"content": ("@Accounting Customer " + frm.doc.customer + " will exceed their credit limit if this order is shipped.  Please place on hold if necessary."),
						"communication_type": "Comment",
						"reference_doctype": "Delivery Note",
						"reference_name": frm.doc.name,
						"reference_owner": "Administrator",
						"purchase_order": frm.doc.name,
						"user": "Administrator"
					};
					frappe.call({
						"method": "frappe.client.insert",
						"args": {
							"doc": doc
						}
					});
				frm.set_value("accounting_contacted",1);
				} else {
					console.log("something else? Credit Limit: " + credit_limit + " Grand Total: " + frm.doc.grand_total + " AR: " + accounts_receivable);
				}
		}
	}
	}
  }});
