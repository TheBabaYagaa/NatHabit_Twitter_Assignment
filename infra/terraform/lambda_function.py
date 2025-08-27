import os
import boto3
import logging 

logger = logging.getLogger() 
logger.setLevel(logging.INFO)

REGION = os.environ.get("AWS_REGION", "eu-north-1")
SENDER_MAIL = os.environ.get("SENDER_MAIL")
DEFAULT_RECIPIENT = os.environ.get("DEFAULT_RECIPIENT")
EMAIL_TEMPLATE = os.environ.get("EMAIL_TEMPLATE", "User {follower_id} followed user {following_id}")


ses = boto3.client("ses", region_name=REGION)

def handler(event, context):
    # print("hello lambda")
    errors = []
    for record in event.get("Records", []):
        attrs = record.get("messageAttributes", {})
        follower_id  = _get(attrs, "follower_id")
        following_id = _get(attrs, "following_id")
        # Prefer recipient provided by the app (the “following” user’s email)
        recipient = _get(attrs, "recipient") or DEFAULT_RECIPIENT or SENDER_MAIL

        subject = f"New Follwer email"
        body_txt = EMAIL_TEMPLATE.format(follower_id=follower_id, following_id=following_id)

        try:
            ses.send_email(
                Source=SENDER_MAIL,
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
