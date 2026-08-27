#!/usr/bin/env python3
"""
Gazit (CRMonLINE) v3 API discovery probe for FreetaxMainDeskBot.

Resolves the six open integration gaps against the sandbox:
  1. doctype_id table  (proforma / tax-invoice numbers)  <-- critical blocker
  2. payments[] line schema (bank-transfer receipt)
  3. entity selection (פריטקס vs דרור) field on a document
  4. free-text line vs. required product pid
  5. מקור vs נאמן למקור PDF variant
  6. VAT rate currently configured (should be 18%)

USAGE
  # never hardcode creds in a public repo
  export GAZIT_BASE='https://demo.gazitniul.co.il'
  export GAZIT_KEY='NTAxMTMwOA=='
  export GAZIT_ID='ZGVtby5nYXpp'
  export GAZIT_USER='demo'

  python gazit_api_probe.py            # read-only discovery (safe)
  python gazit_api_probe.py --create   # also creates throwaway test docs to map doctypes

Read-only mode never writes anything. --create makes a test account, a test
product, and one minimal invoice per candidate doctype, then reads the label
back. The sandbox is the place to do that; do not point --create at production.
"""

import os, sys, json, urllib.request, urllib.error
issuer = DEMO
BASE = os.environ.get(f"GAZIT_{issuer}_BASE", "").rstrip("/")
HEADERS = {
    "Api-Key": os.environ.get(f"GAZIT_{issuer}_KEY", ""),
    "Api-Id": os.environ.get(f"GAZIT_{issuer}_ID", ""),
    "Api-Username": os.environ.get(f"GAZIT_{issuer}_USER", ""),
    "Content-Type": "application/json",
}
CREATE = "--create" in sys.argv


def call(module, method, body=None, http="POST"):
    """POST JSON to /api/v3/{module}/{method}; return parsed JSON or {error}."""
    url = f"{BASE}/api/v3/{module}/{method}"
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=http)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
    except Exception as e:
        return {"_transport_error": str(e)}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_non_json": raw[:800]}


def show(label, obj):
    print(f"\n=== {label} ===")
    print(json.dumps(obj, ensure_ascii=False, indent=2)[:4000])


# ---------------------------------------------------------------------------
# GAP 1 — doctype_id table
# ---------------------------------------------------------------------------
print("###############  GAP 1: doctype_id table  ###############")

# A valid CRM user_id is needed for IsrInvoice/getAll. Masters are CRM users.
masters = call("Calendar", "getMasters")
show("Calendar/getMasters (to grab a real user_id)", masters)

user_id = None
for key in ("data", "masters", "items"):
    rows = masters.get(key) if isinstance(masters, dict) else None
    if isinstance(rows, list) and rows:
        user_id = rows[0].get("id") or rows[0].get("user_id")
        break
print(f"\n-> using user_id = {user_id}")

# getAll returns rows (doctype <-> label on seeded data) AND can_create_docs,
# the per-doctype permission map that enumerates every doctype id the system knows.
inv_list = call("IsrInvoice", "getAll", {"user_id": user_id or 1, "start": 0, "limit": 50})
show("IsrInvoice/getAll  (look at can_create_docs + each row's doctype/label)", inv_list)

# Read a few seeded invoices  in full to pin doctype_id <-> translated label,
# and (GAP 2) to see the payments block field names on a paying doctype.
seen_ids = []
for key in ("items", "data", "rows"):
    rows = inv_list.get(key) if isinstance(inv_list, dict) else None
    if isinstance(rows, list):
        seen_ids = [r.get("id") or r.get("invoiceid") for r in rows if isinstance(r, dict)]
        break

for iid in [i for i in seen_ids if i][:6]:
    show(f"IsrInvoice/Get id={iid}  (doctype_id, doctype label, payments[] shape)",
         call("IsrInvoice", "Get", {"order_id": iid}))

# ---------------------------------------------------------------------------
# GAP 6 — VAT rate + GAP 2 reference: item catalogue
# ---------------------------------------------------------------------------
print("\n###############  GAP 6: VAT / items  ###############")
show("Product/getCategories", call("Product", "getCategories", {"crm_lang": "he"}))
show("Product/getAll (sample items, check unit_price vs unit_price_vat ratio = VAT)",
     call("Product", "getAll", {"search_needle": "", "start": 0, "limit": 10}))

# ---------------------------------------------------------------------------
# GAP 3 — entity (פריטקס vs דרור): inspect a full invoice header for a
# company/branch/entity column. Already visible in the IsrInvoice/Get dumps above
# look for keys like company_id / entity / branch / cancompany.
# ---------------------------------------------------------------------------
print("\n###############  GAP 3: entity field — scan invoice headers above "
      "for company/branch/entity keys  ###############")

# ---------------------------------------------------------------------------
# CREATE-BASED PROBES (sandbox only) — GAP 1 labels, GAP 2 schema, GAP 4 free-text
# ---------------------------------------------------------------------------
if CREATE:
    print("\n###############  CREATE PROBES (sandbox)  ###############")

    acct = call("Account", "Create", {"accountname": "ZZ API Probe Client",
                                       "cnpj_number": "", "mobile": "0500000000"})
    show("Account/Create (test client)", acct)
    account_id = acct.get("id")

    prod = call("Product", "Create", {"productname": "ZZ Probe - טיפול בהפחתת ארנונה",
                                       "vendorname": "ZZ Probe Vendor",
                                       "productcategory": "Services",
                                       "stock_notify": 0, "unit_price": 100})
    show("Product/Create (test item)", prod)
    pid = prod.get("id")

    # GAP 1: map candidate doctype ids to labels by creating one minimal doc each.
    # 3=receipt(known), 4=likely tax-invoice-receipt, 6/7 paying-unknown; the rest
    # are non-paying candidates (proforma / plain tax invoice / credit note).
    for dt in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        body = {"account_id": account_id, "total": 117, "doctype_id": dt,
                "products": [{"pid": pid, "qty": 1, "price": 100, "vat_percent": 18}]}
        if dt in (3, 4, 6, 7):  # paying doctypes need a payment line (GAP 2 probe)
            body["payments"] = [{"type": "transfer", "sum": 117,
                                 "asmachta": "TEST-REF-001", "date": "15-06-2026"}]
        res = call("IsrInvoice", "Create", body)
        new_id = res.get("id") or res.get("invoice_id")
        label = ""
        if new_id:
            label = call("IsrInvoice", "Get", {"order_id": new_id}).get("doctype_label", "")
        print(f"  doctype_id {dt:>2}: create -> {json.dumps(res, ensure_ascii=False)[:160]}"
              f"  | label='{label}'")

    # GAP 4: does a line WITHOUT a pid (free-text description) get accepted?
    show("IsrInvoice/Create with free-text line, NO pid (GAP 4)",
         call("IsrInvoice", "Create", {
             "account_id": account_id, "total": 117, "doctype_id": 3,
             "products": [{"description": "טיפול בהפחתת ארנונה",
                           "qty": 1, "price": 100, "vat_percent": 18}],
             "payments": [{"type": "transfer", "sum": 117, "asmachta": "TEST-REF-002",
                           "date": "15-06-2026"}]}))

print("\nDone. Paste the output back and I'll turn it into the doctype map + schema.")