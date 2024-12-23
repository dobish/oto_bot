# Telegram Bot README

## Overview

This Telegram bot is designed to fetch and display listings from otomoto - Polish car marketplace, calculate averages, and provide users with clickable links to relevant content. It is built using Python and the Telegram Bot API.

It was created in order to practice Python and find a good offer on Mazda RX8

## Features

- Fetch data dynamically from a webpage.
- Display listings with titles, prices, and clickable URLs.
- Calculate and display the average price of items.

## Prerequisites

To run this bot, you need:

- Python 3.8 or higher
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dobish/oto_bot.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:

   - Create a `.env` file in the root directory.
   - Add your bot token:
     ```env
     BOT_TOKEN=your-telegram-bot-token
     ```

4. Run the bot:
   ```bash
   python app.py
   ```

## Usage

Once the bot is running:

1. Start a conversation with your bot on Telegram.
2. Use the `/fetch` command to retrieve the latest listings.
3. The bot will reply with formatted results including titles, clickable links, and prices.
4. Bot will check every hour if new listing appeared

### Example Commands

- `/help` - Get all the available commands.
- `/fetch` - Fetch and display the latest listings.

## Example Output
