import time
import pandas as pd
import numpy as np
from tradingview_ta import TA_Handler, Interval
from telegram import Bot

# === KONFIGURASI ===
TELEGRAM_TOKEN = "ISI_TOKEN_BOT_KAMU_DI_SINI"
TELEGRAM_CHAT_ID = "ISI_CHAT_ID_KAMU_DI_SINI"
SYMBOL = "EURUSD"  # bisa ganti misal: BTCUSD, GBPUSD, EURJPY
TIMEFRAME = Interval.INTERVAL_1_MINUTE  # 1 menit
CHECK_INTERVAL = 60  # detik (cek setiap 1 menit)

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def get_signal():
    handler = TA_Handler(
        symbol=SYMBOL,
        screener="forex",
        exchange="OANDA",
        interval=TIMEFRAME
    )
    analysis = handler.get_analysis()
    ema5 = analysis.indicators["EMA5"]
    ema20 = analysis.indicators["EMA20"]
    ema50 = analysis.indicators["EMA50"]
    rsi = analysis.indicators["RSI"]

    # --- logika sinyal ---
    if ema5 > ema20 and ema20 > ema50 and rsi > 50:
        signal = f"📈 BUY Signal: {SYMBOL}\nRSI: {rsi:.2f}\nEMA5>EMA20>EMA50 ✅"
        return signal
    elif ema5 < ema20 and ema20 < ema50 and rsi < 50:
        signal = f"📉 SELL Signal: {SYMBOL}\nRSI: {rsi:.2f}\nEMA5<EMA20<EMA50 ✅"
        return signal
    else:
        return None

def main():
    print("Bot sinyal berjalan...")
    last_signal = None
    while True:
        try:
            signal = get_signal()
            if signal and signal != last_signal:
                send_signal(signal)
                print(signal)
                last_signal = signal
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("Error:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
