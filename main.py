#! python3

import twitter
import converter
import functools
import telegram_echo
import time

CHANNEL = "-1001300279546"

#ID = "250178637"   #MANNIE
ID = "33473850"     #YNET

RESTART_TIME = 30

def get_bot_echo(bot, convert_func):
    def bot_echo(tweet):
        bot.echo_message(convert_func(tweet), "Markdown")

    return bot_echo

def main():
    telegram_bot = telegram_echo.TelegramEchoBot([CHANNEL])
    
    twitter_bot = twitter.CustomStreamListener([ID], [get_bot_echo(telegram_bot, converter.twitter_to_telegram)])

    while True:
        try:
            twitter_bot.run()
            
        except Exception as e:
            print("Unkown exception!")
            print(e)

        try:
            print(f"Restarting bot in {RESTART_TIME}s... (Ctrl+C to exit)")
            time.sleep(RESTART_TIME)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt while waiting for restart. Exiting bot.")
            exit()

if __name__ == "__main__":
    main()
