#!/usr/bin/env python

""" TopicsSimilarities.py : Topics similarities class."""

__author__ = "Pierre Le Bras, Heriot Watt University"
__license__ = "Creative Commons Attribution 4.0 International License"
__version__ = "1.0"

import numpy as np
from math import sqrt


def __normalize__(comp_vector, distributions):
    return_vector = {}
    for (topic, docs) in comp_vector.items():
        n_vector = np.zeros(shape=len(comp_vector))
        for d in docs:
            for i, dist in enumerate(distributions[d]):
                n_vector[i] += dist
        n_vector = list(map(lambda x: x / len(docs), n_vector))
        return_vector[topic] = n_vector
    return return_vector


class TopicsSimilarities:

    def __init__(self, comp_1, comp_2):
        self.comp_1 = comp_1
        self.comp_2 = comp_2
        self.similarities = {}
        self.weights = []
        self.ids = [i for (i, _) in comp_1.items()]

    def compute_similarities(self, docs_topics_distrib):
        comp1_vector = __normalize__(self.comp_1, docs_topics_distrib)
        comp2_vector = __normalize__(self.comp_2, docs_topics_distrib)
        self.weights = [comp1_vector[i] for i in self.ids]
        for i, id1 in enumerate(self.ids):
            values1 = self.weights[i]
            sim_temp = {}
            for id2, values2 in comp2_vector.items():
                sum_vectors = 0.0
                sqr_sum_vector1 = 0.0
                sqr_sum_vector2 = 0.0
                for j in range(len(values2)):
                    sum_vectors += values1[j] * values2[j]
                    sqr_sum_vector1 += values1[j] * values1[j]
                    sqr_sum_vector2 += values2[j] * values2[j]
                div = max((sqrt(sqr_sum_vector1) * sqrt(sqr_sum_vector2)), 0.00000001)
                relevance = sum_vectors / div
                sim_temp[id2] = relevance
            self.similarities[id1] = sim_temp
