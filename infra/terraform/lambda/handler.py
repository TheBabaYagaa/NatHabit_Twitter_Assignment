import os
import boto3

REGION = os.getenv("AWS_REGION", "ap-south-1")
SENDER = os.environ["SENDER_EMAIL"]                
DEFAULT_RECIPIENT = os.getenv("DEFAULT_RECIPIENT")   
TEMPLATE = os.getenv("EMAIL_TEMPLATE", "User {follower_id} followed {following_id}.")

ses = boto3.client("ses", region_name=REGION)

def handler(event, context):
    errors = []
    for record in event.get("Records", []):
        attrs = record.get("messageAttributes", {})
        follower_id  = _get(attrs, "follower_id")
        following_id = _get(attrs, "following_id")
        # Prefer recipient provided by the app (the “following” user’s email)
        recipient = _get(attrs, "recipient") or DEFAULT_RECIPIENT or SENDER

        subject = f"New Follwer mail"
        body_txt = TEMPLATE.format(follower_id=follower_id, following_id=following_id)

        try:
            ses.send_email(
                Source=SENDER,
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
