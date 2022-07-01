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