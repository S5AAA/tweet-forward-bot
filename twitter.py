#! python
import tweepy
import auth

ID = "1232716565222764544"

class PrintStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

def main():
    api = tweepy.API(auth.twitter)
    sl = PrintStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=sl)

    stream.filter(follow=[ID])

if __name__ == "__main__":
    main()


