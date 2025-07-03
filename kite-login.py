from kiteconnect import KiteConnect
import json

# === Load existing config ===
CONFIG_PATH = "kite_config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

api_key = config["api_key"]
api_secret = config["api_secret"]


kite = KiteConnect(api_key=api_key)
print(kite.login_url())
request_token = input("Enter request token: ")
data = kite.generate_session(request_token, api_secret=api_secret)
access_token = data["access_token"]
print(access_token)

config["access_token"] = access_token
with open(CONFIG_PATH, "w") as f:
    json.dump(config, f, indent=4)

print("Updated key config with new access token")