from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands

from bot.helper.telegram_helper.message_utils import editMessage, sendMessage, sendMarkup
from telegram.ext import CommandHandler, CallbackContext, run_async
from bot.helper.telegram_helper import button_build

import requests,hashlib,sys
import threading 


def apiask(ask_api):
	url = 'https://api.pwnedpasswords.com/range/' +ask_api
	got_api=requests.get(url)
	if got_api.status_code !=200:
		return "SOORY ERROR OUT due to excess Resonse Status over 200"
	return  got_api

def encrypt(passkey):
	po=hashlib.sha1(passkey.encode("utf-8")).hexdigest().upper()
	sha1,sha2=po[:5],po[5:]
	call_darling=apiask(sha1)
	return loop(call_darling,sha2)

def loop(first,last):
	split1=(k.split(":") for k in first.text.splitlines())
	for frst,lst in split1:
		if frst==last:
			return lst
	return 0


def say(update, context):
	message = update.effective_message
	say_pass = message.text[len("/key ") :]
	if say_pass:
		call_me=encrypt(say_pass)
		if call_me:
			# msg=f"Your Password is <b><tg-spoiler> {say_pass}</tg-spoiler></b> found in Server for <b>{call_me}</b> times.You should Probably change your password. "
			sendMessage(f"Your Password is <b><tg-spoiler> {say_pass}</tg-spoiler></b> found in Server for <b>{call_me}</b> times.You should Probably change your password. ", context.bot, update)
		else:
			# msg=f"Your Password is <b><tg-spoiler> {say_pass}</tg-spoiler></b> Not found in Server. Nice Password darling."
			sendMessage(f"Your Password is <b><tg-spoiler> {say_pass}</tg-spoiler></b> Not found in Server. Nice Password darling.", context.bot, update)
	else:
		msg ="Please type your key.Eg: /key your_password"
		sendMessage(f"{msg}", context.bot, update) 
	

PASSWORD_HANDLER = CommandHandler(BotCommands.keyCommand, say, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(PASSWORD_HANDLER)






