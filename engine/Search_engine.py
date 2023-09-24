import os
import pickle
import numpy as np

from engine.text_analysys import *
from engine.file_helper import PATH, read_article, remove_illegal_characters


class Search_engine:
    def __init__(self, vocabulary_path, inverse_document_frequency_path, filenames_path,
                 search_matrix_path=None, us_matrix_path=None, v_t_matrix_path=None):

        engine_data_path = os.path.join(PATH, "engine_data")
        vocabulary_path, inverse_document_frequency_path, filenames_path = [
                os.path.join(engine_data_path, filename) for filename in
                [vocabulary_path, inverse_document_frequency_path, filenames_path]
            ]
        with open(vocabulary_path, 'rb') as file:
            self.vocabulary = pickle.load(file)
        print(self.vocabulary)
        with open(inverse_document_frequency_path, 'rb') as file:
            self.inverse_document_frequency = pickle.load(file)
        with open(filenames_path, 'rb') as file:
            self.titles = pickle.load(file)

        # No SVD search
        if us_matrix_path is None:
            self.use_svd = False
            search_matrix_path = os.path.join(engine_data_path, search_matrix_path)

            self.search_matrix = scipy.sparse.load_npz(search_matrix_path).tocsr()
            self.number_of_documents = self.search_matrix.shape[1]

        # SVD search
        else:
            print(us_matrix_path)
            self.use_svd = True
            us_matrix_path, v_t_matrix_path = [
                os.path.join(engine_data_path, filename) for filename in [us_matrix_path, v_t_matrix_path]
            ]
            self.us_matrix = np.load(us_matrix_path)
            self.v_t_matrix = np.load(v_t_matrix_path)
            self.number_of_documents = self.v_t_matrix.shape[1]

    def __get_search_vector(self, tf_idf):
        vocab_size = len(self.vocabulary)
        vector = np.zeros(shape=vocab_size, dtype=float)
        length_squared = 0
        for word in tf_idf:
            if word in self.vocabulary:
                vector[self.vocabulary[word]] = tf_idf[word]
                length_squared += tf_idf[word] ** 2

        vector_length = length_squared ** 0.5
        if vector_length != 0:
            for word in tf_idf:
                if word in self.vocabulary:
                    vector[self.vocabulary[word]] /= vector_length
        return vector

    def search(self, query_text, number_of_results=10, max_content_length=250):
        search_words = split_into_words([query_text])
        search_words = preprocess_words([(search_words, [])])

        term_frequency = calculate_term_frequency(document_words=search_words)
        tf_idf = calculate_tf_idf(term_frequency, self.inverse_document_frequency, document_words=search_words, alpha=1)

        search_vector = self.__get_search_vector(tf_idf[0])
        # results = []

        # No SVD search
        if self.use_svd:
            scores = (np.array(search_vector) @ self.us_matrix) @ self.v_t_matrix

        # SVD search
        else:
            scores = np.array(search_vector) @ self.search_matrix

        results = [(i, scores[i]) for i in range(self.number_of_documents)]

        results.sort(key=lambda x: x[1], reverse=True)

        search_results = []
        for index, similarity in results[:number_of_results]:
            title = self.titles[index]
            article = read_article(filename=remove_illegal_characters(title))
            content = article["content"]
            if len(content) > max_content_length:
                content = content[:(max_content_length - 3)] + "..."

            similarity = int(10 ** 3 * similarity) / 10
            search_results.append({
                "title": title, "content": content, "url": article["url"], "similarity": similarity
            })
        return search_results
