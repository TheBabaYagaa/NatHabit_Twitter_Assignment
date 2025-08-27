import os
import boto3
from django.conf import settings
REGION = settings.AWS_REGION
SENDER_EMAIL = settings.SENDER_MAIL
DEFAULT_RECIPIENT = settings.DEFAULT_RECIPIENT
EMAIL_TEMPLATE = settings.EMAIL_TEMPLATE

ses = boto3.client("ses", region_name=REGION)

def handler(event, context):
    errors = []
    for record in event.get("Records", []):
        attrs = record.get("messageAttributes", {})
        follower_id  = _get(attrs, "follower_id")
        following_id = _get(attrs, "following_id")
        # Prefer recipient provided by the app (the “following” user’s email)
        recipient = _get(attrs, "recipient") or DEFAULT_RECIPIENT or SENDER_EMAIL

        subject = f"New Follwer mail"
        body_txt = EMAIL_TEMPLATE.format(follower_id=follower_id, following_id=following_id)

        try:
            ses.send_email(
                Source=SENDER_EMAIL,
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {
                        "Text": {"Data": body_txt},
                     
                    },
                },
            )
        except Exception as e:
            errors.append(f"{record.get('messageId')}: {e}")

    if errors:
        raise Exception("SES send failures: " + "; ".join(errors))
    return {"status": "ok"}

def _get(attrs, key):
    v = attrs.get(key) or {}
    return v.get("stringValue")
