import json
import uuid
import boto3
import logging
from datetime import datetime

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("students")

def lambda_handler(event, context):

    logger.info("Received event: %s", json.dumps(event))

    try:
        # check body exists
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Missing request body"
                })
            }

        payload = json.loads(event["body"])

        # basic validation
        if "name" not in payload or "module" not in payload:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Payload must include name and module"
                })
            }

        item_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        item = {
            "id": item_id,
            "timestamp": timestamp,
            "payload": payload
        }

        logger.info("Writing item to DynamoDB: %s", json.dumps(item))

        table.put_item(Item=item)

        logger.info("Successfully stored student with id: %s", item_id)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Student stored successfully",
                "id": item_id,
                "timestamp": timestamp
            })
        }

    except json.JSONDecodeError:
        logger.error("Invalid JSON format")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid JSON payload"
            })
        }

    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }