from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

#Bot variables
TOKEN: Final = ""
BOT_USERNAME: Final = ""
#Public variables


#Commands
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the JustETF bot!")

async def help_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Text something!")
    

#Responses
def handle_Response(text: str) -> str:
    response = ""
        
    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #group chat or single chat
    text: str = update.message.text #input message
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response:str = handle_Response(new_text)

        else: return
    else:
        response:str=handle_Response(text)

    print(response)
    await update.message.reply_text(response)

#Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

#MAIN 
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Error
    app.add_error_handler(error)

    #Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=2)