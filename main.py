#! python3

import twitter
import converter
import functools
import telegram_echo

CHANNEL = "-1001300279546"

ID = "250178637"


def get_bot_echo(bot, convert_func):
    def bot_echo(tweet):
        bot.echo_message(convert_func(tweet), "Markdown")

    return bot_echo

def main():
    telegram_bot = telegram_echo.TelegramEchoBot([CHANNEL])
    
    twitter_bot = twitter.CustomStreamListener([ID], [get_bot_echo(telegram_bot, converter.twitter_to_telegram)])

    twitter_bot.run()

    # [​​​](https://t.co/DCjoquxcUQ)

if __name__ == "__main__":
    main()
