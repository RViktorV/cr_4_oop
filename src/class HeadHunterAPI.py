from abc import ABC, abstractmethod
import requests


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
        while self.params.get('page') != 20:
            response = requests.get(self.url, params=self.params)
            data = response.json()['items']
            self.vacancies.extend(data)
            self.params['page'] += 1

        if response.status_code == 200:
            amount_vacancy = len(self.vacancies)
            print(f'Найдено вакансий: {amount_vacancy}\n')
            for vacancy in self.vacancies:
                id = vacancy["id"]
                name = vacancy["name"]
                salary_from = vacancy["salary"]['from']
                if salary_from != None:
                    salary_from = salary_from
                else:
                    salary_from = 0
                salary_to = vacancy["salary"]['to']
                if salary_to != None:
                    salary_to = salary_to
                else:
                    salary_to = 0
                currency = vacancy["salary"]['currency']
                if currency == 'RUR':
                    currency = 'RUB'
                else:
                    currency = currency
                alternate_url = vacancy["alternate_url"]
                request = str(vacancy['snippet']['requirement']).replace("<highlighttext>", "").replace(
                    "</highlighttext>", "")
                Responsibilities = str(vacancy['snippet']['responsibility']).replace("<highlighttext>", "").replace(
                    "</highlighttext>", "")
                area = vacancy["area"]["name"]

                print(f'''id вакансии: {id}\nНазвание: {name}\nМесто работы:{area}
Зарплата: от {salary_from} до {salary_to}, валюта:{currency}\nСсылка:{alternate_url}
Требования:{request}\nОбязанности:{Responsibilities}\n''')

        else:
            return "Ошибка при запросе вакансий:", response.status_code


if __name__ == '__main__':
    hh_api = HhRuVacancyAPI()
    hh_vacancies = hh_api.get_vacancies("python developer")
    print(hh_vacancies)
