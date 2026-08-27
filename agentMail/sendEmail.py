# pip install agentmail
import os
from agentmail import AgentMail
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = AgentMail(api_key=os.environ.get("AGENTMAIL_API_KEY"))
client.inboxes.messages.send(
    "freetax@agentmail.to",
    to=["noinoya@gmail.com"],
    subject="TEST1",
    text="Sent from an AgentMail inbox.",
)