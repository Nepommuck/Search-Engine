from django import forms


class Search_form(forms.Form):
    search_query = forms.CharField(max_length=1000)
