# Tweet Forward Bot
A simple generic tweet-forwarding bot

---
# twitter.py
Used by the bot to interact with the Twitter API and get tweets
## CustomStreamListener
A StreamListener that filters by a list of IDs.
*   ### follow_ids
    A list of IDs to follow
*   ### status_functions
    A list of functions to run on every status received from the stream
 ---   
# converter.py
Used by the bot to convert tweepy status objects into other formats to be sent to other APIs
*   ### twitter_to_telegram
    Converts a tweepy status into a markdown Telegram message with Twitter link embeds
 ---
# telegram_echo.py
Used by the bot to send messages to Telegram
## TelegramEchoBot
A simple Telegram bot that echoes messages into a list of channels
*   ### echo_channels
    A list of channels to send every message into
 ---
