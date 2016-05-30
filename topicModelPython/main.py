#!/usr/bin/env python

""" main.py : main script to execute topic modeling."""

__author__ = "Pierre Le Bras, Heriot Watt University"
__license__ = "Creative Commons Attribution 4.0 International License"
__version__ = "1.0"

from topicModel.TopicModel import TopicModel

tm = TopicModel(n_topics=30, n_words_per_topic=20, n_iter=2000)
tm.read_data(data_file_name='data/textsData/rp_stefano_data.json',
             path=["grants"],
             id_accessor="grant",
             text_accessors=["Title", "Summary"])
tm.model()
tm.save_data(file_name='data/topicModels/rp_stefano_topic_model.json')
