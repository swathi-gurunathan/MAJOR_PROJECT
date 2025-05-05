import os
import email
from email import policy
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to extract links from email body
def extract_links(body):
    return re.findall(r'https?://\S+', body)

# Function to process .eml files and extract features
def process_emails(eml_folder):
    email_data = []
    for filename in os.listdir(eml_folder):
        if filename.endswith(".eml"):
            with open(os.path.join(eml_folder, filename), 'r', encoding='utf-8') as f:
                msg = email.message_from_file(f, policy=policy.default)

                from_email = msg.get("From")
                to_email = msg.get("To")
                subject = msg.get("Subject", "")
                date = msg.get("Date")

                body = ""
                is_html = 0
                num_attachments = 0

                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode(errors='ignore')
                    elif content_type == "text/html":
                        is_html = 1
                        html = part.get_payload(decode=True).decode(errors='ignore')
                        body = BeautifulSoup(html, "lxml").get_text()
                    elif "attachment" in content_disposition:
                        num_attachments += 1

                links = extract_links(body)
                email_data.append({
                    "from_email": from_email,
                    "to_email": to_email,
                    "subject": subject,
                    "subject_keywords": " ".join(subject.lower().split()[:5]),  # top 5 words
                    "timestamp": date,
                    "body_text": body[:300],  # optionally truncate
                    "num_links": len(links),
                    "num_attachments": num_attachments,
                    "is_html": is_html
                })

    return pd.DataFrame(email_data)