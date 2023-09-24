import math
import re

import nltk
import scipy
from nltk.corpus import stopwords
from nltk.stem import porter


def split_into_words(lines):
    result = []
    for line in lines:
        for word in re.split(r'[  \t\n\r\v\f,.!:;\-=/\\()\[\]\'"]', line):
            if len(word) > 1 and word.isalpha():
                result.append(word.lower())
    return result


def stem_words(words):
    stemmer = porter.PorterStemmer()
    return [stemmer.stem(word) for word in words]


def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]


def preprocess_words(document_words):
    nltk.download('stopwords')
    result = []
    for document in document_words:
        preprocessed_document = []
        for words in document:
            words = remove_stopwords(words)
            words = stem_words(words)
            preprocessed_document.append(words)

        result.append(preprocessed_document)
    return result


def calculate_global_term_frequency(document_words):
    map = {}
    for document in document_words:
        for section in document:
            for word in section:
                counter = map.get(word)
                map[word] = 1 if counter is None else counter+1
    result = []
    for word in map.keys():
        result.append((word, map[word]))
    result.sort(key=lambda record: record[1], reverse=True)
    return result


def calculate_term_frequency(document_words):
    result = []
    for document in document_words:
        tf = {}
        number_of_words = len(document[0]) + len(document[1])
        for section in document:
            for word in section:
                counter = tf.get(word)
                tf[word] = 1/number_of_words if counter is None else counter + 1/number_of_words
        result.append(tf)
    return result


def calculate_document_frequency(document_words, vocabulary):
    df = {}
    for word in vocabulary.keys():
        occurences = 0
        for document in document_words:
            if word in document[0] or word in document[1]:
                occurences += 1
        df[word] = occurences
    return df


def calculate_inverse_document_frequency(document_frequency):
    idf = {}
    number_of_documents = len(document_frequency)
    for word in document_frequency.keys():
        df = document_frequency[word]
        idf[word] = math.log(number_of_documents / (df + 1))
    return idf


def calculate_tf_idf(term_frequency, inverse_document_frequency, document_words, alpha):
    result = []
    for i in range(len(term_frequency)):
        title = document_words[i][0]
        content = document_words[i][1]
        document_term_frequency = term_frequency[i]
        document_tf_idf = {}
        for term in content:
            if term in inverse_document_frequency:
                document_tf_idf[term] = (1 - alpha) * document_term_frequency[term] * inverse_document_frequency[term]

        for term in title:
            if term in inverse_document_frequency:
                if term not in document_tf_idf:
                    document_tf_idf[term] = 0
                document_tf_idf[term] += alpha * document_term_frequency[term] * inverse_document_frequency[term]

        result.append(document_tf_idf)
    return result


# With normalization
def tf_idf_into_matrix(tf_idf, vocabulary):
    vocab_size = len(vocabulary)
    number_of_documents = len(tf_idf)
    # matrix = scipy.sparse.dok_matrix((number_of_documents, vocab_size), dtype=float)
    matrix = scipy.sparse.dok_matrix((vocab_size, number_of_documents), dtype=float)
    for i in range(number_of_documents):
        vector_squared_length = 0
        for word in tf_idf[i]:
            if word in vocabulary:
                # matrix[i, vocabulary[word]] = tf_idf[i][word]
                matrix[vocabulary[word], i] = tf_idf[i][word]
                vector_squared_length += tf_idf[i][word] ** 2

        vector_length = vector_squared_length ** 0.5
        if vector_length != 0:
            for word in tf_idf[i]:
                if word in vocabulary:
                    # matrix[i, vocabulary[word]] /= vector_length
                    matrix[vocabulary[word], i] /= vector_length
    return matrix

