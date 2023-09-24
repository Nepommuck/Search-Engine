import config

from django.shortcuts import render
from engine.Search_engine import Search_engine
from search.forms import Search_form


def contact(request):
    if request.method == 'POST':
        # create an instance of our form, and fill it with the POST data
        form = Search_form(request.POST)
        if form.is_valid():
            if config.USE_SVD:
                search_matrix_path = None
                us_path = "us_matrix.npy"
                v_t_path = "v_t_matrix.npy"
            else:
                search_matrix_path = "search_matrix.npz"
                us_path = None
                v_t_path = None

            search_engine = Search_engine(
                vocabulary_path="vocabulary.pkl",
                inverse_document_frequency_path="idf.pkl",
                filenames_path="filenames.pkl",
                search_matrix_path=search_matrix_path,
                us_matrix_path=us_path,
                v_t_matrix_path=v_t_path
            )
            search_results = search_engine.search(
                query_text=form.cleaned_data["search_query"],
                number_of_results=config.NUMBER_OF_RESULTS, max_content_length=config.ARTICLE_CONTENT_DISPLAYED_LENGTH)

            return render(
                request,
                template_name='results.html',
                context={
                    'query': form.cleaned_data["search_query"],
                    'page_list': search_results
                }
            )
    else:
        # this must be a GET request, so create an empty form
        form = Search_form()

    return render(
        request,
        template_name='search.html',
        context={'form': form}
    )
