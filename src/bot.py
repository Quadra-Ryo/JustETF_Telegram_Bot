from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from JustETFScraper import *
from dotenv import load_dotenv
import os
import asyncio

load_dotenv("sensibleData.env")
# Bot variables
TOKEN: Final = os.getenv("TELEGRAM_BOT_KEY")
BOT_USERNAME: Final = os.getenv("BOT_USER_NAME")
request= {}

# Check if environment variables are loaded
if TOKEN is None or BOT_USERNAME is None:
    raise ValueError("Error: BOT_TOKEN or BOT_USER_NAME cannot be read in the environment.")

###############################################################################################

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the JustETF bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use the following commands as you need!\n"
                                    "scrape - Returns all tha usefull data "
                                    "getName - Returns the Name of the ETF given an ISIN\n"
                                    "getTicker - Returns the Ticker of the ETF given the ISIN and the prefered language\n"
                                    "getPercTenHoldings - Returns the holdings number and the percentage of the top 10 holdings of the ETF given the ISIN and the prefered language\n"
                                    "getHoldingsData - Returns the data of the top 10 holdings in the ETF given the ISIN and the prefered language\n"
                                    "getCountriesData - Returns the data of the 5 states with the more partecipation in the ETF given the ISIN and the prefered language\n"
                                    "getSectorsData - Returns the data of the 5 sectors with the more partecipation in the ETF given the ISIN and the prefered language\n"
                                    "getGeneralInformations - Returns all the general informations of the ETF given the ISIN and the prefered language\n")

async def functionScrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "scrape"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")
    
async def functionGetName(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getName"
    await update.message.reply_text(f"Insert the ISIN of the ETF (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")
    
async def functionGetTicker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getTicker"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")

async def functionGetPercTenHoldings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getPercTenHoldings"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")

async def functionGetHoldingsData(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getHoldingsData"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")

async def functionGetCountriesData(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getCountriesData"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")
    
async def functionGetSectorsData(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getSectorsData"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")
    
async def functionGetGeneralInformations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    request[userID] = "getGeneralInformations"
    await update.message.reply_text(f"Insert the ISIN of the ETF and your preferred language (\"ISIN, language\", Example: \"IE00B4L5Y983, EN\")")

###############################################################################################

# Responses
def handle_Response(text: str, update: Update) -> str:
    
    # Variables used in the function
    userID = update.message.chat.id
    response = "General error, make sure to have used a command before sending this message!" # Default response
    name = ""
    ticker = ""
    percTenHoldings = ""
    holdingsData = ""
    sectorsData = ""
    countriesData = ""
    generalInfo = ""
    outputHashMap = getOutputStringHashMap()
    if request[userID] == "getName":
        name = getName()
        
    return response

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type  # Group chat or single chat
    text: str = update.message.text  # Input message
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    userID = update.message.chat.id
    if userID not in request:
        request[userID] = ""
        
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            if new_text:  # Only process if there's text left after removing the bot mention
                response: str = handle_Response(new_text)
            else:
                response = "You mentioned me, but didn't say anything!"
        else:
            return
    else:
        response: str = handle_Response(text, update)

    print(response)
    if response:  # Only send a response if it’s not empty
        await update.message.reply_text(response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

###############################################################################################

# MAIN
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("getName", getName))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=2)
