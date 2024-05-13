from abc import ABC, abstractmethod
import requests
from progress_bar import progress_bar

class AbstractVacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword, count):
        pass


class HhRuVacancyAPI(AbstractVacancyAPI):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            "text": '',
            "area": 113,  # Код региона (113 - РФ)
            "page": 0,  # номер страницы
            "only_with_salary": True,  # Только вакансии с указанной зарплатой
            "per_page": 100  # Количество вакансий на странице
        }

    def get_vacancies(self, keyword, count):
        self.params['text'] = keyword
        total_vacancies = []
        while len(total_vacancies) < count:
            response = requests.get(self.url, params=self.params)
            data = response.json()['items']
            total_vacancies.extend(data)
            self.params['page'] += 1
        return total_vacancies[:count]


if __name__ == '__main__':
    hh_api = HhRuVacancyAPI()
    hh_vacancies = hh_api.get_vacancies("python developer", 5)  # Задаем количество выводимых вакансий
    print(hh_vacancies)
    progress_bar(100)
