
credit_limit = 0;
accounts_receivable = 0;
cur_frm.add_fetch('code', 'description', 'description');
cur_frm.add_fetch('customer', 'on_hold', 'so_on_hold');
cur_frm.add_fetch('customer', 'sps', 'sps');
cur_frm.add_fetch('customer', 'payment_terms1', 'payment_terms1');

//Custom warning messages
frappe.ui.form.on("Sales Order", {
	validate: function(frm) {
		if (frm.doc.customer == "Phoenix Boats") {
			msgprint("ATTENTION: VERIFY ORDER INPUT AND INSPECT PHYSICAL SHIPMENT PRIOR TO RELEASE.");
		} if (frm.doc.grand_total < 20.00) {
			msgprint("Minimum Order Value Not Met:  Grand total of order should not fall below $20 USD, unless warranted.  Please adjust pricing to bring order total to $20 USD or more.");
		}	if (frm.doc.customer == "Grainger Sourcing") {
			msgprint("Grainger orders require a custom packing list. Please include the custom packing list as an attachment to the SO");
		}
	},
	on_save: function(frm) {
		if (frm.doc.customer == "Phoenix Boats") {
			msgprint("ATTENTION: VERIFY ORDER INPUT AND INSPECT PHYSICAL SHIPMENT PRIOR TO RELEASE.");
		} if (frm.doc.customer == "Grainger Sourcing") {
			msgprint("Grainger orders require a custom packing list. Please include the custom packing list as an attachment to the SO");
		}	if (frm.doc.grand_total < 20.00) {
			msgprint("Minimum Order Value Not Met:  Grand total of order should not fall below $20 USD, unless warranted.  Please adjust pricing to bring order total to $20 USD or more.");
	}
}
});


frappe.ui.form.on("Sales Order", {
	onload: function(frm) {
		frm.refresh_field("customer");
		//------------------------------------------------------------------------------Clears checkboxes on amended orders
		if (frm.doc.__islocal) {
			frm.set_value("printed_by_preengineered_systems", "");
			frm.set_value("printed_by_engineered_systems", "");
			frm.set_value("printed_by_electronic_systems", "");
			frm.set_value("printed_by_portable_systems", "");
		}
		//------------------------------------------------------------------------------Hides pricing for non-customer support personnel
		if (user_roles.indexOf("Sales User") === -1) {
			frm.fields_dict["items"].grid.set_column_disp("rate", false);
			frm.fields_dict["items"].grid.set_column_disp("amount", false);
			frm.fields_dict["items"].grid.set_column_disp("base_amount", false);
			frm.fields_dict["items"].grid.set_column_disp("price_list_rate", false);
			frm.fields_dict["items"].grid.set_column_disp("base_price_list_rate", false);
			frm.fields_dict["items"].grid.set_column_disp("discount_and_margin", false);
			frm.fields_dict["items"].grid.set_column_disp("section_break_simple1", false);
			frm.fields_dict["items"].grid.set_column_disp("section_break_24", false);
			frm.fields_dict["items"].grid.set_column_disp("billed_amt", false);
			frm.fields_dict["items"].grid.set_column_disp("valuation_rate", false);
			frm.fields_dict["items"].grid.set_column_disp("gross_profit", false);
			frm.fields_dict["items"].grid.set_column_disp("item_tax_rate", false);
			frm.set_df_property("items", "hidden", 1);
			frm.set_df_property("totals", "hidden", 1);
			frm.set_df_property("total", "hidden", 1);
			frm.set_df_property("base_total", "hidden", 1);
			frm.set_df_property("grand_total", "hidden", 1);
			frm.set_df_property("rounded_total", "hidden", 1);
			frm.set_df_property("base_in_words", "hidden", 1);
			frm.set_df_property("base_grand_total", "hidden", 1);
			frm.set_df_property("taxes_section", "hidden", 1);
			frm.set_df_property("sales_team_section_break", "hidden", 1);
			frm.refresh_field("items");
		}
	},
	delivery_date: function(frm) { frm.set_value("scheduled_ship_date", frm.doc.delivery_date); }, //Updates Scheduled Ship Date to Delivery Date
  validate: function(frm) {
		frm.set_value("scheduled_ship_date", frm.doc.delivery_date); //Updates scheduled ship date to match delivery date (same as line 45, but for validation)
		frm.doc.items.forEach(function(d) {d.warehouse = "Shipping - MC";}); //Updates all item's warehouse to 'Shipping - MC'
		pes = ["SeaFire", "Cables", "O-Ring", "FD Line", "FG Line", "Loctite", "MD Line", "MG Line", "C-Models", "Fire Foe", "Hardware", "NFD Line", "NFG Line", "NMD Line", "NMG Line", "Cylinders", "Automatics", "FT Stinger", "Stock Item", "Race Systems", "Miscellaneous", "Obsolete Items", "Sub Assemblies", "Agent and Gases", "All Item Groups", "Novec1230 Automatics", "Pre-Engineered Systems", "Dry Chemical Fire Extinguishers", "Consumables", "Accessories"];
		eng = ["M/MN Series", "Engineered Systems"];
		ele = ["Electronic Systems"];
		por = ["HHFE", "Mil-E", "C-Models", "CO2 Steel", "CO2 Aluminium", "Portable Systems", "Potassium Acetate"];
		var ig = [];
		var count = frm.doc.items.length;

		for (i = 0; i < count; i++) {
			ig.push(frm.doc.items[i].item_group);
			console.log(ig);
		}
		for (i = 0; i < pes.length; i++) {
			for (j = 0; j < ig.length; j++) {
				if (ig[j] === pes[i]) {
					frm.set_value("pes_email_alert", -1);
				}
			}
		}
		for (i = 0; i < por.length; i++) {
			for (j = 0; j < ig.length; j++) {
				if (ig[j] === por[i]) {
					frm.set_value("por_email_alert", -1);
				}
			}
		}
		for (i = 0; i < ele.length; i++) {
			for (j = 0; j < ig.length; j++) {
				if (ig[j] === ele[i]) {
					frm.set_value("ele_email_alert", -1);
				}
			}
		}
		for (i = 0; i < eng.length; i++) {
			for (j = 0; j < ig.length; j++) {
				if (ig[j] === eng[i]) {
					frm.set_value("eng_email_alert", -1);
				}
			}
		}
	}
});
//If modifications need to be made, be sure to update Delivery Note as well.

caller = function() {

}
frappe.ui.form.on("Sales Order", {
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
		if (frm.doc.so_on_hold !== 0) {
			msgprint("This customer is on credit hold.  This order will not be able to be advanced past the Draft status.");
		}
		if (frm.doc.so_on_hold === 0) {
			if(frm.doc.__islocal) {
				console.log("Customer is clear");
			} else {
				msgprint("This customer has been cleared.");
			}
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
				if (frm.doc.sales_order_workflow_state !== "Draft") {
          frm.set_value("sales_order_workflow_state","Credit Hold")

				}
			}	else {
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
						"reference_doctype": "Sales Order",
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
				} else if (accounts_receivable + frm.doc.grand_total > credit_limit) {
					console.log("AR + GT > CL");
					msgprint("This customer will exceed their credit limit if this order is shipped. Accounting has been contacted to place this customer on credit hold.");
					doc = {
						"doctype": "Communication",
						"subject": ("@Accounting Customer " + frm.doc.customer + " will exceed their credit limit if this order is shipped.  Please place on hold if necessary."),
						"content": ("@Accounting Customer " + frm.doc.customer + " will exceed their credit limit if this order is shipped.  Please place on hold if necessary."),
						"communication_type": "Comment",
						"reference_doctype": "Sales Order",
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
				} else {
					console.log("something else? Credit Limit: " + credit_limit + " Grand Total: " + frm.doc.grand_total + " AR: " + accounts_receivable);
				}
		}
	}
	}
});

//------------------------------------------------------------------------------
// Custom script by request by Steve Ellis Jr.
// Original Email:
// Chris,
//
// I need a pop-up message on the sales order.
// If PN 212-396 or 212-397 is entered following pop-up message on save:
//
// PN 212-396 is FD375 CE.
// PN 212-397 is FD400 CE.
// Please see Steve Ellis Jr. before processing order.
//
// Thanks,
// Steve

frappe.ui.form.on("Sales Order Item", {
  item_code: function(frm,cdt,cdn){
    var d = locals[cdt][cdn];
    var msg = "PN 212-396 is FD375 CE <br> PN 212-397 is FD400 CE<br><br>Please see Steve Ellis Jr. before processing order";
    if(d.item_code === "212-396") {
      msgprint(msg);
    }
    if(d.item_code === "212-397") {
      msgprint(msg);
    }
  }
});

// End of custom script for Steve Ellis Jr.
//Created by Christopher G. Purbaugh
//Created on 2019-02-11
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
// Custom script for custom RMA doctype and table

frappe.ui.form.on("Sales Order", "rma", function(frm) {
    frappe.model.with_doc("Return Material Authorization", frm.doc.rma, function() {
        var tabletransfer= frappe.model.get_doc("Return Material Authorization", frm.doc.rma);
        $.each(tabletransfer.items, function(index, row){
            d = frm.add_child("rma_table");
            d.rma_item_code = row.rma_item_code;
			console.log(d.rma_item_code);
            d.description = row.description;
            d.qty = row.qty;
            cur_frm.refresh_field("rma_table");
        });
    });
});
cur_frm.set_query("rma", function () {
    return{
        filters: { 'customer': cur_frm.doc.customer }
    }
});

// End of custom script for custom RMA doctype and table
//Created by Christopher G. Purbaugh
//Created on 2019-02-11
//------------------------------------------------------------------------------
