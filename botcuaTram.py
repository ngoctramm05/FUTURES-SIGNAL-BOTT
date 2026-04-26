import time
import requests
from datetime import datetime
from statistics import mean

# ===== CONFIG =====
SYMBOLS = [
    "AAPLONUSDT","ABNBONUSDT","ACNONUSDT","ADBEONUSDT","AMDONUSDT","APPONUSDT",
    "AVGOONUSDT","AXPONUSDT","BAONUSDT","BIDUONUSDT","CMGONUSDT","COINONUSDT",
    "COSTONUSDT","CRCLONUSDT","CRMONUSDT","DASHONUSDT","DISONUSDT","EQIXONUSDT",
    "FIGONUSDT","FUTUONUSDT","GEONUSDT","GMEONUSDT","GOOGLONUSDT","GSONUSDT",
    "HIMSONUSDT","HOODONUSDT","INTCONUSDT","INTUONUSDT","JDONUSDT","LINONUSDT",
    "MAONUSDT","MARAONUSDT","METAONUSDT","MRVLONUSDT","MSFTONUSDT","MSTRONUSDT",
    "MUONUSDT","NFLXONUSDT","NOWONUSDT","NVDAONUSDT","PANWONUSDT","PBRONUSDT",
    "PLTRONUSDT","PYPLONUSDT","RDDTONUSDT","RIOTONUSDT","SBETONUSDT","SHOPONUSDT",
    "SPGIONUSDT","SPOTONUSDT","TSLAONUSDT","TSMONUSDT","UNHONUSDT","WFCONUSDT"
]

BOT_TOKEN = "8697693935:AAGPMBCXIX5VPVFm4KeQ4VbAqwSCgt2bBGE"
CHAT_ID = "7811957600"

GRANULARITY = "5min"
LIMIT = 100
LOOP_SECONDS = 30
ALERT_COOLDOWN = 300  # 5 phut / 1 ma

API = "https://api.bitget.com/api/v2/spot/market/candles"
TG = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

last_state = {}
last_alert_time = {}

# ===== API =====
def get_data(symbol):
    params = {"symbol": symbol, "granularity": GRANULARITY, "limit": str(LIMIT)}
    r = requests.get(API, params=params, timeout=15)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != "00000" or "data" not in j:
        raise RuntimeError(f"Bitget error: {j}")
    data = j["data"]
    closes = [float(x[4]) for x in data]
    volumes = [float(x[5]) for x in data]
    ts = int(data[-1][0])
    return closes, volumes, ts

# ===== INDICATORS =====
def ema(data, p):
    k = 2 / (p + 1)
    out = [data[0]]
    for x in data[1:]:
        out.append(x * k + out[-1] * (1 - k))
    return out

def rsi(data, p=14):
    if len(data) < p + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, len(data)):
        d = data[i] - data[i - 1]
        gains.append(max(d, 0))
        losses.append(abs(min(d, 0)))
    avg_gain = mean(gains[-p:]) if gains[-p:] else 0
    avg_loss = mean(losses[-p:]) if losses[-p:] else 0
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ===== SIGNAL =====
def signal(close, vol):
    e9 = ema(close, 9)
    e21 = ema(close, 21)

    cur = close[-1]
    prev = close[-2]
    r = rsi(close)

    vol_avg = mean(vol[-20:]) if len(vol) >= 20 else mean(vol)
    vol_now = vol[-1]
    vol_ok = vol_now >= 0.8 * vol_avg
    vol_strong = vol_now >= 1.2 * vol_avg

    bull_cross = e9[-2] <= e21[-2] and e9[-1] > e21[-1]
    bear_cross = e9[-2] >= e21[-2] and e9[-1] < e21[-1]
    bull_trend = e9[-1] > e21[-1]
    bear_trend = e9[-1] < e21[-1]

    # Nới tín hiệu để báo nhiều hơn
    if bull_cross and r < 72:
        s = "BUY"
        act = "👉 MUA NGAY"
    elif bear_cross and r > 28:
        s = "SELL"
        act = "👉 BÁN NGAY"
    elif bull_trend and r < 68 and vol_ok:
        s = "WATCH BUY"
        act = "👉 CANH MUA"
    elif bear_trend and r > 32 and vol_ok:
        s = "WATCH SELL"
        act = "👉 CANH BÁN"
    else:
        s = "HOLD"
        act = "👉 THEO DÕI"

    return {
        "price": cur,
        "signal": s,
        "action": act,
        "rsi": r,
        "ema9": e9[-1],
        "ema21": e21[-1],
        "vol": vol_now,
        "vol_avg": vol_avg,
        "vol_strong": vol_strong,
        "dp": (cur - prev) / prev * 100
    }

# ===== TELEGRAM =====
def send(msg):
    try:
        requests.post(
            TG,
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print("TELEGRAM ERR:", e)

def format_msg(symbol, r, ts_text):
    if r["signal"] == "BUY":
        icon = "🟢"
    elif r["signal"] == "SELL":
        icon = "🔴"
    elif r["signal"] == "WATCH BUY":
        icon = "🟡"
    elif r["signal"] == "WATCH SELL":
        icon = "🟠"
    else:
        icon = "⚪"

    raw = (
        f"{symbol} | Price: {r['price']:.4f} | "
        f"Signal: {r['signal']} | "
        f"RSI: {r['rsi']:.2f} | "
        f"EMA9: {r['ema9']:.4f} | "
        f"EMA21: {r['ema21']:.4f} | "
        f"dP: {r['dp']:+.2f}% | "
        f"Vol: {r['vol']:.2f}/{r['vol_avg']:.2f}"
    )

    return (
        f"📊 <b>ROBO-ADVISOR SIGNAL</b>\n\n"
        f"{icon} <b>Token:</b> {symbol}\n"
        f"💰 <b>Giá:</b> {r['price']:.2f} USDT\n"
        f"🎯 <b>Tín hiệu:</b> {r['signal']}\n"
        f"📈 <b>Biến động:</b> {r['dp']:+.2f}%\n"
        f"📊 <b>RSI:</b> {r['rsi']:.2f}\n"
        f"📉 <b>EMA9:</b> {r['ema9']:.4f}\n"
        f"📉 <b>EMA21:</b> {r['ema21']:.4f}\n"
        f"🔊 <b>Volume:</b> {r['vol']:.2f}/{r['vol_avg']:.2f}\n"
        f"⏰ <b>Thời gian:</b> {ts_text}\n\n"
        f"{r['action']}\n\n"
        f"<code>{raw}</code>"
    )

def should_alert(symbol, state):
    if state == "HOLD":
        return False
    now = time.time()
    prev_state = last_state.get(symbol)
    prev_time = last_alert_time.get(symbol, 0)

    # Gui neu doi trang thai, hoac cung trang thai nhung qua cooldown
    if state != prev_state or (now - prev_time >= ALERT_COOLDOWN):
        last_state[symbol] = state
        last_alert_time[symbol] = now
        return True
    return False

# ===== MAIN =====
print("BOT STARTED...")
send(
    f"🚀 <b>ROBO-ADVISOR STARTED!</b>\n"
    f"Theo doi {len(SYMBOLS)} token\n"
    f"Khung nen: {GRANULARITY} | Chu ky quet: {LOOP_SECONDS}s"
)

while True:
    print("\n" + "-" * 120)
    print("Scan at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 120)

    for s in SYMBOLS:
        try:
            closes, volumes, ts = get_data(s)
            r = signal(closes, volumes)
            ts_text = datetime.fromtimestamp(ts / 1000).strftime("%H:%M:%S")

            line = (
                f"{s:<12} | Price: {r['price']:<10.4f} | Signal: {r['signal']:<10} | "
                f"RSI: {r['rsi']:>6.2f} | EMA9: {r['ema9']:>10.4f} | "
                f"EMA21: {r['ema21']:>10.4f} | dP: {r['dp']:>6.2f}% | "
                f"Vol: {r['vol']:.2f}/{r['vol_avg']:.2f}"
            )
            print(line)

            if should_alert(s, r["signal"]):
                send(format_msg(s, r, ts_text))

        except Exception as e:
            print("ERR:", s, e)

    time.sleep(LOOP_SECONDS)