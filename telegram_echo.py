#! python3

from auth import Auth
import telegram

class VideoMessage:
    def __init__(self, video, caption, parse_mode="MarkdownV2"):
        self.video = video
        self.caption = caption
        self.parse_mode = parse_mode

    def send(self, bot, channel):
        bot.send_photo(channel, self.video, caption=self.caption, parse_mode=self.parse_mode)


class PhotoMessage:
    def __init__(self, photo, caption, parse_mode="MarkdownV2"):
        self.photo = photo
        self.caption = caption
        self.parse_mode = parse_mode

    def send(self, bot, channel):
        bot.send_photo(channel, self.photo, caption=self.caption, parse_mode=self.parse_mode)

    def __repr__(self):
        return f"{self.photo}\n{self.caption}"

class TextMessage:
    def __init__(self, text, parse_mode="MarkdownV2"):
        self.text = text
        self.parse_mode = parse_mode

    def send(self, bot, channel):
        bot.send_message(channel, self.text, parse_mode=self.parse_mode)

    def __repr__(self):
        return f"{self.text}"


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
        
        self.bot = telegram.Bot(token=Auth.telegram)

    def echo_message(self, message, parse_mode=''):
        """
        Echo a message to all channels

        Parameters:
            message:    A message to echo
            parse_mode: Parsing mode for the message (HTML/Markdown)
        """
        for channel in self.echo_channels:
            message.send(self.bot, channel)
            #self.bot.send_message(channel, message, parse_mode=parse_mode, disable_web_page_preview=False)

