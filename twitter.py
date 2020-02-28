#! python3

import OpenSSL
import tweepy
import auth

api = tweepy.API(auth.twitter)

class CustomStreamListener(tweepy.StreamListener):
    """
    A class for abstract handling of a Twitter API stream, filtering by account ID.

    Attributes:
        stream:             The stream.
        follow_ids:         A list of IDS to filter by.
        status_functions:   A list of functions to run on every tweet received.
    """
    stream = None
    follow_ids = []
    status_functions = []

    def __init__(self, follow_ids, funcs):
        """
        Create a new CustomStreamListener

        Parameters:
            follow_ids: A list of IDS to filter by.
            funcs:      A list of functions to run on every tweet received.
        """
        self.stream = tweepy.Stream(auth=api.auth, listener=self, tweet_mode='extended')
        self.follow_ids = follow_ids
        self.status_functions = funcs
        super().__init__()


    def add_status_function(self, func):
        """
        Add an additional function to run on every tweet
        """
        self.status_functions.append(self, func)


    def add_follow_id(self, follow_id):
        """
        Add an additional twitter ID to follow
        """
        self.follow_ids.append(follow_id)


    def run(self, run_async=False):
        """
        Start listening using the stream listener

        Parameters:
            run_async: Run asynchronously (default: False)
        """
        try:
            self.stream.filter(follow=self.follow_ids, is_async=run_async)
        except KeyboardInterrupt:
            self.stream.disconnect()
            print("Keyboard interrupt, stopping stream")
        except OpenSSL.SSL.WantReadError:
            self.stream.disconnect()
            print("SSL WantReadError, restarting stream")
            self.run(run_async)
        except Exception:
            self.stream.disconnect()
            print("Unknown error")
            self.run(run_async)


    def on_status(self, status):
        """
        Called every time a tweet is received from the stream
        """
        print(f"new tweet from {status.user.id_str}")

        if status.user.id_str in self.follow_ids:
            if status.in_reply_to_user_id_str is None or status.in_reply_to_user_id_str in self.follow_ids:
                for func in self.status_functions:
                    func(status)

    def on_error(self, status_code):
        if status_code == 420:
            # Disconnect stream
            print("Rate limit exceeded, stopping stream")
            return False
        
