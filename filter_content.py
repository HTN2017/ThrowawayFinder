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

MINUMIM_COMMENTS = 10


class FilterContent():

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            password=PASSWORD,
            user_agent=USER_AGENT,
            username=USERNAME)

    def get_data(self):
        with open(SUBREDDIT + '_data.txt') as data_file:
            data = json.load(data_file)
        self.raw_data = data
        self.set_author_list(data)
        self.store_author_list(self.format_author_list())

    def format_author_list(self):
        normal_comments = []
        for author in self.authors:
            for comment in self.authors[author]:
                normal_comments.append({
                    'data': comment,
                    'author': author,
                })
        throw_comments = []
        for author in self.throwaway_authors:
            for comment in self.throwaway_authors[author]:
                throw_comments.append({
                    'data': comment,
                    'author': author,
                })
        return {
            'normal': normal_comments,
            'throw': throw_comments
        }

    def set_author_list(self, data):
        self.authors = {}
        self.throwaway_authors = {}
        for comment in data:
            if comment['author'] in self.authors:
                self.authors[comment['author']].append(comment['body'])
            elif comment['author'] in self.throwaway_authors:
                self.throwaway_authors[comment['author']].append(comment['body'])
            else:
                if self.is_throw_away(comment['author']):
                    logger.warning(comment['author'])
                    self.throwaway_authors[comment['author']] = []
                    self.throwaway_authors[comment['author']].append(comment['body'])
                else:
                    self.authors[comment['author']] = []
                    self.authors[comment['author']].append(comment['body'])

    def store_author_list(self, comments):
        with open(SUBREDDIT + '_filter.txt', 'w') as outfile:
            json.dump(comments, outfile)

    def is_throw_away(self, author):
        if "throwaway" in author.lower():
            return True
        data = self.reddit.get('/user/' + author)
        trophies = self.reddit.get("/user/" + author + "/trophies")['data']['trophies']
        for trophy in trophies:
            if trophy['data']['name'] == 'Verified Email':
                return False
        comment_count = 0
        for comment in self.reddit.redditor(author).comments.new(limit=None):
            comment_count += 1
            if comment_count == MINUMIM_COMMENTS:
                return False
        return True

logger.warning(FilterContent().get_data())
