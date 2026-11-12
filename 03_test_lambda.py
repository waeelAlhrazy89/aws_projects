import json

from config import client

lam = client("lambda")


def call(event):
    response = lam.invoke(FunctionName="tasks-api", Payload=json.dumps(event))
    result = response["Payload"].read().decode()
    if "FunctionError" in response:
        print("FUNCTION ERROR:", result)
    else:
        print(result)


print("1) List tasks:")
call({"httpMethod": "GET"})

print("2) Add a task:")
call({"httpMethod": "POST", "body": json.dumps({"title": "Learn API Gateway"})})

print("3) List again:")
call({"httpMethod": "GET"}) 