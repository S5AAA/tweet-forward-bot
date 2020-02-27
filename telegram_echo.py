#! python3

import telegram
import auth

class TelegramEchoBot:
    """
    A simple telegram bot that echos string messages

    Attributes:
        echo_channels:  A list of channels to echo to.
        bot:            The bot.
    """

    echo_channels = []
    bot = None
    
    def __init__(self, channels):
        """
        Create a new telegram echo bot

        Parameters:
            channels:   A list of channels for the bot to echo into.
        """
        self.echo_channels = channels
        
        self.bot = telegram.Bot(token=auth.telegram)

    def echo_message(self, message, parse_mode=''):
        """
        Echo a message to all channels

        Parameters:
            message:    A message to echo
            parse_mode: Parsing mode for the message (HTML/Markdown)
        """
        for channel in self.echo_channels:
            self.bot.send_message(channel, message, parse_mode=parse_mode)

