import os, anthropic, json
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = anthropic.Client(api_key=os.environ.get("ANTHROPIC_API_KEY"))
res = client.messages.create(
    max_tokens=1024,
    model="claude-sonnet-5",
   system="""You extract structured data from an email sent to an accounting office's automation inbox.
The email is usually in Hebrew and asks to issue a document. Return ONLY a JSON object — no markdown, no explanation — with these fields:
- issuer: 'freetax' or 'law'
- doctype: 'receipt' | 'tax_invoice' | 'tran_invoice'
- customer_name: the client the document is for, the one who pays, usually in Hebrew
- items: name_key is 'arnona' by default (always one item); if the email mentions שכר טרחה, name_key is 'prof_fee'
- amount: the total as a number, mandatory
- vat_included: your job is אם determine if the amount includes VAT or not, and return a boolean
- payment_type: relevant only for doctypes 'receipt' and 'tax_invoice'(do not show on others), defaults 'bank_transfer', which is called 'העברה' in Hebrew; if the email mentions 'מזומן' or 'cash', return 'cash'; if the email mentions 'צ'ק' or 'check', return 'check'
If a required field is missing, still return the JSON with that field null, along with a warning.""",
    messages=[
        {"role": "user", "content": "להוציא מפריטקס לריברסייד , חן עסקה על סך של  60,000 ₪ +מעמ "}
    ],)

for block in res.content:
    if block.type == "text":
        clean = block.text[block.text.find("{"): block.text.rfind("}") + 1]
        data = json.loads(clean)
        print(json.dumps(data, indent=2, ensure_ascii=False))