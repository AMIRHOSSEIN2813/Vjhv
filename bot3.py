from pyrogram import Client, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from collections import defaultdict
import time
import requests
import json
import re

API_ID = "683734"
API_HASH = "cd3c11f1f8b1368ef2d0623342fbe821"
BOT_TOKEN = "7651297573:AAEYS77wi4qsz4RYemGYungEWQdJs_ZTkCU"
ADMIN_USER_ID = 575030674
banned_users = set()


app = Client("crypto_price_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


crypto_dict = {
    "BTC": ["بیت کوین", "بیتکوین", "بیت‌کوین"],
    "SHIB": ["شیبا", "شیبا اینو"],
    "LTC": ["لایت کوین"],
    "XRP": ["ریپل"],
    "USDT": ["تتر"],
    "BNB": ["بایننس کوین"],
    "DOGE": ["دوج کوین"],
    "ADA": ["کارادانو"],
    "DOT": ["پولکادات"],
    "SOL": ["سولانا"],
    "LINK": ["چین لینک"],
    "BCH": ["بیت کوین کش", "بیتکوین کش"],
    "AVAX": ["آوالانچ", "اواکس"],
    "XMR": ["مونرو"],
    "ZEC": ["زی کش"],
    "ONE": ["هارمونی"],
    "MIOTA": ["آیوتا"],
    "MANA": ["دیسنترالند"],
    "AXS": ["اکسی اینفینیتی"],
    "XLM": ["استلار"],
    "FIL": ["فایل کوین"],
    "ONT": ["آنتولوژی"],
    "CRV": ["کرو فایننس", "کرو دائو"],
    "COMP": ["کامپوند"],
    "SUSHI": ["سوشی سواپ", "سوشی‌سواپ"],
    "MKR": ["میکر"],
    "HBAR": ["هیدرا هشگراف", "هدرا"],
    "DGB": ["دیجی بایت"],
    "CHZ": ["چیلیز"],
    "ALGO": ["آلگوراند"],
    "NEAR": ["نیر", "نیر پروتکل"],
    "XTZ": ["تزوس"],
    "KNC": ["کایبر نتورک"],
    "RENBTC": ["ریبون"],
    "GALA": ["گلکسی"],
    "SNX": ["سینتتیکس"],
    "VET": ["ورتیس"],
    "REN": ["رین"],
    "DAO": ["سازمان غیرمتمرکز", "داو"],
    "RON": ["رونین"],
    "QNT": ["کیوان", "کوانت"],
    "PDA": ["کیف پول"],
    "WIN": ["وینک"],
    "DASH": ["دش"],
    "LUNA": ["ترا"],
    "ARV": ["آروین"],
    "FET": ["فوتی", "فچ"],
    "BAND": ["بند پروتکل"],
    "TWT": ["تراست والت"],
    "USDC": ["یو اس دی کوین"],
    "DAI": ["دای"],
    "AAVE": ["آوه"],
    "SUI": ["سویی"],
    "OP": ["آپتیمیسم"],
    "ARB": ["آربیتریم", "آربیتروم"],
    "ENS": ["خدمات نام اتریوم", "اتریوم نیم سرویس"],
    "PEPE": ["پپه"],
    "HNT": ["هلیوم"],
    "KSM": ["کوزاما"],
    "SAND": ["ساند باکس", "سند باکس"],
    "BLUR": ["بلور"],
    "FET": ["فچ.ای آی"],
    "PUNDIX": ["پاندی ایکس"],
    "STMX": ["استورم ایکس"],
    "LDO": ["لیدو د آو", "لیدو دائو"],
    "KAVA": ["کاوا"],
    "SYN": ["سیناپس"],
    "BTT": ["بیت تورنت"],
    "QTUM": ["کوتوم"],
    "1INCH": ["یک اینچ", "1اینچ"],
    "XEM": ["نِم"],
    "XDC": ["شبکه ایکس دی سی"],
    "FLOKI": ["فلوکی اینو"],
    "ICP": ["کامپیوتر اینترنتی"],
    "WAVES": ["ویوز"],
    "AUDIO": ["آدیوس"],
    "CELO": ["سلو"],
    "BAT": ["توکن توجه اساسی", "بریو توکن"],
    "GRT": ["گراف"],
    "EGLD": ["الران"],
    "GAL": ["گالا"],
    "WBTC": ["رپد بیت‌کوین"],
    "IMX": ["ایموتبل ایکس"],
    "GLM": ["گولم"],
    "SUSHI": ["سوشی‌سواپ"],
    "ZRO": ["زیرو ایکس"],
    "STORJ": ["استورج"],
    "ANT": ["آراگون"],
    "AEVO": ["آوو"],
    "RSR": ["ریزر"],
    "API3": ["ای‌پی‌آی ۳"],
    "OM": ["مانتا دائو"],
    "RDNT": ["رادیانت"],
    "MAGIC": ["مجیک"],
    "T": ["ترا"],
    "RBTC": ["راکی","رابیت","راکی رابیت"],
    "X": ["ایکس امپایر","ایکس","ماسک","ماسک ایمپایر","امپایر","ایمپایر"],
    "CVX": ["کانویکس فایننس"],
    "UMA": ["یو‌ام‌ای"],
    "SSV": ["اس‌اس‌وی نتورک"],
    "FLOW": ["فلو"],
    "CVC": ["سیویک"],
    "NMR": ["نومریر"],
    "SKL": ["اسکیل نتورک"],
    "SNT": ["استاتوس"],
    "TRB": ["تلور"],
    "WLD": ["ورلد‌کوین"],
    "YFI": ["یرن فایننس"],
    "MATIC": ["ماتیک"],
    "FET": ["فچ","فت"],
    "AGIX": ["سینگولاریتی‌نت"],
    "LPT": ["لایوپییر"],
    "SLP": ["اسموث لاو پوشن"],
    "MEME": ["میم کوین"],
    "BAL": ["بلنسر"],
    "NOT": ["نات","نات‌کوین","نات کوین","ناتکوین"],
    "TON": ["تون‌کوین", "تون", "تون کوین"],
    "TRX": ["ترون"],
    "DOGS": ["داگز"],
    "CATS": ["کتز"],
    "HMSTR": ["همستر"],
    "CATI": ["کتیژن","کتیزن"],
    "THETA": ["تتا"],
    "ZIL": ["زیلیکا"],
    "OMG": ["اومیسه گو"],
    "ANKR": ["انکر"],
    "ACH": ["آلکمی پی"],
    "APE": ["ایپ کوین"],
    "APT": ["اپتوس"],
    "ASTR": ["استار"],
    "BICO": ["بیکونومی"],
    "BOSON": ["بوسون پروتکل"],
    "BTRST": ["برینتراست"],
    "CLV": ["کلوور فایننس"],
    "COTI": ["کوتی"],
    "FORTH": ["امپلفورث"],
    "LRC": ["لوپرینگ"],
    "NANO": ["نانو"],
    "OCEAN": ["اوشن پروتکل"],
    "WAT": ["وات","وات کوین","واتکوین"],
    "RUNE": ["تورچین"]
}


def format_toman_amount(amount):
    return f"{amount / 10:,.0f}"


# تابع بن کردن کاربر
def ban_user(user_id):
    banned_users.add(user_id)
 # لاگ برای بررسی

def unban_user(user_id):
    banned_users.discard(user_id)

# تابع چک اسپم
def handle_spam_check(user_id, message_text):
    # اگر پیام شامل کلمات خطرناک باشد، True برمی‌گرداند
    if re.search(r"(eval|exec|import os|subprocess|__)", message_text):
        return True
    return False
    

# چک کردن پیام برای کلمات کلیدی خطرناک

    for exchange, get_price_func in exchanges.items():
        price = get_price_func(symbol)
        if price:
            return price, exchange  # بازگرداندن قیمت و نام صرافی

    return None, None  # اگر ارز در هیچ صرافی موجود نبود
    

def get_crypto_symbol(user_input):
    """یافتن نماد ارز بر اساس نام ورودی"""
    for symbol, names in crypto_dict.items():
        if user_input in names:
            return symbol
    return user_input  

def update_price(message, symbol, quantity):
    price_per_unit, change_24h, exchange = get_price_from_all_exchanges(symbol)
    if price_per_unit is None:
        return
    
def get_price_usdt_nobitex():
    try:
        url = "https://api.nobitex.ir/v3/orderbook/USDTIRT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()


        if 'lastTradePrice' in data:
            return float(data['lastTradePrice']) / 10  
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_price_from_exchange(symbol):
    """دریافت قیمت از صرافی‌ها."""
    price, exchange = get_price_from_all_exchanges(symbol)  # تابع شما برای دریافت قیمت از صرافی‌ها
    return price, exchange

def get_price_usdt():
    try:
        response = requests.get("https://api.nobitex.ir/v3/orderbook/USDTIRT")
        data = response.json()
        return float(data['lastTradePrice']) if 'lastTradePrice' in data else None
    except Exception:
        return None

def calculate_total_price(price_per_unit, quantity):
    return price_per_unit * quantity

def get_price_shiba_nobitex():
    try:
        url = "https://api.nobitex.ir/v3/orderbook/SHIBUSDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()


        if 'lastTradePrice' in data:
            return float(data['lastTradePrice'])  
        else:
            return None
    except requests.exceptions.RequestException:
        return None


@app.on_message(filters.text & filters.regex(r"^(تتر|قیمت تتر|شیبا|قیمت شیبا|شیبا اینو|\d+\s*(شیبا|تتر))$", re.IGNORECASE))
def send_price(client, message):
    user_input = message.text.strip()

    # بررسی برای یافتن تعداد و نام ارز
    match = re.search(r"(\d+)\s*(شیبا|تتر)", user_input)

    if match:
        # حالتی که تعداد مشخص شده باشد
        quantity = int(match.group(1))
        currency = match.group(2)

        if currency == "شیبا":
            shiba_price_usdt = get_price_shiba_nobitex()  
            usdt_price_toman = get_price_usdt_nobitex()  
            if shiba_price_usdt and usdt_price_toman:
                total_price_usdt = shiba_price_usdt * quantity
                total_price_toman = total_price_usdt * usdt_price_toman
                message.reply(f"⭕️ {quantity} شیبا\n"
                              f"🟡 قیمت کل به دلار: {total_price_usdt:.4f} USDT\n"
                              f"🟡 قیمت کل به تومان: {total_price_toman:,.0f} تومان")
            else:
                message.reply("خطا در دریافت قیمت شیبا ❌")

        elif currency == "تتر":
            usdt_price = get_price_usdt_nobitex()
            if usdt_price:
                total_price = usdt_price * quantity
                message.reply(f"⭕️ {quantity} تتر\n"
                              f"🟡 قیمت کل به تومان: {total_price:,.0f} تومان")
            else:
                message.reply("خطا در دریافت قیمت تتر ❌")
    else:
        # حالتی که تعداد مشخص نشده و تنها اسم ارز آمده باشد
        if "شیبا" in user_input:
            shiba_price_usdt = get_price_shiba_nobitex()  
            usdt_price_toman = get_price_usdt_nobitex()  
            if shiba_price_usdt and usdt_price_toman:
                shiba_price_toman = shiba_price_usdt * usdt_price_toman  
                message.reply(f"🟢 قیمت شیبا: {shiba_price_usdt:.4f} USDT ({shiba_price_toman:,.0f} تومان) ")
            else:
                message.reply("خطا در دریافت قیمت شیبا ❌")

        elif "تتر" in user_input:
            usdt_price = get_price_usdt_nobitex()
            if usdt_price:
                message.reply(f"🟢 قیمت تتر: {usdt_price:,.0f} تومان ")
            else:
                message.reply("خطا در دریافت قیمت تتر ❌")


def get_price_from_binance(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = float(data['lastPrice']) if 'lastPrice' in data else None
        change_24h = float(data['priceChangePercent']) if 'priceChangePercent' in data else None
        return price, change_24h
    except:
        return None, None

def get_price_from_kucoin(symbol):
    try:
        url = f"https://api.kucoin.com/api/v1/market/stats?symbol={symbol}-USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = float(data['data']['last']) if 'data' in data and 'last' in data['data'] else None
        change_24h = float(data['data']['changeRate']) * 100 if 'data' in data and 'changeRate' in data['data'] else None
        return price, change_24h
    except:
        return None, None

def get_price_from_gateio(symbol):
    try:
        url = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={symbol}_USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = float(data[0]['last']) if len(data) > 0 else None
        change_24h = float(data[0]['change_percentage']) if len(data) > 0 and 'change_percentage' in data[0] else None
        return price, change_24h
    except:
        return None, None

def get_price_from_okx(symbol):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = float(data['data'][0]['last']) if 'data' in data else None
        change_24h = float(data['data'][0]['changePercent']) if 'data' in data and 'changePercent' in data['data'][0] else None
        return price, change_24h
    except:
        return None, None

# دریافت قیمت از تمامی صرافی‌ها
def get_price_from_all_exchanges(symbol):
    price, change_24h = get_price_from_binance(symbol)
    if price:
        return price, change_24h, "Binance"

    price, change_24h = get_price_from_kucoin(symbol)
    if price:
        return price, change_24h, "KuCoin"

    price, change_24h = get_price_from_gateio(symbol)
    if price:
        return price, change_24h, "Gate.io"

    price, change_24h = get_price_from_okx(symbol)
    if price:
        return price, change_24h, "OKX"

    return None, None, None

def get_price_binance(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['price']) if 'price' in data else None
    except requests.exceptions.RequestException:
        return None

def get_price_kucoin(symbol):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['data']['price']) if 'data' in data and 'price' in data['data'] else None
    except requests.exceptions.RequestException:
        return None

def get_price_gateio(symbol):
    try:
        url = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={symbol}_USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data[0]['last']) if len(data) > 0 and 'last' in data[0] else None
    except requests.exceptions.RequestException:
        return None

def get_price_okx(symbol):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['data'][0]['last']) if 'data' in data and len(data['data']) > 0 else None
    except requests.exceptions.RequestException:
        return None

def get_exchange_rate_nobitex():
    try:
        url = "https://api.nobitex.ir/v3/orderbook/USDTIRT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['lastTradePrice']) if 'lastTradePrice' in data else None
    except requests.exceptions.RequestException:
        return None


def get_price_shiba_nobitex():
    try:
        url = "https://api.nobitex.ir/v3/orderbook/SHIBUSDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['lastTradePrice']) if 'lastTradePrice' in data else None
    except requests.exceptions.RequestException:
        return None


def get_price(symbol):
    try:
        url = f"https://api.nobitex.ir/v3/orderbook/{symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['lastTradePrice']) if 'lastTradePrice' in data else None
    except requests.exceptions.RequestException:
        return None

def calculate_gold_price_per_gram(final_price_toman, discount_percent=0.40):
    """محاسبه قیمت هر گرم طلای 24 عیار بر اساس قیمت نهایی و تبدیل از اونس به گرم."""
    price_per_gram_24 = final_price_toman / 31.1035  
    return price_per_gram_24 * (1 - discount_percent)  

def calculate_price_by_carat(price_per_gram_24, carat, discount_percent=0.0):
    """محاسبه قیمت هر گرم طلا بر اساس عیار مشخص."""
    return price_per_gram_24 * (carat / 24) * (1 - discount_percent)  

def calculate_second_hand_gold(price_per_gram_18, discount_percent=0.01):
    """محاسبه قیمت طلای دست دوم بر اساس قیمت هر گرم طلا 18 عیار و اعمال تخفیف."""
    second_hand_price = (price_per_gram_18 * 740) / 742
    return second_hand_price * (1 - discount_percent) 

def calculate_gold_22(price_per_gram_24, discount_percent=0.0):
    """محاسبه قیمت هر گرم طلای 22 عیار از 24 عیار با امکان تخفیف."""
    price_per_gram_22 = price_per_gram_24 * (22 / 24)
    return price_per_gram_22 * (1 - discount_percent)  

def calculate_gold_21(price_per_gram_24, discount_percent=0.0):
    """محاسبه قیمت هر گرم طلای 21 عیار از 24 عیار با امکان تخفیف."""
    price_per_gram_21 = price_per_gram_24 * (21 / 24)
    return price_per_gram_21 * (1 - discount_percent)  

def calculate_gold_18(price_per_gram_24):
    """محاسبه قیمت هر گرم طلای 18 عیار از قیمت طلای 24 عیار."""
    return price_per_gram_24 * 0.743  
    

def calculate_gold_17(price_per_gram_24, discount_percent=0.0):
    """محاسبه قیمت هر گرم طلای 17 عیار از 24 عیار با امکان تخفیف."""
    price_per_gram_17 = price_per_gram_24 * (17 / 24)
    return price_per_gram_17 * (1 - discount_percent)  

def calculate_bahar_azadi(price_per_gram_24):
    """محاسبه قیمت سکه بهار آزادی بر اساس قیمت هر گرم طلای 24 عیار."""
    weight_bahar_azadi = 8.02  
    return price_per_gram_24 * weight_bahar_azadi 

def calculate_seke_nim(price_per_gram_24):
    """محاسبه قیمت نیم سکه بر اساس قیمت هر گرم طلای 24 عیار."""
    weight_nim_seke = 4.85  
    return price_per_gram_24 * weight_nim_seke  

def calculate_seke_rub(price_per_gram_24):
    """محاسبه قیمت ربع سکه بر اساس قیمت هر گرم طلای 24 عیار."""
    weight_rub_seke = 3.1712  
    return price_per_gram_24 * weight_rub_seke  

def calculate_seke_garmi(price_per_gram_24):
    """محاسبه قیمت سکه گرمی بر اساس قیمت هر گرم طلای 24 عیار."""
    weight_garmi_seke = 1.452  
    return price_per_gram_24 * weight_garmi_seke  

def format_toman_amount(amount):
    """کم کردن یک صفر از قیمت برای نمایش در تومان."""
    return f"{amount / 10:,.0f}"  

@app.on_message(filters.text & filters.regex(r"^(طلا|سکه|نرخ طلا|قیمت طلا)$", re.IGNORECASE))
def main_gold(client, message):

    paxg_price_toman = get_price('PAXGIRT') 
    xaut_price_toman = get_price('XAUTIRT')  
    

    if paxg_price_toman is None and xaut_price_toman is None:
        message.reply("خطا در دریافت قیمت طلا ❌")
        return


    final_price_toman = (paxg_price_toman + xaut_price_toman) / 2


    discount_percent = 0.0019
    price_per_gram_24 = calculate_gold_price_per_gram(final_price_toman, discount_percent)


    price_per_gram_17 = calculate_gold_17(price_per_gram_24)
    price_per_gram_18 = calculate_gold_18(price_per_gram_24)
    price_per_gram_21 = calculate_gold_21(price_per_gram_24)
    price_per_gram_22 = calculate_gold_22(price_per_gram_24)


    bahar_azadi_price = calculate_bahar_azadi(price_per_gram_24)  
    nim_sekeh_price = calculate_seke_nim(price_per_gram_24) 
    rub_e_sekeh_price = calculate_seke_rub(price_per_gram_24)  
    sekkeh_germi_price = calculate_seke_garmi(price_per_gram_24)  


    second_hand_price = calculate_second_hand_gold(price_per_gram_18)


    response_message = (f"🟡 قیمت هر گرم طلای 24 عیار: \n"
                        f" [ {format_toman_amount(price_per_gram_24)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🟡 قیمت هر گرم طلای 22 عیار: \n"
                        f" [ {format_toman_amount(price_per_gram_22)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🟡 قیمت هر گرم طلای 21 عیار: \n"
                        f" [ {format_toman_amount(price_per_gram_21)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🟡 قیمت هر گرم طلای 18 عیار: \n"
                        f" [ {format_toman_amount(price_per_gram_18)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🟡 قیمت هر گرم طلای 17 عیار: \n"
                        f" [ {format_toman_amount(price_per_gram_17)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🟢 قیمت طلای دست دوم: \n"
                        f" [ {format_toman_amount(second_hand_price)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🔴 قیمت سکه بهار آزادی: \n"
                        f" [ {format_toman_amount(bahar_azadi_price)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🔴 قیمت نیم سکه: \n"
                        f" [ {format_toman_amount(nim_sekeh_price)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🔴 قیمت ربع سکه: \n"
                        f" [ {format_toman_amount(rub_e_sekeh_price)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                        f"🔴 قیمت سکه گرمی: \n"
                        f" [ {format_toman_amount(sekkeh_germi_price)} 𝙏𝙊𝙈𝘼𝙉 ] \n")

    message.reply(response_message)

@app.on_message(filters.text)
def handle_requests(client, message):
    user_id = message.from_user.id
    message_text = message.text.strip()

    # بررسی اگر کاربر بن شده باشد
    if user_id in banned_users:
        return  # پیام کاربر بن‌شده پردازش نمی‌شود

    # چک اسپم: اگر پیام مشکوک باشد، به ادمین گزارش می‌دهد و پیام را نادیده می‌گیرد
    if handle_spam_check(user_id, message_text):
        client.send_message(ADMIN_USER_ID, f"پیام مشکوک از کاربر {message.from_user.username}:\n{message_text}")
        return  

    # بررسی برای یافتن تعداد و نام ارز با استفاده از حروف فارسی و انگلیسی
    match = re.search(r"(\d+)\s*([a-zA-Z]+|[\u0600-\u06FF]+)", message_text)
    match_reverse = re.search(r"([a-zA-Z]+|[\u0600-\u06FF]+)\s*(\d+)", message_text)

    if (match or match_reverse) and not re.search(r"[^a-zA-Z0-9\s\u0600-\u06FF]", message_text):
        if match:
            quantity = int(match.group(1))
            currency_input = match.group(2).strip()
        else:
            quantity = int(match_reverse.group(2))
            currency_input = match_reverse.group(1).strip()

        symbol = get_crypto_symbol(currency_input.upper())

        # دریافت قیمت از صرافی
        price_per_unit, change_24h, exchange = get_price_from_all_exchanges(symbol)

        if price_per_unit is None:
            message.reply("ارز مورد نظر یافت نشد.")
            return

        price_usdt = get_price_usdt()  # دریافت قیمت تتر به تومان

        # محاسبه قیمت کل
        total_price_usd = round(price_per_unit * quantity, 3)
        total_price_toman = total_price_usd * price_usdt

        message.reply(f"⭕️ {quantity} [ {currency_input} ] \n"
                      f"🟡  [ {total_price_usd} 𝙐𝙎𝘿𝙏 ] \n"
                      f"🟡  [ {format_toman_amount(total_price_toman)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                      f"🔼 درصد تغییرات: {change_24h}% \n"
                      f"🟡 این قیمت از صرافی • {exchange} • گرفته شده است.")
                      
    elif message_text.isalpha() or re.match(r"^[a-zA-Z\u0600-\u06FF]+$", message_text):
        symbol = get_crypto_symbol(message_text)
        price_binance, change_binance = get_price_from_binance(symbol)
        price_kucoin, change_kucoin = get_price_from_kucoin(symbol)
        price_gateio, change_gateio = get_price_from_gateio(symbol)
        price_okx, change_okx = get_price_from_okx(symbol)

        price_usdt = get_price_usdt()

        response_message = f"⭕️ قیمت لحظه‌ای [ {symbol} ]"

        if price_binance is not None:
            price_toman = price_binance * price_usdt
            response_message += (f"\n🟡 - 𝘽𝙄𝙉𝘼𝙉𝘾𝙀: \n"
                                 f"       - {price_binance} 𝙐𝙎𝘿𝙏 [ {format_toman_amount(price_toman)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                                 f"       🔼 درصد تغییرات: {change_binance}%")
        if price_kucoin is not None:
            price_toman = price_kucoin * price_usdt
            response_message += (f"\n🟡 - 𝙆𝙐𝘾𝙊𝙄𝙉: \n"
                                 f"       - {price_kucoin} 𝙐𝙎𝘿𝙏 [ {format_toman_amount(price_toman)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                                 f"       🔼 درصد تغییرات: {change_kucoin}%")
        if price_gateio is not None:
            price_toman = price_gateio * price_usdt
            response_message += (f"\n🟡 - 𝙂𝘼𝙏𝙀.𝙄𝙊: \n"
                                 f"       - {price_gateio} 𝙐𝙎𝘿𝙏 [ {format_toman_amount(price_toman)} 𝙏𝙊𝙈𝘼𝙉 ] \n"
                                 f"       🔼 درصد تغییرات: {change_gateio}%")
        if price_okx is not None:
            price_toman = price_okx * price_usdt
            response_message += (f"\n🟡 - 𝙊𝙆𝙓: \n"
                                 f"       - {price_okx} 𝙐𝙎𝘿𝙏 [ {format_toman_amount(price_toman)} 𝙏𝙊𝙈𝘼𝙉 ] \n")

        message.reply(response_message)


@app.on_message(filters.command("ban") & filters.user(ADMIN_USER_ID))
def ban_command(client, message):
    if len(message.command) < 2:
        message.reply("لطفاً شناسه کاربر را وارد کنید.")
        return

    try:
        user_id = int(message.command[1])
        ban_user(user_id)
        message.reply(f"کاربر با شناسه {user_id} بن شد.")
    except ValueError:
        message.reply("شناسه کاربر نامعتبر است.")

# فرمان انبن کردن کاربر
@app.on_message(filters.command("unban") & filters.user(ADMIN_USER_ID))
def unban_command(client, message):
    if len(message.command) < 2:
        message.reply("لطفاً شناسه کاربر را وارد کنید.")
        return

    try:
        user_id = int(message.command[1])
        unban_user(user_id)
        message.reply(f"کاربر با شناسه {user_id} انبن شد.")
    except ValueError:
        message.reply("شناسه کاربر نامعتبر است.")


@app.on_message(filters.text)
def handle_message(client, message):
    user_input = message.text.strip()


@app.on_message(filters.text)
def crypto_price(client, message):
    user_input = message.text.strip()




if __name__ == "__main__":
    app.run()
    
