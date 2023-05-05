import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler, CallbackQueryHandler, MessageHandler, Application, filters
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardButton, InlineKeyboardMarkup
from scrapper import Scrapper
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

MENU = 'Comandos:\n'\
       '/start - Muestra los Comandos del BOT\n'\
       '/bcv - Tasa $ con respecto al Banco Central De Venezuela\n'\
       '/parall - Tasa $ con respecto a la cuenta enParalelo\n\n'\
       'Nota: Puede enviar un mensaje con los simbolos "$" o "Bs"\n'\
       'al final de cada cantidad para convertir de $ a Bs y Viceversa\n\n'\
       'Ej: 100$ o 100Bs'

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   await context.bot.send_message(chat_id=update.effective_chat.id, text=MENU)
#
#
# async def bcv(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   dollar = Scrapper().get_dictionary()
#
#   BVC = dollar['BVC']
#   BVC_TIMER = dollar['BVC_TIMER']
#   await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{BVC} Bs\n{BVC_TIMER}')
#
#
# async def parall(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   dollar = Scrapper().get_dictionary()
#
#   PARALELO = dollar['PARALELO']
#   PARALELO_TIMER = dollar['PARALL_TIMER']
#   await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{PARALELO} Bs\n{PARALELO_TIMER}')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  MESSAGE_BOT = update.message.text
  Dollar = Scrapper()

  if Dollar.is_Dollar(MESSAGE_BOT):
    MESSAGE_BVC = Scrapper().get_dollar_bs_BVC(MESSAGE_BOT[:-1])
    MESSAGE_PARALELO = Scrapper().get_dollar_bs_PARALELO(MESSAGE_BOT[:-1])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{MESSAGE_BOT} = {MESSAGE_BVC} Bs  <- Tasa BVC ->\n{MESSAGE_BOT} = {MESSAGE_PARALELO} Bs  <- Tasa Paralelo ->')

  elif Dollar.is_Bs(MESSAGE_BOT):
    MESSAGE_BVC = Scrapper().get_bs_dollar_BVC(MESSAGE_BOT[:-2])
    MESSAGE_PARALELO = Scrapper().get_bs_dollar_PARALELO(MESSAGE_BOT[:-2])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{MESSAGE_BOT} = {MESSAGE_BVC} $  <- Tasa BVC ->\n{MESSAGE_BOT} = {MESSAGE_PARALELO} $  <- Tasa Paralelo ->')

  else:
    MESSAGE_BVC = Scrapper().get_dollar_bs_BVC(MESSAGE_BOT)
    MESSAGE_PARALELO = Scrapper().get_dollar_bs_PARALELO(MESSAGE_BOT)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{MESSAGE_BOT} $ = {MESSAGE_BVC} Bs  <- Tasa BVC ->\n{MESSAGE_BOT} $ = {MESSAGE_PARALELO} Bs  <- Tasa Paralelo ->')


async def inline_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    Dollar = Scrapper()

    if Dollar.is_Dollar(query):
      MESSAGE_BVC = Dollar.get_dollar_bs_BVC(query[:-1])
      MESSAGE_PARALELO = Dollar.get_dollar_bs_PARALELO(query[:-1])
          
      results = []
      results.append(
          InlineQueryResultArticle(
              id=query,
              title='Calcular',
              input_message_content=InputTextMessageContent(f'{query} = {MESSAGE_BVC} Bs  <- Tasa BVC ->\n{query} = {MESSAGE_PARALELO} Bs  <- Tasa Paralelo ->')
          )
      )
      await context.bot.answer_inline_query(update.inline_query.id, results)

    elif Dollar.is_Bs(query):
      MESSAGE_BVC = Dollar.get_bs_dollar_BVC(query[:-2])
      MESSAGE_PARALELO = Dollar.get_bs_dollar_PARALELO(query[:-2])

      results = []
      results.append(
          InlineQueryResultArticle(
              id=query,
              title='Calcular',
              input_message_content=InputTextMessageContent(f'{query} = {MESSAGE_BVC} $  <- Tasa BVC ->\n{query} = {MESSAGE_PARALELO} $  <- Tasa Paralelo ->')
          )
      )
      await context.bot.answer_inline_query(update.inline_query.id, results)

    else:
      MESSAGE_BVC = Dollar.get_dollar_bs_BVC(query)
      MESSAGE_PARALELO = Dollar.get_dollar_bs_PARALELO(query)

      results = []
      results.append(
          InlineQueryResultArticle(
              id=query,
              title='Calcular',
              input_message_content=InputTextMessageContent(f'{query} = {MESSAGE_BVC} Bs  <- Tasa BVC ->\n{query} = {MESSAGE_PARALELO} Bs  <- Tasa Paralelo ->')
          )
      )
      await context.bot.answer_inline_query(update.inline_query.id, results)

######################################################NEW Funtion################################################

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("💰Tasa BCV", callback_data="1"),
            InlineKeyboardButton("🛍Tasa Paralelo", callback_data="2"),
        ],
        [InlineKeyboardButton("➕MAS", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Presione su opcion:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query


    if '1' in query.data:
        dollar = Scrapper().get_dictionary()
        BVC = dollar['BVC']
        BVC_TIMER = dollar['BVC_TIMER']

        await query.answer()
        await query.edit_message_text(text=f'{BVC} Bs\n{BVC_TIMER}')

    elif '2' in query.data:
        dollar = Scrapper().get_dictionary()
        PARALELO = dollar['PARALELO']
        PARALELO_TIMER = dollar['PARALL_TIMER']

        await query.answer()
        await query.edit_message_text(text=f'{PARALELO} Bs\n{PARALELO_TIMER}')
    else:
        await query.answer()
        await query.edit_message_text(text='Nota: Puede enviar un mensaje con los simbolos "$" o "Bs"\n' \
                                           'al final de cada cantidad para convertir de $ a Bs y Viceversa\n\n' \
                                           'Ej: 100$ o 100Bs')


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text("Use /start para iniciar al bot.")


if __name__ == '__main__':
  keep_alive()
  application = ApplicationBuilder().token(TOKEN).build()

  # start_handler = CommandHandler('start', start)
  # application.add_handler(start_handler)
  #
  # bvc_handler = CommandHandler('bcv', bcv)
  # application.add_handler(bvc_handler)
  #
  # parall_handler = CommandHandler('parall', parall)
  # application.add_handler(parall_handler)

  inline_calculator_handler = InlineQueryHandler(inline_calculator)
  application.add_handler(inline_calculator_handler)

  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
  application.add_handler(echo_handler)

  ########################################New Funtion#################################################3

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button))
  # application.add_handler(CommandHandler("help", help_command))

  application.run_polling()
