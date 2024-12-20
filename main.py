import os
import telebot
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MODEL_NAME = os.environ.get("MODEL_NAME")

bot = telebot.TeleBot(BOT_TOKEN)
openai_client = OpenAI()

def reply(message):
    return openai_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a very helpful assistant. Speak with the user very politely and friendly, no matter what user says. Always answer in Ukrainian and end your message with a citation by Taras Shevchenko. Provide response as a valid JSON object that contains two keys: `question` (containing the user message) and `response` (containing your response)"
            },
            {
                "role": "user",
                "content": message,
            }
        ]
    ).choices[0].message.content

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, reply("Start"))

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, reply(message.text))


if __name__ == "__main__":
    bot.infinity_polling()
