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
