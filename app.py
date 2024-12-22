from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import re
import time

# Global storage for previously seen listings
seen_listings = set()

# Load environment variables from the .env file
load_dotenv()

# Telegram Config
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = 'your-chat-id'
URL = 'https://www.otomoto.pl/osobowe/mazda/rx-8'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Initialize bot
bot = Bot(token=BOT_TOKEN)

carList = ["Mazda", "Honda"]
modelList = ["RX8"]

# Define the /start command handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I see you want to buy nice gruzik! type /help to see all the options")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "All the available options:\n"
        "/fetch - Check all the listings for Mazda RX8 and check every 60min\n"
        "/all - Get a list of all the available cars with prices"
    )


async def car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Format the list into a string with each item on a new line
    car_list_formatted = "\n".join(f"- {car}" for car in carList)
    await update.message.reply_text(f"Choose a car from the list:\n{car_list_formatted}")


async def mazda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    checkListing()
    await update.message.reply_text("Mazda")


async def fetch_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Fetch data from the webpage
        data = fetch_data()
        print(data)

        # Format the data into clickable links
        if not data:
            await update.message.reply_text("No listings found.")
            return

        # Calculate the average
        prices = []
        for _, _, price in data:
            # Remove spaces and extract numeric value
            cleaned_price = price.replace(" ", "")
            # Extract numeric value (integer or float)
            match = re.search(r'\d+(?:\.\d+)?', cleaned_price)
            if match:
                prices.append(float(match.group()))  # Convert to float

        if prices:
            average_price = sum(prices) / len(prices)
        else:
            average_price = 0

        # Make clickable links
        response = "\n".join(
            [f"[{title}]({url}) " + price for title, url, price in data[:10]])
        await update.message.reply_text(
            f"Here are the latest listings:\n{response}\n"
            f"Average price: {average_price:.2f}",
            parse_mode=ParseMode.MARKDOWN,  # Enables clickable links
        )
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

    # Main function to run the bot


def checkListing():
    return print('Whoop')

# Function to fetch data with BeautifulSoup


def fetch_data():
    url = URL  # Replace with the target URL
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    soup = BeautifulSoup(response.text, 'html.parser')

    listings = []
    for tag in soup.select('article.e15xeixv0'):
        # Get the title
        title = tag.find('h2').text.strip()
        # Get the listing url
        link_tag = tag.select_one('div.ey6oyue6 a')
        link = link_tag['href']
        # Get the lisitng price
        price_tag = tag.select_one('h3')
        price = price_tag.text.strip()
        print(title + ' ' + link + ' ' + price)
        # Ensure absolute URLs if the href is relative
        full_url = link if link.startswith(
            "http") else requests.compat.urljoin(url, link)
        listings.append((title, full_url, price))

    return listings

    # Example: Extract headlines (replace with your specific logic)
    # headlines = [h.text.strip() for h in soup.select('h2')]  # Adjust selector
    # return headlines or ["No data found"]

# /fetch command handler

# Function to check for new listings and send notifications


async def check_new_listings(context: ContextTypes.DEFAULT_TYPE) -> None:
    global seen_listings
    try:
        # Fetch data from the webpage
        data = fetch_data()
        new_listings = []

        # Compare current listings with the stored ones
        for title, url in data:
            if url not in seen_listings:
                new_listings.append((title, url))
                seen_listings.add(url)  # Add new URL to seen_listings

        # Notify the user about new listings
        if new_listings:
            for title, url in new_listings:
                await context.bot.send_message(
                    chat_id=context.job.chat_id,
                    text=f"New listing found:\n[{title}]({url})",
                    parse_mode=ParseMode.MARKDOWN,
                )
    except Exception as e:
        print(f"Error checking listings: {e}")

# Command handler to start notifications


async def start_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(
        check_new_listings, 60, first=0, chat_id=chat_id
    )  # Check every 60 seconds
    await update.message.reply_text("Started checking for new listings!")


def main():

    # Create the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add a handler for the /start command
    app.add_handler(CommandHandler("start", start))

    # Add a handler for the /help command
    app.add_handler(CommandHandler('help', help))

    # Handler for choosing a car
    app.add_handler(CommandHandler('car', car))

    # Handler for Mazda
    app.add_handler(CommandHandler('mazda', mazda))

    # Add the /fetch command handler
    app.add_handler(CommandHandler("all", fetch_command))

    # Add handlers
    app.add_handler(CommandHandler("fetch", start_notifications))

    # Start the bot
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
