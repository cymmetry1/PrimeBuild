"""Read-only MT5 demo connection test; never submits an order."""
import json
import os
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:5001"

def get(path):
    request = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + os.environ["API_KEY"]})
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.load(response)

def main():
    for _ in range(48):
        try:
            status = get("/health/ready")
            if status.get("status") == "ready" and status.get("mt5_status") == "connected":
                break
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass
        time.sleep(10)
    else:
        raise SystemExit("FAIL: broker connection not ready after 8 minutes")
    account = get("/account")
    if str(account.get("login", account.get("account", ""))) != str(os.environ["MT5_LOGIN"]):
        raise SystemExit("FAIL: broker account mismatch")
    if account.get("trade_mode", account.get("mode")) not in (0, "0", "demo", "DEMO"):
        raise SystemExit("FAIL: account not confirmed demo")
    print("PASS: MT5 demo broker connection confirmed; no orders sent")

if __name__ == "__main__":
    main()
