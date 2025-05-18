import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
TOKEN = os.environ.get("TOKEN")

def format_number(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}k"
    else:
        return str(n)

async def prezenta_actuala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = 'https://g4media.org/g4/prezidentiale18052025/presence/overview.json'
        url2 = 'https://g4media.org/g4/prezidentiale18052025/presence/hourly-extended.json'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'Referer': 'https://prezenta.roaep.ro/ep2025/'
        }

        r = requests.get(url, headers=headers)
        r2 = requests.get(url2, headers=headers)

        date = r.json()
        procent = date['total_pct']
        total = format_number(date['total'])

        date2 = r2.json()
        data = date2[-1]
        procent_vechi = data['past']['total_pct']
        procent_nou = data['now']['total_pct']

        nr_vechi = format_number(data['past']['total'])
        nr_nou = data['now']['total']

        ora = datetime.strptime(data['hour'], "%Y-%m-%d %H:%M:%S").hour

        await update.message.reply_text(f"{procent}% \n{total}\n\nPrezență ora {ora} in 2024:\n{procent_vechi}%\n{nr_vechi} \n")

    except Exception as e:
        await update.message.reply_text(f"Eroare la preluarea datelor: {e}")

async def rezultate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = 'https://g4media.org/g4/prezidentiale04052025/results/national.json'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'Referer': 'https://prezenta.roaep.ro/ep2025/'
        }

        r = requests.get(url, headers=headers)

        date = r.json()

        results = date['results']
        candidates = results['candidates']
        fiirst = candidates[0]
        second = candidates[1]

        name1 = fiirst['shortName']
        name2 = second['shortName']
        votes1 = fiirst['votes']
        votes2 = second['votes']
        total = results['countedVotes']

        await update.message.reply_text(f"{name1} : {round(votes1 / total,2)}%\n{name2} : {round(votes2 / total, 2)}%")

    except Exception as e:
        await update.message.reply_text(f"Eroare la preluarea datelor: {e}")

async def prezenta(application):
    try:
        url = 'https://g4media.org/g4/prezidentiale18052025/presence/hourly-extended.json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'Referer': 'https://prezenta.roaep.ro/ep2025/'
        }
        r = requests.get(url, headers=headers)

        date = r.json()
        data = date[-1]
        procent_vechi = data['past']['total_pct']
        procent_nou = data['now']['total_pct']

        nr_vechi = data['past']['total']
        nr_nou = data['now']['total']

        ora = data['hour']

        await update.message.reply_text(f"Ora: {ora}\nPrezență:\n{procent_nou}% | {nr_nou} {procent_vechi}% | {nr_vechi} (2024) \n")
    except Exception as e:
        await update.message.reply_text(f"Eroare la preluarea datelor: {e}")

async def rara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(f"Ai ceva cu mine ca sunt rarait?")
    except Exception as e:
        await update.message.reply_text(f"Eroare la preluarea datelor: {e}")

async def injura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(f"Cristosu mami lor de suveranisti")
    except Exception as e:
        await update.message.reply_text(f"Eroare la preluarea datelor: {e}")

async def francais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(f"Nous volouns aaaa uuaaaa o incetare a focului")
    except Exception as e:
        await update.message.reply_text(f"Eroare la preluarea datelor: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("p", prezenta_actuala))
    app.add_handler(CommandHandler("r", rara))
    app.add_handler(CommandHandler("f", injura))
    app.add_handler(CommandHandler("t", francais))
    app.add_handler(CommandHandler("w", rezultate))



    print("Botul rulează...")
    app.run_polling()
