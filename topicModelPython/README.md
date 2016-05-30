Topic Modeling with Python
===

Author : **Pierre Le Bras**, Heriot Watt University

Date : **May 2016**

Note : This 'tutorial' was written for a UNIX system, and tested on a Ubuntu 14.04 machine.

Introduction
---
Topic modeling is a data mining, or text mining, technique.
It automatically generates topics from a corpus of text documents.

There are many forms of topic modelling techniques, like Probabilistic latent semantic indexing (PLSI).
However the most commonly used topic model is Latent Dirichlet Allocation (LDA), introduced by **David Blei**.
In addition to the common ideas of what is a topic model, in
[his article](http://www.cs.princeton.edu/~blei/papers/Blei2012.pdf), Blei describes a topic model using the following
intuitions :
- a *document* contains a certain set of words
- a *topic* is a distributions over words, i.e. words will be "packed" together in a certain number of topics, each
word having a certain weight in the topic
- words are assigned together in a topic if they appear often together in the documents
- therefore documents are also a distribution over topics, i.e. one document can be represented by many topics, with a
different weight.

Description of the pipeline
---
1. Documents are read and put into a map with **key = document id** and **value = text**.
2. The texts in the map are lemmatised. Lemmatising the text will produce an array of the words in the text reduced to
their base (e.g. *words* becomes *word*, *computing* (verb) becomes *compute*). In addition to lemmatisation, this
process also removes stopwords (e.g. *and*, *to*, *in*, *a*, *the*, ...) and numbers.
3. The lemmatised map is used to produce a matrix of words' occurrences in documents.
4. This matrix is used by the LDA algorithm to produce a topic model.
5. Topics (words and their weight) and per topic documents distribution are retrieved.
6. Using the per topic documents distribution, similarities between topics are computed. Two topics being used with
similar weights in the same documents are more likely to be close.
7. These three elements : *topics*, *per topic documents distribution* and *topics similarity matrix* are then output.

Modules, classes and packages of the application
---
- *main.py* (module), the application entry point
- *topicModel* package :
    - *TopicModel.py* (class), where the previous pipeline is managed
    - *lemmatizer.py* (module), provides functions to make the lemmatisation
    - *TopicSimilarities.py* (class), computes the topic similarities
    - *dataIO.py* module, manages the input and output data, i.e. read the documents and save the topic model data. It
    contains two classes : *DataReader* and *DataWriter*.

Getting started
---
First make sure you have python 3.4+ and *pip* (python's library manager) installed on your machine.

Note : if python 2 is also installed on your machine there might be issues with the version of python and pip used in
the terminal. You can force the version used by typing *python3* and *pip3*.

Then, using pip, install *nltk* (Natural Language ToolKit), which will help us for the lemmatisation. Open a terminal
and type :
>       $ sudo pip install nltk

Once nltk is installed, you need to download its datasets, to do so, open the python console :
>       $ python

load nltk :
>       >>> import nltk

now you can download datasets using :
>       >>> nltk.download('dataset_name')

note the quotes around the dataset name. The names of the datasets needed are the following :
- *stopwords* (stopwords removal)
- *wordnet* (lemmatizing)
- *averaged_perceptron_tagger* (tagging words)

You can now exit the python console :
>       >>> exit()

You will also need *numpy* :
>       $ sudo pip install numpy

And of course the *lda* package:
>       $ sudo pip install lda

Running the topic modeling
---
You should be able to run the topic modeling only interacting with the *main.py* file.

The first line :
>       from topicModel.TopicModel import TopicModel
loads the TopicModel class in the application

Then we create the topic model object :
>       tm = TopicModel(n_topics=30)
*n_topics* represents the number of topics that will be generated, default value is 20. There are other attributes you
can specify :
- *n_words_per_topic*, the number of words per topic, default is 10
- *n_iter*, number of iterations the modeling process will go through, default is 1500
- *stopwords_array*, an array of terms you specifically want to exclude from the modeling process, e.g. words that create
overly specific topics, default is an empty array
- *alpha* and *eta*, defaults are respectively 0.1 and 0.01, those attributes are used to as parameters of the Dirichlet
distributions, respectively per-document topic distribution and per-topic word distribution.

After that we read the file containing the text data :
>       tm.read_data(data_file_name='text_data_file.json',
>                             path=['documentsArray'],
>                             id_accessor='docId',
>                             text_accessors=['text1', 'text2'])
Assumptions :
- the data file is in json format
- all documents are stored somewhere in this file in an array
- all documents are represented by an object

Arguments :
- *data_file_name* is the path to the data file, relative to the location of the *main.py* script. We recommend that you
use a dedicated folder structure for all data files. For instance a folder *data* next to the script and a subfolder
*input* in which you can put the text data file. Therefore the path specified should be
*data/input/text_data_file.json*. Default value is the empty string and will cause an exception.
- *path*, in case the array in which the documents are stored is not the root of the file, this argument allows you to
specify the keys under which to find the document array. For instance if your json architecture is :
    >       {
    >           key1 : ... ,
    >           key2 : {
    >               subkey1 : {
    >                   documentArray : [
    >                       // here are the documents
    >                    ] ,
    >                   ...
    >               } ,
    >               ...
    >           }
    >       }
    then the value you should pass to *path* is \[ 'key2', 'subkey1', 'documentArray' \]. Default value is an empty
    array.
- *id_accessor*, the key to use to access the document id. Default value is 'id'.
- *text_accessors*, the keys to use to access the document text. Default value is the empty array. You can specify
multiple keys here, in case you wish to include a title for instance or if there are multiple text fields.

Now we can make the topic model :
>       tm.model()

And finally save the topic model in a file :
>       tm.save_data(file_name='topic_model.json')
Again *file_name* is the path to the file relative to the *main.py* script. If you create a dedicated folder (e.g.
*topicModels* under *data*) don't forget to prepend it before the actual filename.

To execute *main.py* simply, open your terminal, go to the directory containing the script :
>       $ cd path/to/folder/
and type :
>       $ python main.py

License
---
This project is under the [Creative Commons Attribution License](https://creativecommons.org/licenses/by/4.0/).

You can share and adapt the code for any purpose, but must give credit, indicate any changes and provide link to the
license.

See LICENSE for full details.