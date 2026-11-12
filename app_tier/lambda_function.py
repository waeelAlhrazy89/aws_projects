import json
import os
import uuid

import boto3

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
}


def get_table():
    endpoint = os.environ.get("DB_ENDPOINT")
    if endpoint:
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
    else:
        dynamodb = boto3.resource("dynamodb")
        return dynamodb.Table(os.environ.get("TABLE_NAME", "Tasks"))


def respond(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", **CORS_HEADERS},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    method = (
        event.get("httpMethod")
        or event.get("requestContext", {}).get("http", {}).get("method")
        or "GET"
    )

    # The browser's "am I allowed?" check
    if method == "OPTIONS":
        return respond(200, {"status": "ok"})

    table = get_table()

    if method == "GET":
        return respond(200, table.scan()["Items"])

    if method == "POST":
        data = json.loads(event.get("body") or "{}")
        item = {"id": str(uuid.uuid4()), "title": data.get("title", "untitled"), "done": False}
        table.put_item(Item=item)
        return respond(201, item)

    return respond(405, {"error": "Method not allowed"})