from api.classes.access_data_logic_controller import AccessDataLogicController
from necesary_scripts.list_features import separate_by_vowels
from necesary_scripts.search_requirements import get_coincidences
from ..models import PostModel


class SearchAlgorithm(AccessDataLogicController):
    def __init__(self, request):
        super().__init__(request=request)
        self.search = self.request_manager.request.query_params.get('search')
        self.list_coincidence = []

    def start_process(self):
        self.convert_search_to_work_string()
        self.set_coincidences_list()
        self.sort_coincidence_list()
        self.queryset = self.get_searched_posts()

    def set_coincidences_list(self):
        posts = PostModel.objects.select_related('user').prefetch_related('categories', 'files', 'likes', 'dislikes',
                                                                          'messages').all().order_by('-created')
        for element in posts:
            list_content = separate_by_vowels(element.description.lower())
            list_title = separate_by_vowels(element.title.lower())
            coincidences = (get_coincidences(list_title, search=self.search) + get_coincidences(list_content,
                                                                                                search=self.search))
            if coincidences > 0:
                self.list_coincidence.append([coincidences, element])

    def convert_search_to_work_string(self):
        self.search = self.search.strip().lower()
        self.search = separate_by_vowels(self.search)
        self.search = self.delete_repetitive_words()

    def sort_coincidence_list(self):
        self.list_coincidence.sort(key=lambda item: item[0], reverse=True)

    def delete_repetitive_words(self):
        return list(set(self.search))

    def get_searched_posts(self):
        list_unidimensional = [element[1] for element in self.list_coincidence]
        return list_unidimensional
