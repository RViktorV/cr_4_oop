from src.class_HeadHunterAPI import HhRuVacancyAPI
from progress_bar import progress_bar
from config import ROOT_DIR
import json
import os


class Vacancy(HhRuVacancyAPI):
    ''' Класс для работы с вакансиями - формирует список объектов класса в файл json'''
    def __init__(self, name, url, salary, request):
        self.name = name # Наименование вакансии
        self.url = url # URL  вакансии
        self.salary = salary #Заработная плата
        self.request = request #Требования к вакансии

    def __repr__(self):
        return f'{self.name}, {self.url}, {self.salary}, {self.request}'

    def __str__(self):
        return f'Вакансия:{self.name}, зарплата: {self.salary}, требования: {self.request}'

    def __eq__(self, other): # магический метод сравнеия вакансий на равенство по заработной плате
        return self.salary == other.salary

    def __lt__(self, other):# магический метод сравнеия вакансий на < по заработной плате
        return self.salary < other.salary

    def __gt__(self, other):# магический метод сравнеия вакансий на > по заработной плате
        return self.salary > other.salary

    def cast_to_object_list(self, hh_vacancies=HhRuVacancyAPI().get_vacancies("python", 5)):
        '''Метод класса Vacancy который создает список объектов вакансий из json полученного в калссе HhRuVacancyAPI
        В аргумент подается объект класса HhRuVacancyAPI() обработанный методом  класса get_vacancies("python", 5))
        в который подается ключевое слово для поиска вакансий и количество выводимых вакансий'''
        list_vacancies = []
        amount_vacancy = len(hh_vacancies)
        print(f'Найдено вакансий: {amount_vacancy}\n')
        for vacancy in hh_vacancies:
            id = vacancy["id"]
            name = vacancy["name"]
            salary_from = vacancy["salary"]['from']
            if salary_from is not None:
                salary_from = salary_from
            else:
                salary_from = 0
            salary_to = vacancy["salary"]['to']
            if salary_to is not None:
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
            list_vacancies.append({
                "id": id,
                "name": name,
                "area": area,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "url": alternate_url,
                "requirements": request,
                "responsibilities": Responsibilities
            })
        # Запись данных в файл JSON
        folder_path = ROOT_DIR
        file_path = os.path.join(folder_path, 'data', "vacancies.json")
        # Откройте файл для записи в указанной папке
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(list_vacancies, f, ensure_ascii=False, indent=4)

        return list_vacancies


if __name__ == '__main__':
    vacancy1 = Vacancy('python', '', '70000-100000', 'опыт работы от 3х лет')
    vacancy2 = Vacancy('developer', '', '60000-110000', 'опыт работы программистом')
    print(vacancy1)
    print(vacancy2)
    print(vacancy1 == vacancy2)
    print(vacancy1 < vacancy2)
    print(vacancy1 > vacancy2)
    vac = HhRuVacancyAPI()
    print(vacancy1.cast_to_object_list(vac.get_vacancies("develop", 2)))
    progress_bar(100)
