# MT5 demo account connection checklist

This project is **not live-trading enabled**. The read-only GitHub Actions smoke test requires three GitHub Actions repository secrets:

- `MT5_DEMO_LOGIN`: demo account login
- `MT5_DEMO_PASSWORD`: demo trading password
- `MT5_DEMO_SERVER`: exact broker server (not shown in account screenshot)
- `MT5_GATEWAY_API_KEY`: a unique random gateway authentication key

**Do not paste account passwords into issues, commits, or chat.** The demo password was exposed in a screenshot and should be rotated.

Run the workflow manually under Actions → MT5 demo broker smoke test → Run workflow. A successful run must verify account number, demo trade mode, and broker connectivity; it must never place an order.

**Known blockers:** actual MT5 gateway health and account endpoint compatibility has not been validated; broker server and GitHub secrets are absent. Do not treat passing unit tests as broker verification. Scheduled order execution is not enabled.
