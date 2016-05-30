#!/usr/bin/env python

""" lemmatizer.py : Lemmatization helper functions."""

__author__ = "Pierre Le Bras, Heriot Watt University"
__license__ = "Creative Commons Attribution 4.0 International License"
__version__ = "1.0"

import nltk
import time
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import re


# takes text
# returns [words]
def tokenize_single_text(text):
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(text)


# takes {id -> text}
# returns {id -> [words]}
def tokenize(texts):
    print('tokenizing')
    tokenizer = RegexpTokenizer(r'\w+')
    return {i: tokenizer.tokenize(text) for (i, text) in texts.items()}


# takes {id -> [words]}
# returns same without stop words
def remove_stopwords(tokenized_texts, stopwords_array):
    print('removing stopwords and numbers')
    number_pattern = re.compile('-?\d+(\.\d+)?')
    res = {}
    for (i, words) in tokenized_texts.items():
        _words = []
        for w in words:
            if w.lower() not in stopwords.words('english') \
                    and w.lower() not in stopwords_array \
                    and not number_pattern.match(w.lower()) \
                    and len(w) > 1:
                _words.append(w.lower())
        res[i] = _words
    return res


# takes {id -> [words]}
# returns {id -> [(words, tags)]}
def tag(texts):
    print('tagging words')
    return {i: nltk.pos_tag(words) for (i, words) in texts.items()}


# takes {id -> [(words, tags)]}
# returns same with correct tags for lemmatising
# removes non noun words (verb, adjectives, adverbs)
def switch_tags_for_lemmatizer_and_clean(texts):
    print('cleaning')
    res = {}
    for (i, words) in texts.items():
        _words = []
        for w in words:
            if w[1].startswith('N'):
                _words.append([w[0], wordnet.NOUN])
                # uncomment to add verbs, adjectives or adverbs
                # elif w[1].startswith('J'):
                #     _words.append([w[0], wordnet.ADJ])
                # elif w[1].startswith('V'):
                #     _words.append([w[0], wordnet.VERB])
                # elif w[1].startswith('R'):
                #     _words.append([w[0], wordnet.ADV])
        res[i] = _words
    return res


# takes {id -> [(words, tags)]}
# returns {id -> [lemmas]}
def lemmatize(texts):
    print('lemmatizing')
    lemmatizer = WordNetLemmatizer()
    return {i: [lemmatizer.lemmatize(w[0], w[1]) for w in words] for (i, words) in texts.items()}


# lemmatization function
# takes text dictionary and custom stopwords array (default is [])
# return lemmas dictionary
def do_lemmatization(texts, stopwords_array=None):
    if stopwords_array is None:
        stopwords_array = []
    start = time.time()
    print('starting lemmatization')
    lemmas = lemmatize(switch_tags_for_lemmatizer_and_clean(tag(remove_stopwords(tokenize(texts), stopwords_array))))
    end = time.time()
    elapsed = end - start
    print('lemmatization done, time elapsed : %s m %s s' % (str(int(elapsed) / 60), str(int(elapsed) % 60)))
    return lemmas
