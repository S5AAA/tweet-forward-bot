#! python3

import re
import tweepy
import requests
from telegram_echo import TextMessage, PhotoMessage, VideoMessage#, MediaGroupMessage

HTTP_PATTERN = r"(https?://[^ ]*)"
EMBED_PATTERN = r"\[.*\]\((https?://[^ ]*)\)"

EMPTY_EMBED = r"[​](\1)"
LINK_EMBED = r"[\1](\1)"


def twitter_to_telegram(status):
    """
    Convert a twitter status to a telegram message
    
    Parameters:
        status: The twitter status
    """

    print(status)
    text = ""
    telegram = None

    if 'extended_tweet' in status:
        text = status['extended_tweet']['full_text']
    else:
        text = status['text']

    print(f"TWITTER: {text} -> ", end="")
    
    if 'entities' in status:
        if 'media' in status['entities']:
            text = re.sub(HTTP_PATTERN, "", text, re.IGNORECASE)
            if len(status['entities']['media']) == 1:
                telegram = PhotoMessage(status['entities']['media'][0]['media_url'], caption=text)
        #elif 'urls' in status['entities']:
            #text = re.sub(HTTP_PATTERN, EMPTY_EMBED_FMT.format(url=status['entities']['urls'][0]['expanded_url']), text, re.IGNORECASE)
        else:
            # Replace links with link embeds
            if re.sub(HTTP_PATTERN, "", text, re.IGNORECASE):
                text = re.sub(HTTP_PATTERN, EMPTY_EMBED, text, re.IGNORECASE)
            else:
                text = re.sub(HTTP_PATTERN, LINK_EMBED, text, re.IGNORECASE)
            telegram = TextMessage(text)

    #match = re.search(HTTP_PATTERN, text, re.IGNORECASE)
    #if match is not None:
        #url = requests.get(match[0]).url
        #if re.sub(HTTP_PATTERN, "", text, re.IGNORECASE):
            #text = re.sub(HTTP_PATTERN, EMPTY_EMBED_FMT.format(url=url), text, re.IGNORECASE)
        #else:
            #text = re.sub(HTTP_PATTERN, LINK_EMBED, text, re.IGNORECASE)

    print(f"TELEGRAM: {telegram}")

    return telegram
