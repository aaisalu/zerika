from re import match, findall
from threading import Thread, Event
from time import time
from math import ceil
from html import escape
from psutil import virtual_memory, cpu_percent, disk_usage
from requests import head as rhead
from urllib.request import urlopen
from telegram import InlineKeyboardMarkup

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import download_dict, download_dict_lock, STATUS_LIMIT, botStartTime
from bot.helper.telegram_helper.button_build import ButtonMaker

from telegram import Message
from bot import AUTHORIZED_CHATS, SUDO_USERS
from os import remove as osremove, path as ospath, environ

MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

COUNT = 0
PAGE_NO = 1


class MirrorStatus:
    STATUS_UPLOADING = "Uploading...📤"
    STATUS_DOWNLOADING = "Downloading...📥"
    STATUS_CLONING = "Cloning...♻️"
    STATUS_WAITING = "Queued...💤"
    STATUS_FAILED = "Failed 🚫. Cleaning Download..."
    STATUS_PAUSE = "Paused...⛔️"
    STATUS_ARCHIVING = "Archiving...🔐"
    STATUS_EXTRACTING = "Extracting...📂"
    STATUS_SPLITTING = "Splitting...✂️"
    STATUS_CHECKING = "CheckingUp...📝"
    STATUS_SEEDING = "Seeding...🌧"

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time() + self.interval
        while not self.stopEvent.wait(nextTime - time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return '‼️ File too large'

def getDownloadByGid(gid):
    with download_dict_lock:
        for dl in list(download_dict.values()):
            status = dl.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                ]
                and dl.gid() == gid
            ):
                return dl
    return None

def getAllDownload():
    with download_dict_lock:
        for dlDetails in list(download_dict.values()):
            status = dlDetails.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                    MirrorStatus.STATUS_CLONING,
                    MirrorStatus.STATUS_UPLOADING,
                    MirrorStatus.STATUS_CHECKING,
                ]
                and dlDetails
            ):
                return dlDetails
    return None

def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    p_str = '⬤' * cFull
    p_str += '○' * (12 - cFull)
    p_str = f"「{p_str}」"
    return p_str

# def check_idgroup(msg):
#     return bool(id in AUTHORIZED_CHATS or id in SUDO_USERS or id == OWNER_ID)
#     idk = msg.from_user.id
#     say=list(AUTHORIZED_CHATS)
#     for k in str(say).splitlines():
#         for b in str(idk).splitlines():
#             call=(b.replace('[','').replace(']','').split())
#             for j in call:
#                 j
#         sop=(k.replace('[','').replace(']','').replace(' ','').replace('-','').split(','))
#         for am in sop:
#             if j in am:
#                 loprex=f"hello my love {am}" 
#         return loprex


# def check_idgroup(message):
#     id = message.from_user.id
#     return bool(id in AUTHORIZED_CHATS or id in SUDO_USERS or id == OWNER_ID)


def check_idgroup(msg):
    id = msg.from_user.id
    return bool(id in AUTHORIZED_CHATS)

    
def if_oneid(haha,baba,chaha):
    if len(haha)<=1:      
        for line in haha:
            one_id=f'<a href="https://t.me/c/{str(line)[4:]}/{baba}">{chaha}</a>'
            return one_id
    else:
        return ('two',len(haha))

def juneli(message):
    group_username='zeroncell'
    chat_unqid='-1001570004675'
    user_unqname=message.from_user.first_name
    user_unqusername=message.chat.username
    user_unqid=message.from_user.id
    message_unqid = message.reply_to_message.message_id if message.reply_to_message else message.message_id    
    if message.chat.type in ['supergroup','group']:
        if len(AUTHORIZED_CHATS)<=1:      
                # identity = f'<a href="https://t.me/{group_username}/{message_unqid}">{user_unqname}</a>'
                # identity = f'<a href="https://t.me/c/{str(chat_unqid)[4:]}/{message_unqid}">{user_unqname}</a>'
                for line in AUTHORIZED_CHATS:
                    identity=f'<a href="https://t.me/c/{str(line)[4:]}/{message_unqid}">a.{user_unqname}</a>🗿 <code>{user_unqid}</code>'
        else:
            identity=f'<a href="tg://user?id={user_unqid}">b.{user_unqname}</a>🗿 <code>{user_unqid}</code>'
    else:
        identity=f'<a href="tg://user?id={user_unqid}">c.{user_unqname}</a>🗿 <code>{user_unqid}</code>'
    return identity

def get_readable_message():
    with download_dict_lock:
        msg = ""
        dlspeed_bytes = 0
        uldl_bytes = 0
        START = 0
        if STATUS_LIMIT is not None:
            tasks = len(download_dict)
            global pages
            pages = ceil(tasks/STATUS_LIMIT)
            if PAGE_NO > pages and pages != 0:
                globals()['🎰COUNT'] -= STATUS_LIMIT
                globals()['📋PAGE_NO'] -= 1
            START = COUNT

        for index, download in enumerate(list(download_dict.values())[START:], start=1):
            msg += f"<b>🔰 Name:</b> <code>{escape(str(download.name()))}</code>"
            msg += f"\n<b>🎃 Status:</b> <i>{download.status()}</i>"
            msg += f'\n<b>🥷 User :</b> {juneli(download.message)}'
            # msg += f'\n<b>💀 Check :</b> {check_idgroup(download.message)}  '#{juneli(download.message)}
            if download.status() not in [
                MirrorStatus.STATUS_ARCHIVING,
                MirrorStatus.STATUS_EXTRACTING,
                MirrorStatus.STATUS_SPLITTING,
                MirrorStatus.STATUS_SEEDING,
            ]:
                msg += f"\n{get_progress_bar_string(download)} <b>{download.progress()}</b>"
                if download.status() == MirrorStatus.STATUS_CLONING:
                    msg += f"\n<b>🗜 Cloned:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                elif download.status() == MirrorStatus.STATUS_UPLOADING:
                    msg += f"\n<b>🌈 Uploaded:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                else:
                    msg += f"\n<b>🌈 Downloaded:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                msg += f"\n<b>⚡ Speed:</b> {download.speed()} | <b>⏰ETA:</b> {download.eta()}"
                try:
                    msg += f"\n<b>☘ Seeders:</b> {download.aria_download().num_seeders}" \
                           f" | <b>📡 Peers:</b> {download.aria_download().connections}"
                except:
                    pass
                try:
                    msg += f"\n<b>🍀 Seeders:</b> {download.torrent_info().num_seeds}" \
                           f" | <b>❄ Leechers:</b> {download.torrent_info().num_leechs}"
                except:
                    pass
                msg += f"\n<b>☠️ Cancel:</b> <code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            elif download.status() == MirrorStatus.STATUS_SEEDING:
                msg += f"\n<b>🗃 Size: </b>{download.size()}"
                msg += f"\n<b>⚡ Speed: </b>{get_readable_file_size(download.torrent_info().upspeed)}/s"
                msg += f" | <b>🌡 Uploaded: </b>{get_readable_file_size(download.torrent_info().uploaded)}"
                msg += f"\n<b>⏳ Ratio: </b>{round(download.torrent_info().ratio, 3)}"
                msg += f" | <b>⏰ Time: </b>{get_readable_time(download.torrent_info().seeding_time)}"
                msg += f"\n<b>☠️ Cancel:</b> <code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            else:
                msg += f"\n<b>📜 Size: </b>{download.size()}"
            msg += "\n\n"
            if STATUS_LIMIT is not None and index == STATUS_LIMIT:
                break
        total, used, free, _ = disk_usage('.')
        free = get_readable_file_size(free)
        currentTime = get_readable_time(time() - botStartTime)
        bmsg = f"<b>CPU:</b> {cpu_percent()}% | <b>FREE:</b> {free}"
        for download in list(download_dict.values()):
            speedy = download.speed()
            if download.status() == MirrorStatus.STATUS_DOWNLOADING:
                if 'K' in speedy:
                    dlspeed_bytes += float(speedy.split('K')[0]) * 1024
                elif 'M' in speedy:
                    dlspeed_bytes += float(speedy.split('M')[0]) * 1048576
            if download.status() == MirrorStatus.STATUS_UPLOADING:
                if 'KB/s' in speedy:
                    uldl_bytes += float(speedy.split('K')[0]) * 1024
                elif 'MB/s' in speedy:
                    uldl_bytes += float(speedy.split('M')[0]) * 1048576
        dlspeed = get_readable_file_size(dlspeed_bytes)
        ulspeed = get_readable_file_size(uldl_bytes)
        bmsg += f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>UPTIME:</b> {currentTime}"
        bmsg += f"\n<b>DL:</b> {dlspeed}/s 🔻 |  <b>UL:</b> {ulspeed}/s 🔺"
        if STATUS_LIMIT is not None and tasks > STATUS_LIMIT:
            msg += f"<b>Page:</b> {PAGE_NO}/{pages} | <b>Tasks:</b> {tasks}\n"
            buttons = ButtonMaker()
            buttons.sbutton("◀️ Previous", "status pre")
            buttons.sbutton("Next ▶️", "status nex")
            button = InlineKeyboardMarkup(buttons.build_menu(2))
            return msg + bmsg, button
        return msg + bmsg, ""

def turn(data):
    try:
        with download_dict_lock:
            global COUNT, PAGE_NO
            if data[1] == "nex":
                if PAGE_NO == pages:
                    COUNT = 0
                    PAGE_NO = 1
                else:
                    COUNT += STATUS_LIMIT
                    PAGE_NO += 1
            elif data[1] == "pre":
                if PAGE_NO == 1:
                    COUNT = STATUS_LIMIT * (pages - 1)
                    PAGE_NO = pages
                else:
                    COUNT -= STATUS_LIMIT
                    PAGE_NO -= 1
        return True
    except:
        return False

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def is_url(url: str):
    url = findall(URL_REGEX, url)
    return bool(url)

def is_gdrive_link(url: str):
    return "drive.google.com" in url

def is_gdtot_link(url: str):
    url = match(r'https?://.*\.gdtot\.\S+', url)
    return bool(url)

def is_mega_link(url: str):
    return "mega.nz" in url or "mega.co.nz" in url

def get_mega_link_type(url: str):
    if "folder" in url:
        return "folder"
    elif "file" in url:
        return "file"
    elif "/#F!" in url:
        return "folder"
    return "file"

def is_magnet(url: str):
    magnet = findall(MAGNET_REGEX, url)
    return bool(magnet)

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper

def get_content_type(link: str):
    try:
        res = rhead(link, allow_redirects=True, timeout=5)
        content_type = res.headers.get('content-type')
    except:
        content_type = None

    if content_type is None:
        try:
            res = urlopen(link, timeout=5)
            info = res.info()
            content_type = info.get_content_type()
        except:
            content_type = None
    return content_type

