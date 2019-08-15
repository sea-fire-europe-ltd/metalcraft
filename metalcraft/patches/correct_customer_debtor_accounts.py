import frappe
from frappe.contacts.doctype.address.address import get_default_address

countries_in_europe = ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City']

outliers = customers = [{"name": "Seebo Handel GMBH", "currency": "EUR", 'vat_code': 'T4', "price_list": "2019-05 EUR Sea-Fire Suggested Retail Price List"},
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

def execute():
	if frappe.db.get_value("Global Defaults", None, "default_company") != 'Sea-fire Europe Ltd.':
		print('This patch only applies to Sea-fire Europe Ltd.')
		return
	default_account = frappe._dict()
	default_account.EUR = frappe.get_value("Account", {"account_currency": 'EUR', 'account_type': 'Receivable'})
	default_account.USD = frappe.get_value("Account", {"account_currency": 'USD', 'account_type': 'Receivable'})
	default_account.GBP = frappe.get_value("Account", {"account_name": 'Debtors GBP'})
	customers = get_foreign_currency_customers()
	unknown = []
	for customer in customers:
		if customer['default_currency'] not in ["EUR", "USD"] or customer['default_currency'] == None:
			unknown.append(customer)
			customers.remove(customer)
	if unknown:
		print("The following customer currencies must be corrected")
		for un in unknown:
			print(str(un['default_currency']) + " for " + un['name'] + "/" + un['territory'])

	print("\nCorrecting customer currency accounts")
	for customer in customers:
		correct_account(default_account, customer)
		print("Correcting account for " + customer['name'] + " to " + str(customer['default_currency']))

def get_foreign_currency_customers():
	cust = frappe.get_list("Customer", {'default_currency': ['!=', "GBP"]}, ["name", "default_currency", "territory"])
	return cust

def correct_account(default_account, customer):
	if customer['name'] in [o['name'] for o in outliers]:
		customer = [c for c in outliers if c['name'] == customer['name']][0]
	cust = frappe.get_doc("Customer", customer['name'])
	cust.vat_code_customer, cust.default_currency = get_vat_code(cust)
	cust.vat_code_customer = customer.get('vat_code') if customer.get('vat_code') else cust.vat_code_customer
	currency = customer.get('currency') if customer.get('currency') else cust.default_currency
	cust.default_currency = currency
	cust.accounts = []

	cust.append('accounts', {
		'company': 'Sea-fire Europe Ltd.',
		'account': default_account.get(currency)
	})

	cust.default_price_list = customer.get("price_list") if customer.get("price_list") else cust.default_price_list
	try:
		cust.save(ignore_permissions=True)
	except Exception as e:
		print('error correcting ' + customer['name'] + "\n" + str(e))


def get_vat_code(customer):
	address = get_default_address('Customer', customer.name)
	if address:
		country = frappe.get_value('Address', address, 'country')
		if country not in {'United Kingdom', 'United States'} and country in countries_in_europe:
			customer.default_currency = 'EUR' if not customer.default_currency else customer.default_currency
			return 'T4', customer.default_currency
		elif country == 'United Kingdom':
			return 'T1', 'GBP'
		elif country == 'United States':
			return 'T0', 'USD'
	if not customer.territory and not customer.vat_code_customer and not customer.default_currency:
		print('more information is required about ' + cust.name)
		return '', 'GBP'
	if customer.default_currency == 'USD':
		return 'T0', 'USD'
	elif customer.default_currency == 'EUR':
		return 'T4', 'EUR'
	elif customer.default_currency == 'GBP':
		return 'T1', 'GBP'


def get_address(customer_name):
	addy = frappe.db.sql("""
		SELECT `tabAddress`.name
		FROM `tabAddress`, `tabDynamic Link`
		WHERE `tabDynamic Link`.parent = `tabAddress`.name
		AND `tabDynamic Link`.link_doctype = 'Customer'
		AND	`tabDynamic Link`.link_name = %(customer_name)s
		AND ifnull(`tabAddress`.disabled, 0) = 0
		ORDER BY `tabAddress`.is_primary_address DESC
		""", {'customer_name': customer_name}, as_dict=True)
	return addy[0].get('name') if addy else ''
