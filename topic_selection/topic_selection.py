# -*- coding: utf-8 -*-
"""topic_selection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15lh2Kas5nM75UDMtqoyGFoUKh-AVybmt
"""

import pickle
import gensim
import numpy as np
import nltk
import pickle
import gensim
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import LdaModel
from gensim import corpora

nltk.download('punkt')
from nltk.corpus import wordnet as wn
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
nltk.download('stopwords')

"""The code begins by loading a list of documents from a file called "newsgroups" using pickle.

It uses the CountVectorizer from scikit-learn to preprocess the text data. It finds three-letter tokens, removes stop words, eliminates tokens that appear in fewer than 20 documents or more than 20% of the documents.

The preprocessed data is transformed into a sparse matrix representation using fit_transform on the CountVectorizer object. This matrix is converted to a Gensim corpus using Sparse2Corpus from gensim.matutils.

The vocabulary mapping is created as a dictionary where the key-value pairs represent the index-term mapping.

The LDA model is then trained using the LdaModel constructor from gensim.models. It takes the corpus, the number of topics (10 in this case), the vocabulary mapping, and other parameters such as the number of passes and random state.

The lda_topics function prints the topics and the most significant words for each topic using the print_topics method of the trained LDA model. It returns a list of tuples where each tuple represents a topic and its associated words.

The topic_distribution function calculates the topic distribution for a new document (new_doc). It transforms the document using the same CountVectorizer object, converts it to a Gensim corpus, and then uses the trained LDA model's get_document_topics method to obtain the topic distribution. The function returns a list of tuples where each tuple represents a topic and its probability in the new document.

The topic_names function assigns topic names to the topics found based on the given list of topic names. It uses the topic distribution obtained from the topic_distribution function and assigns the closest matching topic name from the list. The function returns a list of strings representing the topic names.
"""

# Load the list of documents
with open('newsgroups', 'rb') as f:
    newsgroup_data = pickle.load(f)

# Use CountVectorizor to find three letter tokens, remove stop_words, 
# remove tokens that don't appear in at least 20 documents,
# remove tokens that appear in more than 20% of the documents
vect = CountVectorizer(min_df=20, max_df=0.2, stop_words='english', 
                       token_pattern='(?u)\\b\\w\\w\\w+\\b')
# Fit and transform
X = vect.fit_transform(newsgroup_data)

# Convert sparse matrix to gensim corpus.
corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)

# Mapping from word IDs to words (To be used in LdaModel's id2word parameter)
id_map = dict((v, k) for k, v in vect.vocabulary_.items())

# Use the gensim.models.ldamodel.LdaModel constructor to estimate 
# LDA model parameters on the corpus, and save to the variable `ldamodel`
ldamodel=LdaModel(corpus=corpus, num_topics=10, id2word=id_map, passes=25, random_state=34)

def lda_topics():
    topics = ldamodel.print_topics(num_topics=10, num_words=10)
   
    return topics
lda_topics()

new_doc = ["\n\nIt's my understanding that the freezing will start to occur because \
of the\ngrowing distance of Pluto and Charon from the Sun, due to it's\nelliptical orbit. \
It is not due to shadowing effects. \n\n\nPluto can shadow Charon, and vice-versa.\n\nGeorge \
Krumins\n-- "]

def topic_distribution():
    
    X_new_doc = vect.transform(new_doc)
    corpus_new_doc = gensim.matutils.Sparse2Corpus(X_new_doc, documents_columns=False)
    topic_distribution = ldamodel.get_document_topics(corpus_new_doc)
    
    
    topic_dist=[set_proba for topic in list(topic_distribution) for set_proba in topic]
    
    return topic_dist

topic_distribution()

def topic_names():
    
    # Define list of topic names
    list_topics = ['Health', 'Science', 'Automobiles', 'Politics', 'Government', 'Travel', 
                   'Computers & IT', 'Sports', 'Business', 'Society & Lifestyle', 'Religion', 'Education']
   
    topics_found = []

    threshold = 0.1

   
    topics_=topic_distribution()
    for t in topics_:
        topics_found.append((list_topics[t[0]]))
                            
    return topics_found
topic_names()

