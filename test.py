from flask import Flask, request, render_template
from get_ytb_trans import get_ytb_trans
import json
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# .env ファイルから環境変数を読み込む
load_dotenv()

# 環境変数を取得
endpoints = os.environ.get("ENDPOINTS")

if endpoints is None:
    raise EnvironmentError("The ENDPOINTS environment variable is not set.")
else:
    endpoints = endpoints.split(",")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", endpoints=endpoints)


def fetch_content(url, endpoint):
    if endpoint == "http://127.0.0.1:5000/get_ytb_trans":
        response = get_ytb_trans(type("FakeRequest", (), {"args": {"url": url}}))
        # responseがタプルの場合（エラー時）の処理を追加
        if isinstance(response, tuple):
            return f"Error: {response[0].json['error']}" if len(response) > 0 else "Unknown error occurred"
        json_data = json.loads(response.data)
        return json_data["transcript"]
    else:
        response = requests.get(f"{endpoint}?url={url}")
        json_data = response.json()
        return json_data["transcript"] if response.status_code == 200 else f"Error: {response.text}"


@app.route("/show_result", methods=["POST"])
def show_result():
    url = request.form["url"]
    endpoint = request.form["endpoint"]
    content = fetch_content(url, endpoint)
    return render_template("index.html", content=content, endpoints=endpoints)


@app.route("/get_ytb_trans", methods=["GET"])
def get_txt_from_url_route():
    return get_ytb_trans(request)


if __name__ == "__main__":
    app.run(debug=True)
