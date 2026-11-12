import io
import zipfile

from config import client

lam = client("lambda")
NAME = "tasks-api"

# Address of Floci as seen from INSIDE the Lambda container.
# "localhost" would mean the container itself, so we try this one first.
DB_ENDPOINT = "http://host.docker.internal:4566"

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.write("app_tier/lambda_function.py", "lambda_function.py")
code = buf.getvalue()

env = {"Variables": {"DB_ENDPOINT": DB_ENDPOINT}}

try:
    lam.get_function(FunctionName=NAME)
    lam.update_function_code(FunctionName=NAME, ZipFile=code)
    lam.update_function_configuration(FunctionName=NAME, Environment=env, Timeout=30)
    print("Updated function")
except lam.exceptions.ResourceNotFoundException:
    lam.create_function(
        FunctionName=NAME,
        Runtime="python3.12",
        Role="arn:aws:iam::000000000000:role/lambda-role",
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": code},
        Environment=env,
        Timeout=30,
    )
    print("Created function")