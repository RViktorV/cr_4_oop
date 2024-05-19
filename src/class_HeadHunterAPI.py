from abc import ABC, abstractmethod
import requests


class AbstractVacancyAPI(ABC):
    '''Абстрактный класс для работы с API сервиса с вакансиями'''
    @abstractmethod
    def get_vacancies(self, keyword, count):
        pass


class HhRuVacancyAPI(AbstractVacancyAPI):
    '''Класс для работы с платформой hh.ru.'''
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            "text": '',
            "area": 113,  # Код региона (113 - РФ)
            "page": 0,  # номер страницы
            "only_with_salary": True,  # Только вакансии с указанной зарплатой
            "per_page": 100  # Количество вакансий на странице
        }

    def get_vacancies(self, keyword, count): # count - количество вакансий для выгрузки
        '''Метод класс подключается к API и получать вакансии в формате json'''
        self.params.update({'text': keyword}) # Ключевое слово для поиска вакансий
        total_vacancies = []
        if count > 2000:
            print('Вы ввели не правильное количество вакансий для загрузки, количество не должно превышать 2000')
            count = 2000
            print("Количество загруженных вакансий будет равно 2000")
        while len(total_vacancies) < count:
            response = requests.get(self.url, params=self.params)
            data = response.json()['items']
            total_vacancies.extend(data)
            self.params['page'] += 1
            return total_vacancies[:count]

if __name__ == '__main__':
    hh_api = HhRuVacancyAPI()
    hh_vacancies = hh_api.get_vacancies("python developer", 100)  # Задаем количество выводимых вакансий
    print(hh_vacancies)

