import pickle
import numpy as np

from sklearn.decomposition import TruncatedSVD
from file_helper import get_all_words_and_titles
from text_analysys import *


def create_vocabulary(preprocessed_words, vocabulary_size):
    global_term_frequency = calculate_global_term_frequency(preprocessed_words)

    vocabulary = {}
    for i in range(vocabulary_size):
        word, _ = global_term_frequency[i]
        vocabulary[word] = i
    return vocabulary


def get_idf(preprocessed_words, vocabulary):
    document_frequency = calculate_document_frequency(preprocessed_words, vocabulary)
    inverse_document_frequency = calculate_inverse_document_frequency(document_frequency)
    return inverse_document_frequency


def generate_search_matrix(preprocessed_words, vocabulary, inverse_document_frequency, alpha_value):
    term_frequency = calculate_term_frequency(preprocessed_words)

    tf_idf = calculate_tf_idf(term_frequency, inverse_document_frequency, preprocessed_words, alpha_value)
    search_matrix = tf_idf_into_matrix(tf_idf, vocabulary)
    return search_matrix.tocoo()


def initialize_search_engine(documents_directory_path, vocabulary_size, alpha_value,
                             matrix_save_as_path, vocabulary_save_as_path,
                             inverse_document_frequency_save_as_path, filenames_save_as_path):

    print("Engine full initialization started.")
    document_words, filenames = get_all_words_and_titles(documents_directory_path)
    print("Reading documents finished.")
    preprocessed_words = preprocess_words(document_words)
    print("Word preprocessing finished.")
    vocabulary = create_vocabulary(preprocessed_words, vocabulary_size)
    print("Creating vocabulary finished.")
    inverse_document_frequency = get_idf(preprocessed_words, vocabulary)
    print("Calculating IDF finished.")
    search_matrix = generate_search_matrix(preprocessed_words, vocabulary, inverse_document_frequency, alpha_value)
    print("Generating search matrix finished.")

    scipy.sparse.save_npz(matrix_save_as_path, search_matrix.tobsr())
    with open(vocabulary_save_as_path, 'wb') as file:
        pickle.dump(vocabulary, file)
    with open(inverse_document_frequency_save_as_path, 'wb') as file:
        pickle.dump(inverse_document_frequency, file)
    with open(filenames_save_as_path, 'wb') as file:
        pickle.dump(filenames, file)
    print("All components saved succesfully.")


def initialize_svd(search_matrix_path, us_save_as_path, v_t_save_as_path, k=100):
    search_matrix = scipy.sparse.load_npz(search_matrix_path)

    print("SVD calculation started.")
    svd = TruncatedSVD(n_components=k)
    svd.fit(search_matrix)

    us_matrix = svd.transform(search_matrix)
    v_t_matrix = np.array(svd.components_)
    print("SVD calculation finished.")

    with open(us_save_as_path, 'wb') as file:
        np.save(file, us_matrix)
    with open(v_t_save_as_path, 'wb') as file:
        np.save(file, v_t_matrix)
    print("SVD matrices saved succesfully.")
