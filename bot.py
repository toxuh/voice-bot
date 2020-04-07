import telebot
import urllib.request
import json
import tokens

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['voice'])
def default_command(message):
  filepath = bot.get_file(message.voice.file_id)
  urllib.request.urlretrieve("https://api.telegram.org/file/bot" + tokens.TOKEN + "/" + filepath.file_path, 'audio.oga')
  with open("audio.oga", "rb") as f:
    data = f.read()

  params = "&".join([
      "topic=general",
      "folderId=%s" % tokens.FOLDER_ID,
      "lang=ru-RU"
  ])

  url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
  url.add_header("Authorization", "Bearer %s" % tokens.IAM_TOKEN)

  print(url)

  responseData = urllib.request.urlopen(url).read().decode('UTF-8')
  decodedData = json.loads(responseData)

  if decodedData.get("error_code") is None:
    bot.reply_to(message, decodedData.get("result"))

bot.polling(none_stop=True, interval=0)
