from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, JobQueue
from tradingview_ta import TA_Handler, Interval

# توکن ربات تلگرام
TOKEN = '7845147162:AAHOezezZ_V9Uu9Uizk_yuvqvd-j-Y_KAI0'

# شناسه کانال (برای ارسال خودکار قیمت به کانال)
CHANNEL_ID = '@GoldAlertUpdatesbot'

# آدرس تلگرام پشتیبانی
SUPPORT_USERNAME = 'xmrtraderx'

# تابع دریافت قیمت لحظه‌ای طلا از TradingView
def get_gold_price():
    gold_handler = TA_Handler(
        symbol="XAUUSD",
        screener="forex",      # برای جفت ارزها و فلزات
        exchange="FX_IDC",     # یکی از منابع معاملاتی TradingView برای قیمت طلا
        interval=Interval.INTERVAL_1_HOUR  # بازه زمانی
    )
    analysis = gold_handler.get_analysis()
    price = analysis.indicators["close"]
    return f"قیمت لحظه‌ای انس طلا: {price} دلار آمریکا"

# تابع شروع و نمایش دکمه‌ها
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📈 نمایش لحظه‌ای قیمت طلا", callback_data='gold_price')],
        [InlineKeyboardButton("💬 پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

# تابع مدیریت کلیک روی دکمه‌ها
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'gold_price':
        price_text = get_gold_price()
        query.edit_message_text(text=price_text)

# تابع برای ارسال خودکار قیمت طلا به کانال
def send_gold_price(context: CallbackContext):
    price_text = get_gold_price()
    context.bot.send_message(chat_id=CHANNEL_ID, text=price_text)

# تابع اصلی برای شروع ربات
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # مدیریت فرمان‌های ربات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # تنظیم ارسال خودکار قیمت طلا هر ساعت به کانال
    job_queue = updater.job_queue
    job_queue.run_repeating(send_gold_price, interval=3600, first=10)  # هر ساعت

    # شروع به کار ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
