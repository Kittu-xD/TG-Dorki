import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import re
import requests

BOT_TOKEN = "Your Bot token here!"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I'm a search bot. Send me a query to get started!")

edmemesIDs = [admin IDs here(comma separated)]

def search(update, context):
    query = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id not in edmemesIDs:
        context.bot.send_message(chat_id=chat_id, text="Sorry, you are not authorized to use this bot. Contact @FullNoob_xD to get your access!")
        return

    with requests.Session() as session:
        session.headers.update({"User-Agent": USER_AGENT})
        start = 0
        while True:
            url = f"https://search.earthlink.net/search-api/?q={query}&num=50&start={start}&lr=lang_en&oe=utf-8"
            try:
                response = session.get(url)
                response.raise_for_status()
            except requests.RequestException as exc:
                context.bot.send_message(chat_id=chat_id, text=f"Error fetching {url}: {exc}")
                break
            results = re.findall('"U":"(.+?)"', response.text)
            context.bot.send_message(chat_id=chat_id, text=f"Found {len(results)} results!!")
            if not results:
                break
            for result in results:
                context.bot.send_message(chat_id=chat_id, text=f"[+] {result}")
            start += 50
            context.bot.send_message(chat_id=chat_id, text="-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-҉҉-")
            if context.bot.send_message(chat_id=chat_id, text="[+] Enter 1 for next page Results || Enter new query to search: ").text != '1':
                break
    context.bot.send_message(chat_id=chat_id, text="[+] Process finished!!!")

if __name__ == '__main__':
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), search))
    print("Bot is UP!")

    updater.start_polling()
    updater.idle()

