import praw
import logging
import json
logger = logging.getLogger()
CLIENT_ID = ''
CLIENT_SECRET = ''
PASSWORD = ''
USERNAME = ''
USER_AGENT = ''
SUBREDDIT = ''


class FilterContent():

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            password=PASSWORD,
            user_agent=USER_AGENT,
            username=USERNAME)
        self.get_data()

    def get_data(self):
        with open('data.txt') as data_file:
            data = json.load(data_file)
        self.raw_data = data
        self.set_author_list(data)

    def set_author_list(self, data):
        self.authors = {}
        for comment in data:
            logger.warning(comment)
            if comment['author'] in self.authors:
                self.authors[comment['author']].append(comment['body'])
            else:
                self.authors[comment['author']] = []
                self.authors[comment['author']].append(comment['body'])


FilterContent()