# -*- coding: utf-8 -*-

import telebot
import os
import json
import codecs

import auth as AUTH

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text)
    AUTH.AuthUser(message,bot)

bot.polling()