import frappe

def execute():
    if frappe.db.get_value("Global Defaults", None, "default_company") != 'Sea-fire Europe Ltd.':
        print('This patch only applies to Sea-fire Europe Ltd.')
        return
    # customers = get_foreign_currency_customers()
    default_account = frappe._dict()
    default_account.EUR = frappe.get_value("Account", {"account_name": 'Debtors EUR'})
    default_account.USD = frappe.get_value("Account", {"account_name": 'Debtors USD'})
    default_account.GBP = frappe.get_value("Account", {"account_name": 'Debtors GBP'})
    customers = [{"name": "Seebo Handel GMBH", "currency": "EUR", 'vat_code': 'T4', "price_list": "2019-05 EUR Sea-Fire Suggested Retail Price List"},
    	{"name": "Powerboat Center CO.", "currency": "USD", 'vat_code': 'T0', 'price_list': '2019-05 USD Sea-Fire Suggested Retail Price List'},
    	{"name": "Metalcraft Inc.", "currency": "USD", 'vat_code': 'T0'},
    	{"name": "Marine Works", "currency": "USD", 'vat_code': 'T4', 'price_list': '2019-05 USD Sea-Fire Suggested Retail Price List'},
    	{"name": "TWO OCEANS MARINE", "currency": "USD", 'vat_code': 'T0'},
    	{"name": "Alter Baltics OU", "currency": "EUR", 'vat_code': 'T4', "price_list": "2019-05 EUR Sea-Fire Suggested Retail Price List"},
    	{"name": "Abakus Europe", "currency": "GBP", 'vat_code': 'T4'},
    	{"name": "Ten Napel Brandbeveiliging", "currency": "EUR", "price_list": "2019-05 EUR Sea-Fire Suggested Retail Price List"},
    	{"name": "Stephen Attard", "currency": "GBP", 'vat_code': 'T1', "price_list": "2019-05 GBP Sea-Fire Suggested Retail Price List"},
    	{"name": "Richard Cain", "currency": "GBP", 'vat_code': 'T1', "price_list": "2019-05 GBP Sea-Fire Suggested Retail Price List"},
    	{"name": "Neil Wood", "currency": "GBP", 'vat_code': 'T1', "price_list": "2019-05 GBP Sea-Fire Suggested Retail Price List"},
    	{"name": "Nautikos México", "currency": "USD", 'vat_code': 'T0', 'price_list': '2019-05 USD Sea-Fire Suggested Retail Price List'},
    	{"name": "MY ZEMBRA Ltd", "currency": "EUR", 'vat_code': 'T4', "price_list": "2019-05 EUR Sea-Fire Suggested Retail Price List"},
    	{"name": "PFC Marine Ltd", "currency": "GBP", 'vat_code': 'T1', 'price_list': "2019-05 GBP Sea-Fire Suggested Retail Price List"},
    	{"name": "Princess Yachts Limited", "currency": "USD", 'vat_code': 'T1', 'price_list': "2019-05 USD Sea-Fire Suggested Retail Price List"},
    	{"name": "RF Composites LTD", "currency": "GBP", 'vat_code': 'T1', 'price_list': "2019-05 GBP Sea-Fire Suggested Retail Price List"}]
    for customer in customers:
        patch_entries_in_wrong_currency(default_account, customer)
    # clean up stragglers
    frappe.db.set_value('Sales Invoice', '40442', 'debit_to', '1111 - Debtors EUR - SFE')
    frappe.db.set_value('Sales Invoice', '40412', 'debit_to', '1111 - Debtors EUR - SFE')
    frappe.db.set_value('Sales Invoice', '40017', 'debit_to', '1111 - Debtors EUR - SFE')

def get_foreign_currency_customers():
    cust = frappe.get_list("Customer", {'default_currency': ['!=', "GBP"]}, ["name", "default_currency"])
    return cust

def patch_entries_in_wrong_currency(default_account, customer):
    print(customer['name'])
    gl_entries = [gl["name"] for gl in frappe.get_list("GL Entry", {'party': customer["name"]})]
    for entry in gl_entries:
        entry = frappe.get_doc('GL Entry', entry)
        print(entry.account, default_account.get(customer['currency']))
        if entry.account != default_account.get(customer['currency']):
            print('Setting account to ' + default_account.get(customer['currency']))
            frappe.db.set_value("GL Entry", entry.name, 'account', default_account.get(customer['currency']))
            frappe.db.set_value("GL Entry", entry.name, 'account_currency', customer['currency'])
            print(entry.voucher_type, entry.voucher_no)
            if entry.voucher_no and entry.voucher_type == "Sales Invoice":
                print("setting " + entry.voucher_type + " " + entry.voucher_no + " debit_to to " + default_account.get(customer['currency']) )
                frappe.db.set_value(entry.voucher_type, entry.voucher_no, 'debit_to', default_account.get(customer['currency']))



def check_unmatched_transactions():
    customers = get_foreign_currency_customers()
    for customer in customers:
        gl_entries = [gl["name"] for gl in frappe.get_list("GL Entry", {'party': customer["name"], 'account_currency': ['!=', customer['default_currency']]})]
        if len(gl_entries) > 0:
            for entry in gl_entries:
                entry = frappe.get_doc('GL Entry', entry)
                print(entry.name, entry.party, entry.account_currency, customer['default_currency'])
