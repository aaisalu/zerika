import speedtest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage,deleteMessage,sendMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler



def convert(speed):
    return round(int(speed) / 1048576, 2)


def speedtestxyz(update, context):
    buttons = [
        [
            InlineKeyboardButton("Cool Image", callback_data="speedtest_image"),
            InlineKeyboardButton("Preety Text", callback_data="speedtest_text"),
        ]
    ]
    update.effective_message.reply_text(
        "🛠 Select SpeedTest Mode", reply_markup=InlineKeyboardMarkup(buttons)
    )


def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"



def speedtestxyz_callback(update, context):
    query = update.callback_query
    msg = update.effective_message.edit_text("📡 Running a speedtest....")
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    replymsg = "⚡️ SpeedTest Results:"
    if query.data == "speedtest_image":
        speedtest_image = speed.results.share()
        update.effective_message.reply_photo(
            photo=speedtest_image, caption=replymsg
        )
        msg.delete()
    elif query.data == "speedtest_text":
        result = speed.results.dict()
        string_speed = f'''
<b>🛠 Zeron Server</b>
<b>Name:</b> <code>{result['server']['name']}</code>
<b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
<b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
<b>ISP:</b> <code>{result['client']['isp']}</code>

<b>SpeedTest Results</b>
<b>Upload:</b> <code>{speed_convert(result['upload'] / 8)}</code>
<b>Download:</b>  <code>{speed_convert(result['download'] / 8)}</code>
<b>Ping:</b> <code>{result['ping']} ms</code>
<b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
        # string_speed += f"\nDownload: `{convert(result['download'])}Mb/s`\nUpload: `{convert(result['upload'])}Mb/s`\nPing: `{result['ping']}`"
        # update.effective_message.edit_text(string_speed)

        editMessage(string_speed, msg)



SPEED_HANDLER = CommandHandler(BotCommands.SpeedCommand, speedtestxyz,
                                                  filters=CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
Speed_result_handler = CallbackQueryHandler(speedtestxyz_callback, pattern="speedtest_.*", run_async=True)

dispatcher.add_handler(SPEED_HANDLER)
dispatcher.add_handler(Speed_result_handler)