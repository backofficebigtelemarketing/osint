
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

GESTORI = {
    "TIM": "🔥 TIM Power Smart: 100GB + Min/SMS Illimitati a 7,99€/mese\n👉 Attivabile da iliad e virtuali",
    "WindTre": "🔥 WindTre Start: 100GB + Minuti Illimitati a 7,99€/mese\n👉 Solo per nuovi numeri",
    "Vodafone": "🔥 Vodafone Silver: 150GB + Minuti Illimitati a 7,99€/mese\n👉 Per clienti selezionati",
    "Fastweb": "🔥 Fastweb Mobile: 150GB + Minuti/SMS Illimitati a 7,95€/mese\n✅ Nessun costo di attivazione",
    "Optima": "🔥 Optima Super Mobile: 70GB + Minuti Illimitati a 4,95€/mese\n👉 Offerta online",
    "Iliad": "🔥 Iliad Giga 150: 150GB + Minuti/SMS illimitati a 9,99€/mese\n✅ Per tutti i clienti"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(gestore, callback_data=gestore)] for gestore in GESTORI.keys()]
    keyboard.append([InlineKeyboardButton("💬 Contattaci su WhatsApp", url="https://wa.me/393491234567")])
    keyboard.append([InlineKeyboardButton("🌐 Visita il nostro sito", url="https://www.bigtelemarketing.com")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📲 Benvenuto nel *Bot Promozioni Risparmio*!\n\nScegli un operatore per scoprire la promo migliore di oggi:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def show_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    gestore = query.data
    promo = GESTORI.get(gestore, "❌ Nessuna promo trovata per questo gestore.")
    await query.message.reply_text(f"📢 Promo {gestore}:\n\n{promo}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_promo))
    print("✅ Bot avviato.")
    app.run_polling()
