import requests
from telegram.ext import Updater, CommandHandler
import os
import re
from alive import keep_alive



#Define the bot token
TOKEN = os.environ['BOT_TOKEN']

#The function for the /gen command
def gen(update, context):
  #Check if the user has entered the text after /gen
  if update.message.text == '/gen':
    update.message.reply_text(f"Please enter the text after /gen")
    return
  #Get the requested text from the user
  # text = update.message.text.split(' ')[1]
  text = re.sub(r"(^/gen|@.*bot|^/gen@.*bot| )", "", update.message.text)

  #Generating the URL
  url = "https://www.mikropuhe.com/live/generatemp3.asp?t={}".format(text)

  cookies = {
    'live': 'defaultloaded=yes',
    'ASPSESSIONIDAWRRSTBA': 'KBDBMLEAHFDPNNFCDEMAFHNK',
  }

  headers = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language':
    'en-US,en;q=0.9,th-TH;q=0.8,th;q=0.7,zh-HK;q=0.6,zh;q=0.5,zh-CN;q=0.4,zh-TW;q=0.3',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'live=defaultloaded=yes; ASPSESSIONIDAWRRSTBA=KBDBMLEAHFDPNNFCDEMAFHNK',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua':
    '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
  }

  #Fetching the voice file
  response = requests.get(url, cookies=cookies, headers=headers)

  #Sending the voice file
  context.bot.send_voice(chat_id=update.effective_chat.id,
                         voice=response.content)


#Main function
def main():
  keep_alive()
  #Creating updater object
  updater = Updater(TOKEN,use_context=True)
  updater.bot.set_my_commands([("gen","start the bot")])
  #Getting dispatcher
  disp = updater.dispatcher

  #Adding /gen command handler
  gen_handler = CommandHandler('gen', gen)
  disp.add_handler(gen_handler)

  #Start the bot
  updater.start_polling()

  #Run the bot until user presses Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT
  updater.idle()


if __name__ == '__main__':
  main()
