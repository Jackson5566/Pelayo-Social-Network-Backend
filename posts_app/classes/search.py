from api.classes.view_logic_executor import ViewLogicExecutor
from necesary_scripts.list_features import separate_by_vowels
from necesary_scripts.search_requirements import get_coincidences
from ..models import PostModel
from rest_framework import status


class SearchAlgorithm(ViewLogicExecutor):
    def __init__(self, request):
        super().__init__(request=request)
        self.search = self.request.query_params.get('search')
        self.list_coincidence = []

    def start_process(self):
        self.convert_search_to_work_string()
        self.set_coincidences_list()
        self.sort_coincidence_list()
        self.set_response()

    def convert_search_to_work_string(self):
        self.search = self.search.strip().lower()
        self.search = separate_by_vowels(self.search)
        self.search = self.delete_repetitive_words()

    def set_coincidences_list(self):
        for element in PostModel.objects.all().order_by("-created"):
            list_content = separate_by_vowels(element.description.lower())
            list_title = separate_by_vowels(element.title.lower())
            coincidences = (get_coincidences(list_title, search=self.search) + get_coincidences(list_content,
                                                                                                search=self.search))
            if coincidences > 0:
                self.list_coincidence.append([coincidences, element])

    def sort_coincidence_list(self):
        self.list_coincidence.sort(key=lambda item: item[0], reverse=True)

    def delete_repetitive_words(self):
        return list(set(self.search))

    def set_response(self):
        self._set_response(data=self.list_coincidence, status=status.HTTP_200_OK)

    def get_searched_posts(self):
        list_unidimensional = [element[1] for element in self.list_coincidence]
        return list_unidimensional
