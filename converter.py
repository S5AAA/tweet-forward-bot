#! python3

import re
import tweepy

HTTP_PATTERN = r"(https?://[^ ]*)"

EMPTY_EMBED = r"[​](\1)"
LINK_EMBED = r"[\1](\1)"


def twitter_to_telegram(status):
    """
    Convert a twitter status to a telegram message
    
    Parameters:
        status: The twitter status
    """
    text = status.text

    print(f"TWITTER: {text} -> ", end="")
    
    if re.sub(HTTP_PATTERN, "", text, re.IGNORECASE):
        text = re.sub(HTTP_PATTERN, EMPTY_EMBED, text, re.IGNORECASE)
    else:
        text = re.sub(HTTP_PATTERN, LINK_EMBED, text, re.IGNORECASE)

    print(f"TELEGRAM: {text}")

    return text
