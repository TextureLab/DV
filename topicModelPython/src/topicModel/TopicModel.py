#!/usr/bin/env python

""" TopicModel.py : Topic model class."""

__author__ = "Pierre Le Bras, Heriot Watt University"
__license__ = "Creative Commons Attribution 4.0 International License"
__version__ = "1.0"

import time
from copy import deepcopy

import lda
import numpy as np

from . import lemmatizer
from .TopicsSimilarities import TopicsSimilarities
from .dataIO import DataReader, DataWriter


class TopicModel:

    def __init__(self, n_topics=20, n_words_per_topic=10, n_iter=1500, alpha=0.1, eta=0.01, stopwords_array=None):
        if stopwords_array is None:
            self.stopwords_array = []
        else:
            self.stopwords_array = stopwords_array
        self.n_topics = n_topics
        self.n_words_per_topic = n_words_per_topic
        self.n_iter = n_iter
        self.alpha = alpha
        self.eta = eta
        self.topics = {}
        self.docs_topics_distrib = {}
        self.topics_docs_distrib = {}
        self.topics_similarities = {}
        self.n_docs = 0
        self.texts = {}

    def model(self):

        if not self.texts:
            raise Exception('No texts to make topic modeling, check if data was correctly uploaded')

        lemmatized_docs = lemmatizer.do_lemmatization(self.texts, self.stopwords_array)

        print('making doc word matrix')
        words = []
        docs = []
        for (d, _words) in lemmatized_docs.items():
            docs.append(d)
            for w in _words:
                if w not in words:
                    words.append(w)
        docs_words_matrix = np.zeros(shape=(len(docs), len(words)), dtype=np.int)
        for i, d in enumerate(docs):
            for j, w in enumerate(words):
                docs_words_matrix[i][j] += lemmatized_docs[d].count(w)

        self.n_docs = len(docs)

        print('INFO : %s documents, %s words' % (str(len(docs)), str(len(words))))

        start = time.time()
        print('Modeling topics')
        topic_model = lda.LDA(n_topics=self.n_topics,
                              n_iter=self.n_iter,
                              random_state=1,
                              alpha=self.alpha,
                              eta=self.eta)
        topic_model.fit(docs_words_matrix)
        end = time.time()
        elapsed = end - start
        print('topic modeling done, time elapsed : %s m %s s' % (str(int(elapsed / 60)), str(int(elapsed) % 60)))

        print('getting topics')
        for i, topic_dist in enumerate(topic_model.topic_word_):
            top_indices = np.argsort(topic_dist)[:-(self.n_words_per_topic + 1):-1]
            self.topics[str(i)] = [{'label': words[j], 'weight': topic_dist[j]} for j in top_indices]

        print('getting documents distribution per topic')
        sum_topic_distrib = np.zeros(shape=self.n_topics)
        avg_topic_distrib = np.zeros(shape=self.n_topics)
        count_sum = 0
        for i, d in enumerate(docs):
            self.docs_topics_distrib[d] = topic_model.doc_topic_[i]
            count_sum += 1
            for j in range(self.n_topics):
                sum_topic_distrib[j] += topic_model.doc_topic_[i][j]
        for i in range(self.n_topics):
            avg_topic_distrib[i] = sum_topic_distrib[i] / count_sum
        topic_comp_1 = {}
        for i in range(self.n_topics):
            tmp_ids = []
            tmp_weights = []
            mult = 10
            done = False
            while not done:
                for (d, t) in self.docs_topics_distrib.items():
                    text_length = len(lemmatizer.tokenize_single_text(self.texts[d]))
                    if t[i] > avg_topic_distrib[i] * mult and text_length > 10:
                        tmp_ids.append(d)
                        tmp_weights.append(t[i])
                if not tmp_ids:
                    mult -= 1
                else:
                    done = True
            topic_comp_1[str(i)] = tmp_ids
            docs_distrib = []
            for index, doc_id in enumerate(tmp_ids):
                docs_distrib.append({'docID': doc_id, 'weight': tmp_weights[index]})
            self.topics_docs_distrib[str(i)] = docs_distrib

        print('computing topics similarities')
        sim = TopicsSimilarities(topic_comp_1, deepcopy(topic_comp_1))
        sim.compute_similarities(self.docs_topics_distrib)
        self.topics_similarities = sim.similarities

    def read_data(self, data_file_name='', path=None, id_accessor="id", text_accessors=None):
        if text_accessors is None:
            text_accessors = ["text"]
        if path is None:
            path = []
        self.texts = DataReader(data_file_name=data_file_name)\
            .get_texts(path=path, id_accessor=id_accessor, text_accessors=text_accessors)

    def save_data(self, file_name):
        DataWriter(file_name=file_name)\
            .write(data={'topics': self.topics,
                         'topicsSimilarities': self.topics_similarities,
                         'topicsDocsDistrib': self.topics_docs_distrib})
