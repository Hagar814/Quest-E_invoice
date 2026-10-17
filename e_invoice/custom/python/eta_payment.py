import frappe

# Always sent to ETA in "salesOrderReference"
SALES_ORDER_REFERENCE = "الشركة تخضع لنظام الدفعات المقدمة لعام ٢٠٢٦"

# Mercuri bank accounts per invoice currency
MERCURI_BANK_ACCOUNTS = {
    "EGP": "100064722357",
    "USD": "100064722314",
}


def is_mercuri_company(company):
    name = (company or "").strip().lower()
    return "mercuri" in name or "merquri" in name


def get_bank_account_no_eta(sales_invoice):
    """Bank account number to send to ETA.

    - Mercuri + EGP -> 100064722357
    - Mercuri + USD -> 100064722314
    - Quest (any currency) / anything else -> the invoice's bank_account_no
    """
    company = sales_invoice.get("company")
    currency = (sales_invoice.get("currency") or "").upper()

    if is_mercuri_company(company) and currency in MERCURI_BANK_ACCOUNTS:
        value = MERCURI_BANK_ACCOUNTS[currency]
    else:
        value = sales_invoice.get("bank_account_no") or ""

    # Keep the field on the invoice in sync when it exists, so the user sees what was sent
    meta = frappe.get_meta(sales_invoice.doctype)
    if meta.has_field("bank_account_no_eta") and sales_invoice.get("bank_account_no_eta") != value:
        frappe.db.set_value(sales_invoice.doctype, sales_invoice.name,
                            "bank_account_no_eta", value, update_modified=False)
        sales_invoice.bank_account_no_eta = value

    return value
