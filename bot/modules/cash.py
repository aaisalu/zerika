from telegram.ext import CallbackContext, CommandHandler, run_async
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup,editMessage, deleteMessage, delete_all_messages, update_all_messages, sendStatusMessage


import requests
from bot import CASH_API_KEY


def convert(update, context):
    chat = update.effective_chat
    args = update.effective_message.text.split(" ")
    look= 'Usages: Eg: /paisa 1 USD EGP 🦊 /paisa 1 usd inr'


    if len(args) == 4:
        try:
            orig_cur_amount = float(args[1])

        except ValueError:
            update.effective_message.reply_text(f"Invalid  currency {look}")
            return

        orig_cur = args[2].upper()

        new_cur = args[3].upper()

        request_url = (
            f"https://www.alphavantage.co/query"
            f"?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={orig_cur}"
            f"&to_currency={new_cur}"
            f"&apikey={CASH_API_KEY}"
        )
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["Exchange Rate"]["5. Exchange Rate"]
            )
        except KeyError:
            update.effective_message.reply_text(f"not supported.  {look}")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        delmsg = update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}"
        )

    else:
        delmsg = update.effective_message.reply_text(
            f" {len(args) -1}  {look}"
        )


CASH_HANDLER = CommandHandler(BotCommands.cashCommand, convert, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(CASH_HANDLER)
