from flask import Flask, request, Response, send_from_directory
import urllib.request
import urllib.error

app = Flask(__name__)

FRONTEND = "frontend"
API = "http://localhost:5000"


@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy_api(path):
    url = f"{API}/api/{path}"

    data = request.get_data() if request.method != "GET" else None

    headers = {}
    if request.content_type:
        headers["Content-Type"] = request.content_type

    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=request.method
    )

    try:
        with urllib.request.urlopen(req) as response:
            return Response(
                response.read(),
                status=response.status,
                content_type=response.headers.get("Content-Type")
            )
    except urllib.error.HTTPError as e:
        return Response(e.read(), status=e.code)


@app.route("/")
def frontend():
    return send_from_directory(FRONTEND, "index.html")


app.run(port=8080)
