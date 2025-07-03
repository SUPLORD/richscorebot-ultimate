import requests, time
_CACHE = {}
def get_key_rate():
    now = time.time()
    if _CACHE and now - _CACHE["ts"] < 3600:
        return _CACHE["rate"]
    r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    rate = r["Valute"]["USD"]["Value"]
    _CACHE.update({"rate": rate, "ts": now})
    return rate
