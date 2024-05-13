from abc import ABC, abstractmethod
import requests
from progress_bar import progress_bar


class AbstractVacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class HhRuVacancyAPI(AbstractVacancyAPI):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            "text": '',
            "area": 113,  # Код региона (113 - РФ)
            "page": 0,  #номер страници
            "only_with_salary": True,  # Только вакансии с указанной зарплатой
            "per_page": 100  # Количество вакансий на странице
        }
        self.vacancies = []


    def get_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 1:
            response = requests.get(self.url, params=self.params)
            data = response.json()['items']
            self.vacancies.extend(data)
            self.params['page'] += 1
        return self.vacancies


if __name__ == '__main__':
    hh_api = HhRuVacancyAPI()
    hh_vacancies = hh_api.get_vacancies("python developer")
    print(hh_vacancies)
    progress_bar(100)