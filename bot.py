import logging
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔧 Вставь сюда свой токен от BotFather
import os
TOKEN = os.getenv("TOKEN")

SPREADSHEET_NAME = 'Учет посещений United Triathlon'

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1dkSFxKF9DP1vy6XolzeaRD-QIMS1bmKKiwRbA4GhcpY").sheet1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip().upper()
    data = sheet.get_all_records()

    for i, row in enumerate(data, start=2):
        if str(row["ID"]).strip().upper() == message:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            sheet.update_cell(i, 4, today)
            visits = int(row["Кол-во посещений"]) + 1
            sheet.update_cell(i, 5, visits)

            response = f"✅ {row['Имя']} пришёл! Всего посещений: {visits}"
            await update.message.reply_text(response)
            return

    await update.message.reply_text("❌ Участник не найден. Проверь QR-код или ID.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
