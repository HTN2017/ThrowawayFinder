import praw
import logging
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
import numpy as np
from constants import *


class MatchUsers(object):

    def __init__(self, SUBREDDIT):
        self.SUBREDDIT = SUBREDDIT
        self.get_data()

    def get_data(self):
        with open(self.SUBREDDIT + '_filter.txt') as data_file:
            data = json.load(data_file)
        self.raw_data = data

    def match_results(self):
        normal_comments = [comment['data'] for comment in self.raw_data['normal']]
        normal_authors = [comment['author'] for comment in self.raw_data['normal']]

        throw_comments = [self.raw_data['throw'][author] for author in self.raw_data['throw']]
        throw_authors = [author for author in self.raw_data['throw']]

        vectorizer = TfidfVectorizer()
        normal_vectors = vectorizer.fit_transform(normal_comments)
        throw_vectors = vectorizer.transform(throw_comments)

        X_train, X_test, y_train, y_test = train_test_split(normal_vectors, normal_authors, test_size=0, random_state=1337)

        svm = LinearSVC()
        svm.fit(X_train, y_train)
        predictions = svm.predict(throw_vectors)
        decision = svm.decision_function(throw_vectors)
        display_dict = []
        i = 0
        while(i < len(predictions)):
            display_dict.append({
                'throw': throw_authors[i],
                'match': predictions[i],
                'comment': self.raw_data['throw'][throw_authors[i]]
            })
            logging.warning(throw_authors[i] + ": " + predictions[i])
            closeness = [abs(value) for value in decision[i]]
            min_index = closeness.index(min(closeness))
            logging.warning(normal_authors[min_index] + ": " + str(closeness[min_index]))
            i += 1
        logging.warning(display_dict)
        return display_dict


#MatchUsers('uwaterloo').match_results()
