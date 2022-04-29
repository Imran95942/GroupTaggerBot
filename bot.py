import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

from pyrogram.types.messages_and_media import Message
from pyrogram import Client, filters
import time


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

app = Client("GUNC",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token
             )


anlik_calisan = []

ozel_list = [5074483091]
anlik_calisan = []
grup_sayi = []
tekli_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**@CemileTaggerBot 🌀 Salam, Mən sənin əvəzinə qrupdaki istifadəçiləri tağ edə bilərəm ✔️ Əvvəlcə məni qrupa əlavə et və admin et ❗ Admin olmadan bot işləməyəcək əmrlərlə tanış olmaq üçün  /help toxunun**'.", buttons=(
    
                  [Button.url('➕Məni Qrupa Əlave Et', 'https://t.me/CemileTaggerBot?startgroup=a'),
                  Button.url('Botlarımız🤖', 'https://t.me/loungesupport'),
                  Button.url('Sahib', 'https://t.me/HuseynH')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**@CemileTaggerBot Əmrlər**\n\n**/tag <səbəb> - 5 Teq Atır**\n\n**/etag <səbəb> - Emojili teqlər**\n\n**/tektag səbəbi - Üzvlərin Fərdi Teqləri **\n\n**/admins səbəbi - Adminləri Fərdi olaraq Taqlayın**\n\n**/start - botu işə salır**"
  await event.reply(helptext,
                    buttons=(
		      [Button.url('Sahib🧑‍🔧', 'https://t.me/HuseynH')],
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/tektag ?(.*)"))
async def tektag(event):
  global tekli_calisan
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə mesajları görə bilmirəm! (bu mesaj məni qrupa əlavə etməmişdən qabaq yazılıb)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Tağ mesajı yazmadın!__")
  else:
    return await event.respond("__Tağ etməy üçün bir mesaj yanıtlayın və ya bir mətn yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Tək-Tək Tağ Başladı\n⏱️ İnterval - 2 saniyə",
                    buttons=(
                      [
                      Button.inline(f"{dayandir}", data="cancel")
                      ]
                    )
                  ) 
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("⛔ Tək Tək Tağ Prosesi Dayandırıldı",
                    buttons=(
                      [
                      Button.inline(f"{yeniden}", data="yeniden")
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


### istatistik 

@client.on(events.NewMessage())
async def mentionalladmin(event):
  global grup_sayi
  if event.is_group:
    if event.chat_id in grup_sayi:
      pass
    else:
      grup_sayi.append(event.chat_id)

@client.on(events.NewMessage(pattern='^/botstatik ?(.*)'))
async def son_durum(event):
    global anlik_calisan,grup_sayi,ozel_list
    sender = await event.get_sender()
    if sender.id not in ozel_list:
      return
    await event.respond(f"**Gece kuşu Tagger İstatistikleri 🤖**\n\nToplam Grup: `{len(grup_sayi)}`\nAnlık Çalışan Grup: `{len(anlik_calisan)}`")
 

### brokcast modülü

@client.on(events.NewMessage(pattern='^/botreklam ?(.*)'))
async def duyuru(event):
 
  global grup_sayi,ozel_list
  sender = await event.get_sender()
  if sender.id not in ozel_list:
    return
  reply = await event.get_reply_message()
  await event.respond(f"Toplam {len(grup_sayi)} Gruba'a mesaj gönderiliyor...")
  for x in grup_sayi:
    try:
      await client.send_message(x,f"**📣 Sponsor**\n\n{reply.message}")
    except:
      pass
  await event.respond(f"Gönderildi.")


#### botcum modülü

@app.on_message(filters.user(5074483091) & filters.command(["botcum"], ["."]))
def admin(_, message: Message):
    message.reply(f"__Biricik Sahibim Gelmiş Hoşgeldin Efendim 💋 Muck__")


app.run()
print(">> Bot çalışıyor <<")
client.run_until_disconnected()
