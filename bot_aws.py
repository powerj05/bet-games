import json
import asyncio
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Bot
from telegram.ext import ContextTypes

TOKEN: Final = '7137871448:AAGF5aNYGX6ghxTSHEHDLruGKiEsKPDMMlw'
BOT_USERNAME: Final = '@jpaddy_bot'

# Initialize bot instance
bot = Bot(token=TOKEN)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am a bot. Send me a message to test responses. ")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a simple bot written in Python; I don't do much. Send me any message. ")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This custom command does nothing. ")

# Responses
def handle_response(text: str) -> str:
    return f'Thanks. We received "{text}"'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User {update.message.chat.id} in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
   
    # Generate keyboard markup for webapp
    webapp = WebAppInfo(url="https://powerj05.github.io/bet-games/")
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Check out my webapp!", web_app=webapp)]])
    
    print(f'Bot: "{response}"')
    await update.message.reply_text(response, reply_markup=keyboard)

async def process_update(update_data: dict):
    """Process a single update from webhook"""
    try:
        # Create Update object from webhook data
        update = Update.de_json(update_data, bot)
        
        if update.message:
            if update.message.text:
                # Check if it's a command
                if update.message.text.startswith('/start'):
                    await start_command(update, None)
                elif update.message.text.startswith('/help'):
                    await help_command(update, None)
                elif update.message.text.startswith('/custom'):
                    await custom_command(update, None)
                else:
                    # Handle regular message
                    await handle_message(update, None)
        
    except Exception as e:
        print(f'Error processing update: {e}')
        raise e

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    try:
        # Parse the webhook payload
        if 'body' in event:
            # API Gateway sends body as string
            body = event['body']
            if isinstance(body, str):
                update_data = json.loads(body)
            else:
                update_data = body
        else:
            # Direct invocation
            update_data = event
        
        # Process the update asynchronously
        asyncio.run(process_update(update_data))
        
        # Return success response for API Gateway
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ok'})
        }
        
    except Exception as e:
        print(f'Lambda handler error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# For local testing (optional)
if __name__ == '__main__':
    # Test with sample update
    sample_update = {
        "update_id": 123,
        "message": {
            "message_id": 456,
            "from": {"id": 789, "first_name": "Test"},
            "chat": {"id": 789, "type": "private"},
            "date": 1234567890,
            "text": "/start"
        }
    }
    
    result = lambda_handler(sample_update, None)
    print(result)