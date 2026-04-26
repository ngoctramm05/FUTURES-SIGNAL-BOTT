import time
import requests
from datetime import datetime
from statistics import mean

# ===== CONFIG =====
SYMBOLS = [
    "BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","LINKUSDT","DOTUSDT",
    "LTCUSDT","MATICUSDT","TRXUSDT","UNIUSDT","ATOMUSDT",
    "ETCUSDT","FILUSDT","APTUSDT","OPUSDT","ARBUSDT"
]

BOT_TOKEN = "8571428242:AAElbRc4pk_yhzvlSndPT9XzpRYaUexkRc4"
CHAT_ID = "7811957600"

TG = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

LOOP_SECONDS = 30  # < 30s theo đề

# ===== API =====
def get_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=100"
    data = requests.get(url, timeout=10).json()

    closes = [float(x[4]) for x in data]
    volumes = [float(x[5]) for x in data]

    return closes, volumes

# ===== INDICATORS =====
def ema(data, p):
    k = 2 / (p + 1)
    out = [data[0]]
    for x in data[1:]:
        out.append(x * k + out[-1] * (1 - k))
    return out

def rsi(data, p=14):
    gains, losses = [], []
    for i in range(1, len(data)):
        d = data[i] - data[i - 1]
        gains.append(max(d, 0))
        losses.append(abs(min(d, 0)))
    avg_gain = mean(gains[-p:])
    avg_loss = mean(losses[-p:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ===== SIGNAL LOGIC (>=2 ALPHA) =====
def signal(close, vol):
    e9 = ema(close, 9)
    e21 = ema(close, 21)
    r = rsi(close)

    vol_avg = mean(vol[-20:])
    vol_now = vol[-1]

    change = (close[-1] - close[-2]) / close[-2] * 100

    # Alpha 1: RSI
    # Alpha 2: Volume spike
    # Bonus: EMA trend

    if r < 40 and vol_now > vol_avg * 1.2 and e9[-1] > e21[-1]:
        return "LONG", r, vol_now/vol_avg, change, "RSI thấp + Volume tăng + Trend tăng"

    elif r > 60 and vol_now > vol_avg * 1.2 and e9[-1] < e21[-1]:
        return "SHORT", r, vol_now/vol_avg, change, "RSI cao + Volume tăng + Trend giảm"

    elif vol_now > vol_avg * 1.8:
        return "WATCH", r, vol_now/vol_avg, change, "Volume đột biến"

    else:
        return "HOLD", r, vol_now/vol_avg, change, ""

# ===== TELEGRAM =====
def send(msg):
    try:
        requests.post(
            TG,
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print("TELEGRAM ERROR:", e)

# ===== MAIN =====
print("🚀 BOT STARTED")
send("🚀 <b>Futures Signal Bot Started</b>")

while True:
    now = datetime.now()
    time_text = now.strftime("%H:%M:%S %d/%m/%Y")

    print("\nScan:", time_text)

    signals = []

    for s in SYMBOLS:
        try:
            closes, volumes = get_data(s)
            sig, r, vol_ratio, change, reason = signal(closes, volumes)

            if sig != "HOLD":
                price = closes[-1]

                if sig == "LONG":
                    icon = "🟢"
                elif sig == "SHORT":
                    icon = "🔴"
                else:
                    icon = "⚡"

                text = (
                    f"{icon} <b>{s} → {sig}</b>\n"
                    f"💰 Giá: {price:.4f}\n"
                    f"📊 RSI: {r:.2f}\n"
                    f"📈 Biến động: {change:+.2f}%\n"
                    f"🔊 Volume Spike: {vol_ratio:.2f}x\n"
                    f"🧠 {reason}\n"
                )

                signals.append(text)

                print(s, sig)

        except Exception as e:
            print("ERR:", s, e)

    # ===== GỬI TELEGRAM =====
    if signals:
        msg = (
            f"📊 <b>MEXC SIGNAL BOT</b>\n"
            f"⏰ {time_text}\n"
            f"🔔 {len(signals)} tín hiệu\n\n"
        )
        msg += "\n".join(signals)

        send(msg)

    time.sleep(LOOP_SECONDS)