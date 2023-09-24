import config
import os

from engine_initialization import initialize_search_engine, initialize_svd


def print_first_n(dictionary, n):
    print({key: dictionary[key] for key in list(dictionary.keys())[:n]})


def init(vocabulary_size, alpha_value):
    engine_data_path = os.path.join("..", "engine_data")
    initialize_search_engine(
        # documents_directory_path=os.path.join("../english_content", "machinery"),
        documents_directory_path=os.path.join("..", "wiki_articles"),
        vocabulary_size=vocabulary_size,
        alpha_value=alpha_value,
        matrix_save_as_path=os.path.join(engine_data_path, "search_matrix.npz"),
        vocabulary_save_as_path=os.path.join(engine_data_path, "vocabulary.pkl"),
        inverse_document_frequency_save_as_path=os.path.join(engine_data_path, "idf.pkl"),
        filenames_save_as_path=os.path.join(engine_data_path, "filenames.pkl")
    )


def init_svd(k):
    engine_data_path = os.path.join("..", "engine_data")
    initialize_svd(
        search_matrix_path=os.path.join(engine_data_path, "search_matrix.npz"),
        us_save_as_path=os.path.join(engine_data_path, "us_matrix.npy"),
        v_t_save_as_path=os.path.join(engine_data_path, "v_t_matrix.npy"),
        k=k
    )


init(vocabulary_size=config.VOCABULARY_SIZE, alpha_value=config.ALPHA_VALUE)
init_svd(k=config.SVD_K)
