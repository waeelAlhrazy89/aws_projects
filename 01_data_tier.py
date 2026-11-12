from config import resource

dynamodb = resource("dynamodb")
table_name = "Tasks"

existing = [t.name for t in dynamodb.tables.all()]
if table_name not in existing:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print("Created table", table_name)
else:
    table = dynamodb.Table(table_name)
    print("Table already exists")

for i, title in enumerate(["Learn S3", "Learn DynamoDB", "Learn Lambda"], start=1):
    table.put_item(Item={"id": str(i), "title": title, "done": False})

print("Tasks in the table:")
for item in table.scan()["Items"]:
    print(" ", item)