# -*- coding: utf-8 -*-
# bot_send_file.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = "8561891128:AAFtmm1AOxwGorMnrRk_35qd3zh0tiuANb0"

# Misol: kino kodi -> local fayl yo'li
movies = {
    "124": "movies/inception.mp4",
    "125": "movies/avatar.mp4",
    "126": "movies/the_matrix.mp4"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Kino botga xush kelibsiz.\n"
        "Kino ko'rmoqchi bo'lsangiz, kino kodini yuboring."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input in movies:
        path = movies[user_input]
        if not os.path.isfile(path):
            await update.message.reply_text("Kechirasiz, fayl serverda topilmadi.")
            return

        # Fayl hajmi va Telegram cheklovlarini tekshirish foydali:
        size_mb = os.path.getsize(path) / (1024*1024)
        # Telegram bot API cheklovi (odatda ~50 MB) borligini yodda tuting.
        if size_mb > 50:
            await update.message.reply_text(
                f"Fayl juda katta ({size_mb:.1f} MB). "
                "Iltimos, faylni qisqartiring yoki hostingga yuklab, link yuboring."
            )
            return

        # Faylni yuborish (video bo'lsa send_video, umumiy fayllar uchun send_document)
        try:
            # Video sifatida yuborish (agar video bo'lsa)
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(path, "rb"))
            # yoki hujjat sifatida yuborish:
            # await context.bot.send_document(chat_id=update.effective_chat.id, document=open(path, "rb"))
        except Exception as e:
            await update.message.reply_text(f"Fayl yuborishda xatolik: {e}")
    else:
        await update.message.reply_text("Kechirasiz, bunday kino kodi mavjud emas.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()