import requests
import os
from dotenv import load_dotenv


load_dotenv()


def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"Yaseen <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body,
        },
    )


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully Signed up!",
        f"Hi,{username}! You have Successfully signed up for my REST API!",
    )
