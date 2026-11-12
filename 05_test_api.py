import json
import urllib.error
import urllib.request

api_id = open("api_id.txt").read().strip()
HOST = f"{api_id}.execute-api.localhost.floci.io"
URL = f"http://{HOST}:4566/dev/tasks"


def call(method, body=None):
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(URL, data=data, method=method, headers=headers)
        resp = urllib.request.urlopen(req, timeout=60)
    except urllib.error.URLError as e:
        if isinstance(e, urllib.error.HTTPError):
            raise
        # Fallback if the hostname doesn't resolve on your network:
        # connect to localhost but still send the API's hostname.
        headers["Host"] = f"{HOST}:4566"
        req = urllib.request.Request(
            "http://localhost:4566/dev/tasks", data=data, method=method, headers=headers
        )
        resp = urllib.request.urlopen(req, timeout=60)
    print(resp.status, resp.read().decode())


print("1) GET /tasks")
call("GET")

print("2) POST /tasks")
call("POST", {"title": "Build the web tier"})

print("3) GET /tasks")
call("GET")