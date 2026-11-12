from config import client

s3 = client("s3")
BUCKET = "tasks-web"

api_id = open("api_id.txt").read().strip()
api_url = f"http://{api_id}.execute-api.localhost.floci.io:4566/dev/tasks"

with open("web_tier/index.html", encoding="utf-8") as f:
    html = f.read().replace("__API_URL__", api_url)

if BUCKET not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
    s3.create_bucket(Bucket=BUCKET)

s3.put_object(Bucket=BUCKET, Key="index.html", Body=html.encode("utf-8"), ContentType="text/html")
print(f"Open: http://localhost:4566/{BUCKET}/index.html")