#! python3

import OpenSSL
import tweepy
import auth
import time

api = tweepy.API(auth.twitter)

MIN_DELAY = 0

def ids_from_names(*names):
    ids = []
    for name in names:
        ids.append(api.get_user(name))

    return ids


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
        self.delay_min = MIN_DELAY
        self.delay = MIN_DELAY
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
        
        #print(f"Sleeping for {self.delay}s...")
        #time.sleep(self.delay)
        self.delay *= 2

        start = time.time()

        try:
            print("Connecting...")
            self.stream.filter(follow=self.follow_ids, is_async=run_async)
            print("Connected!")
        except KeyboardInterrupt:
            self.stream.disconnect()
            print("\nKeyboard interrupt, stopping stream")
        except OpenSSL.SSL.WantReadError:
            self.stream.disconnect()
            print("SSL WantReadError, restarting stream")

            lower_delay = time.time() - start
            self.delay = max(MIN_DELAY, self.delay - lower_delay)

            self.run(run_async)
        except Exception as e:
            self.stream.disconnect()
            print("Unknown error")
            print(e)

            lower_delay = time.time() - start
            self.delay = max(MIN_DELAY, self.delay - lower_delay)

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
        
