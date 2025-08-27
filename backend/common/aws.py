# common/aws.py
import boto3
import os

_sqs = None
def sqs_client():
    global _sqs
    if _sqs is None:
        _sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))
    return _sqs

def send_follow_event(follower_id: int, following_id: int, recipient_email: str | None = None):
    url = os.getenv("SQS_QUEUE_URL", "")
    if not url:
        return
    attrs = {
        "follower_id":  {"StringValue": str(follower_id),  "DataType": "String"},
        "following_id": {"StringValue": str(following_id), "DataType": "String"},
    }
    if recipient_email:
        attrs["recipient"] = {"StringValue": recipient_email, "DataType": "String"}

    sqs_client().send_message(
        QueueUrl=url,
        MessageBody="follow",
        MessageAttributes=attrs,
    )
