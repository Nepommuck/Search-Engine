import os
import pickle

from engine.text_analysys import split_into_words

PATH = os.path.dirname(os.path.dirname(__file__))
WIKI_ARTICLES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wiki_articles")


# Windows file illegal characters
def remove_illegal_characters(original_title):
    illegal_characters = "/\\:*?\"<>|"
    title = original_title
    for char in illegal_characters:
        title = title.replace(char, "")
    return title


def get_all_words_and_titles(directory_path):
    words = []
    titles = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)

        if os.path.isfile(file_path):
            file = open(file_path, mode="rb")
            try:
                document = pickle.load(file)
                title_words = split_into_words(lines=[document["title"]])
                content_words = split_into_words(lines=[document["content"]])
                words.append((title_words, content_words))
                titles.append(document["title"])
            except UnicodeDecodeError:
                pass
            finally:
                file.close()
    return words, titles


def read_article(filename):
    file_path = os.path.join(WIKI_ARTICLES_PATH, filename)
    with open(file_path, mode="rb") as file:
        article = pickle.load(file)
    return article
