from src.class_HeadHunterAPI import HhRuVacancyAPI
from progress_bar import progress_bar
from config import ROOT_DIR
import json
import os


class Vacancy(HhRuVacancyAPI):
    def __init__(self, id, name, url, salary, request):
        self.__id = id
        self.name = name
        self.url = url
        self.salary = salary
        self.request = request

    def __repr__(self):
        return f'{self.name}, {self.url}, {self.salary}, {self.request}'

    def __str__(self):
        return f'Вакансия:{self.name}, зарплата: {self.salary}, требования: {self.request}'

    def cast_to_object_list(self, hh_vacancies=HhRuVacancyAPI().get_vacancies("python", 5)):
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
    vacancy = Vacancy('python', '', '80000-100000', 'опыт работы от 3х лет')
    print(vacancy)
    vac = HhRuVacancyAPI()
    print(vacancy.cast_to_object_list(vac.get_vacancies("develop", 3)))
    progress_bar(100)
