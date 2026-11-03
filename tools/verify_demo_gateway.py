"""Read-only demo gateway smoke test. Never sends orders."""
import json
import os
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:5001"

def get(path):
    request = urllib.request.Request(
        BASE + path,
        headers={"Authorization": "Bearer " + os.environ["API_KEY"]},
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.load(response)

def main():
    deadline = time.monotonic() + 150
    last_error = "no response"
    while time.monotonic() < deadline:
        try:
            status = get("/health/ready")
            if status.get("status") == "ready" and status.get("mt5_status") == "connected":
                break
            last_error = "gateway not yet reporting ready/connected"
        except (OSError, urllib.error.HTTPError, ValueError, TimeoutError) as exc:
            last_error = type(exc).__name__ + (" HTTP " + str(exc.code) if isinstance(exc, urllib.error.HTTPError) else "")
        time.sleep(8)
    else:
        raise SystemExit("FAIL: gateway not ready after 150 seconds; last error: " + last_error)

    try:
        account = get("/account")
    except (OSError, ValueError) as exc:
        raise SystemExit("FAIL: account endpoint: " + type(exc).__name__)
    if str(account.get("login", account.get("account", ""))) != str(os.environ["MT5_LOGIN"]):
        raise SystemExit("FAIL: broker account mismatch")
    if account.get("trade_mode", account.get("mode")) not in (0, "0", "demo", "DEMO"):
        raise SystemExit("FAIL: account not confirmed demo")
    print("PASS: MT5 demo broker connection confirmed; no orders sent")

if __name__ == "__main__":
    main()
