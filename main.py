#! python3

from logger import Logger
from auth import Auth
import telegram_echo
import converter
import functools
import argparse
import twitter
import tweepy

RESTART_TIME = 30

def get_bot_echo(bot, convert_func):
    def bot_echo(tweet):
        bot.echo_message(convert_func(tweet), "Markdown")

    return bot_echo


def parse_args():
    parser = argparse.ArgumentParser()

    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')

    required.add_argument('-i', metavar='twitter_name', help='Name of Twitter accounts to echo', nargs='+', required=True)
    required.add_argument('-o', metavar='telegram_channel', help='Telegram channel IDs to echo into', nargs='+', required=True)

    required.add_argument('--telegram-token', metavar='telegram_token', help='Telegram API token in the form of XXXXXXX:YYYYYYYYYYYY', required=True)

    required.add_argument('--twitter-consumer', metavar=('consumer_key', 'consumer_secret'), help='Twitter consumer key and secret', nargs=2, required=True)

    required.add_argument('--twitter-token', metavar=('access_token', 'token_secret'), help='Twitter access token and access token secret', nargs=2, required=True)

    optional.add_argument('-r', metavar='reset_time', help='Time the bot sleeps between rate limit errors or manual restarts', default=30, type=int)


    parser._action_groups.append(optional)

    return parser.parse_args()

def main():
    args = parse_args()
    
    twitter_names = args.i
    telegram_channels = args.o
    reset_time = args.r

    twitter_consumer = args.twitter_consumer
    twitter_access = args.twitter_token
    telegram_token = args.telegram_token

    print(f"""Initializing twitter API with credentials:
{twitter_consumer}
{twitter_access}""")

    Auth.twitter = tweepy.OAuthHandler(*twitter_consumer)
    Auth.twitter.set_access_token(*twitter_access)

    Auth.twitter_api = tweepy.API(Auth.twitter)

    print(f"""Initializing telegram API with credentials:
{telegram_token}""")

    Auth.telegram = telegram_token

    print(f"""Starting with:
twitter_names = {twitter_names},
telegram_channels = {telegram_channels},
reset_time = {reset_time}""")

    print(f"Getting ids for {twitter_names}")
    twitter_ids = twitter.ids_from_names(*twitter_names)
    print(f"Got {twitter_ids}")

    telegram_bot = telegram_echo.TelegramEchoBot(telegram_channels)
    
    twitter_bot = twitter.CustomStreamListener(twitter_ids, [get_bot_echo(telegram_bot, converter.twitter_to_telegram)])
    
    print(f"Initializing logger...")
    logger = Logger()
    logger.init()

    while True:
        try:
            twitter_bot.run()
            
        except Exception as e:
            print("Unkown exception!")
            print(e)

        try:
            print(f"Restarting bot in {reset_time}s... (Ctrl+C to exit)")
            time.sleep(reset_time)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt while waiting for restart. Shutting down.")
            break

    print("Shutting down logger...")
    logger.finit()

    print("Exiting")

if __name__ == "__main__":
    main()
