import time
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          CallbackContext)
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from AuthConfig.keys import API_TOKEN
from errror_handler import error_handler
import logging

# It gives you when and why things don't work as expected.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
from chat_action import send_typing_action


@send_typing_action  # for sending typing.. action, define before the function
def start_command(update, context):
    time.sleep(0.5)
    """When user sends start command do these"""
    # For sending a photo to user
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('assets/hello_world.png', 'rb'), )

    # Showing "typing..." action

    # For sending a message
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello buddy👋 Welcome to our 'theteam' bot.")


# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def unknown(update, context):
    """Defines unknown commands and report them to user
    It should be added last part of bot. Otherwise it may be ignored the commands which are written after this"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def request_location_contact(update, context):
    location_keyboard = KeyboardButton(text="send_location", request_location=True)
    contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Would you mind sharing your location and contact with me?",
                             reply_markup=reply_markup)


def types_parse_mode(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='<b>It is the bold text</b>\n<i>This is the italic</i>\n<a href="https://python-telegram-bot.readthedocs.io/">This is the link for python-telegram-bot docs page</a>.',
                             parse_mode=ParseMode.HTML)


def keyboard_menus(update, context):
    custom_keyboard = [['top-left', 'top-right'],
                       ['bottom-left', 'bottom-right']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Keyboard for testing",
                             reply_markup=reply_markup)


def main():
    updater = Updater(token=API_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start_command)
    dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    request_l_c = MessageHandler(Filters.regex("data") & (~Filters.command), request_location_contact)
    dispatcher.add_handler(request_l_c)

    testing_parse_mode = MessageHandler(Filters.regex("parse"), types_parse_mode)
    dispatcher.add_handler(testing_parse_mode)

    custom_keyboard = MessageHandler(Filters.regex("custom kb"), keyboard_menus)
    dispatcher.add_handler(custom_keyboard)


    # ...and the error handler
    # dispatcher.add_error_handler(error_handler)

    updater.start_polling()
