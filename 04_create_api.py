from config import client

lam = client("lambda")
api = client("apigatewayv2")

API_NAME = "tasks-http-api"
STAGE = "dev"

function_arn = lam.get_function(FunctionName="tasks-api")["Configuration"]["FunctionArn"]

# Remove an older copy so the new routes apply
for old in [a for a in api.get_apis()["Items"] if a["Name"] == API_NAME]:
    api.delete_api(ApiId=old["ApiId"])
    print("Deleted old API")

api_id = api.create_api(Name=API_NAME, ProtocolType="HTTP")["ApiId"]

integration_id = api.create_integration(
    ApiId=api_id,
    IntegrationType="AWS_PROXY",
    IntegrationUri=function_arn,
    PayloadFormatVersion="2.0",
)["IntegrationId"]

for route in ["GET /tasks", "POST /tasks", "OPTIONS /tasks"]:
    api.create_route(
        ApiId=api_id,
        RouteKey=route,
        Target=f"integrations/{integration_id}",
    )

api.create_stage(ApiId=api_id, StageName=STAGE, AutoDeploy=True)

with open("api_id.txt", "w") as f:
    f.write(api_id)

print("API id:", api_id)
print(f"URL: http://{api_id}.execute-api.localhost.floci.io:4566/{STAGE}/tasks")