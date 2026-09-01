# pip install agentmail
import os
from agentmail import AgentMail
from datetime import datetime, timezone
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from zoneinfo import ZoneInfo
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = AgentMail(api_key=os.environ.get("AGENTMAIL_API_KEY"))
tz = ZoneInfo("Asia/Jerusalem")
after=datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
print(f"Fetching emails after: {after.isoformat()}")
res = client.inboxes.messages.list(
  inbox_id="freetax@agentmail.to",
  limit=100,
  after=after
)

print(res)