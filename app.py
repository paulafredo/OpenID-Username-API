from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import urlparse
import time

app = Flask(__name__)

# -----------------------------
#  credits : https://great.thug4ff.com/
# -----------------------------


def _get_openid_headers(base_url):
    host = urlparse(base_url).netloc
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "source=pc; region=PK; language=en; "
                  "mspid2=4b56e8f65e7a8454c2dd9e9f1eaff5cc; "
                  "datadome=465CY_MInLmrrYVl4rCZo4ltk_j~~fJgn770GVVBXsV~EoF_BnK9xNJwot4cspq7VSzSa77ZwARm_6IpT8twIt941vFi0dR0oAZcJikHRWCoApFKF9eeI8TREH3r0IAl; "
                  "session_key=x0jshjilr25wwgg993pvlb3wnlwcudct",
        "Host": host,
        "Origin": base_url,
        "Referer": base_url,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"'
    }


def get_openid_data(account_id):
    payload = {
        "app_id": 100067,
        "login_id": str(account_id)
    }

    base_url = "https://shop2game.com"
    url = f"{base_url}/api/auth/player_id_login"
    headers = _get_openid_headers(base_url)

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()

        open_id = data.get("open_id")
        if open_id:
            return {
                "nickname": data.get("nickname"),
                "region": data.get("region"),
                "account_id": account_id,
                "open_id": open_id,
            }

    except Exception as e:
        print("Error:", e)

    return {"error": "Failed to get nickname and open_id"}


@app.route("/username", methods=["GET"])
def api_openid():
    uid = request.args.get("uid")

    if not uid:
        return jsonify({"error": "Missing 'uid' parameter"}), 400

    result = get_openid_data(uid)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
