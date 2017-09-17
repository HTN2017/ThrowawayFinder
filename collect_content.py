import praw
import logging
import json
import os
logger = logging.getLogger()
from constants import *


class ContentCollector(object):

    def __init__(self, SUBREDDIT):
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            password=PASSWORD,
            user_agent=USER_AGENT,
            username=USERNAME)
        self.SUBREDDIT = SUBREDDIT
        if self.check_for_file(): # if data file exists dont collect again
            return
        self.get_comments(self.get_sub_reddit())

    def get_sub_reddit(self):
        subreddit = self.reddit.subreddit(self.SUBREDDIT)
        return subreddit

    def check_for_file(self):
        if os.path.exists(self.SUBREDDIT + '_data.txt'):
            logger.warning("Opened")
            return True
        return False

    def get_comments(self, subreddit):
        submissions = subreddit.new(limit=100)
        comments_content = []
        appeared_authors = {}
        for submission in submissions:
            submission.comments.replace_more(limit=32)
            try:
                comments_content.append({
                    'body': submission.selftext,
                    'author': submission.author.name,
                })
            except AttributeError:
                logger.warn("AUthor not found")
            all_comments = submission.comments.list()
            for comment in all_comments:
                try:
                    content = {
                        'body': comment.body,
                        'author': comment.author.name,
                    }
                    if comment.author.name not in appeared_authors:
                        appeared_authors[comment.author.name] = True
                        comments_content = comments_content + self.get_recent_general_comments_by_author(comment.author.name)
                except AttributeError:
                    continue
                comments_content.append(content)
        self.store_comments(comments_content)
        return comments_content

    def store_comments(self, comments):
        with open(self.SUBREDDIT + '_data.txt', 'w') as outfile:
            json.dump(comments, outfile)

    def get_recent_general_comments_by_author(self, author):
        # gets users comments from out of subreddit
        comments = []
        for comment in self.reddit.redditor(author).comments.new(limit=10):
            content = {
                'body': comment.body,
                'author': comment.author.name,
            }
            if comment.subreddit == self.SUBREDDIT:
                continue
            comments.append(content)
        return comments



#ContentCollector('uwaterloo')
