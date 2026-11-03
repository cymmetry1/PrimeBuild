"""Read-only native Windows MT5 broker check. No orders or account changes."""
import os
import sys
import time
import MetaTrader5 as mt5

login = int(os.environ["MT5_LOGIN"])
server = os.environ["MT5_SERVER"]
password = os.environ["MT5_PASSWORD"]

# Native Windows Python-to-terminal IPC, not Docker/Wine.
# MetaTrader5.initialize() may install/start a terminal automatically.
connected = False
for attempt in range(3):
    if mt5.initialize(login=login, password=password, server=server, timeout=60000):
        connected = True
        break
    print("MT5 native initialization attempt", attempt + 1, "failed:", mt5.last_error())
    mt5.shutdown()
    time.sleep(10)
if not connected:
    sys.exit("FAIL: native Windows terminal could not connect to broker")

try:
    account = mt5.account_info()
    if account is None:
        sys.exit("FAIL: broker returned no account information")
    if account.login != login:
        sys.exit("FAIL: wrong broker account")
    if account.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        sys.exit("FAIL: connected account is not DEMO; no trades sent")
    symbol = mt5.symbol_info("EURUSD")
    if symbol is None:
        sys.exit("FAIL: EURUSD not found on connected broker")
    print("PASS: native MT5 broker demo connection, correct account and EURUSD symbol.")
    print("Broker:", account.company, "Server:", account.server, "EURUSD digits:", symbol.digits)
    print("No orders placed; this is a connectivity check only.")
finally:
    mt5.shutdown()
