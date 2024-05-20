from abc import ABC, abstractmethod
import json
import os
from src.class_HeadHunterAPI import HhRuVacancyAPI
from src.vacancy import Vacancy
from config import DATA_PATH


class AbstractVacancyStorage(ABC):
    '''Абстрактный класс для добавления, чтения и удаления вакансий'''

    @abstractmethod
    def add_vacancies(self, vacancies):
        pass
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, criteria):
        pass


class JSONVacancyStorage(AbstractVacancyStorage):
    '''Класс  который при  инициализации сохраняет список объектов калсса Vacancy в файл формата json,
     добаляет вакансии в этот файл,
     удаляет вакансии из этого файла и
     выводит вакансии из этого файла'''

    def __init__(self, file_name):
        # Запись данных в файл JSON
        self.file_path = os.path.join(DATA_PATH, file_name)
        self.prepare()

    def __str__(self):
        return (f'Вакансия:{self.name}\n'
                f'Город: {self.area}\n'
                f'Зарплата от: {self.salary_from}\n'
                f'Зарплата до: {self.salary_to}\n'
                f'Валюта: {self.currency}\n'
                f'URL вакансии: {self.url}\n'
                f'Требования: {self.requirement}\n'
                f'Обязанности: {self.responsibilities}\n')

    def prepare(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding='utf-8') as file:
                json.dump([], file)

    def add_vacancies(self, vacancies):
        vacancies_dict = [vacancy.to_dict() for vacancy in vacancies]
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(vacancies_dict, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        '''Метод который добавляет вакансию в файл "vacancies_storage.json"'''
        try:
            # Чтение существующих данных из файла
            with open(self.file_path, "r", encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        except FileNotFoundError:
            data = []

        # Добавление новой вакансии в список
        data.append(vars(vacancy))

        # Запись обновленного списка данных обратно в файл
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def get_vacancies(self, criteria_filtr: dict) -> list:
        '''Метод для извлечения данных из файла на основе заданного критерия'''
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        def matches_criteria(vacancy, criteria_filtr):
            for key, value in criteria_filtr.items():
                vacancy_value = vacancy.get(key)
                if vacancy_value is None or value not in vacancy_value:
                    return False
            return True

        return [vacancy for vacancy in data if matches_criteria(vacancy, criteria_filtr)]


    def remove_vacancy(self, criteria_remove):
        '''Метод для удаления информации о вакансиях из файла по указанным критериям'''
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        remaining_vacancies = [vacancy for vacancy in data if
                               not all(vacancy.get(key) == value for key, value in criteria_remove.items())]

        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(remaining_vacancies, f, ensure_ascii=False, indent=4)

    def print_json(self,file_name):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(json.dumps(data, indent=4, ensure_ascii=False))
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле {file_name}.")

    def save_filtered_vacancies(self, filtered_vacancies, output_file_name):
        output_file_path = os.path.join(DATA_PATH, output_file_name)
        with open(output_file_path, "w", encoding='utf-8') as f:
            json.dump(filtered_vacancies, f, ensure_ascii=False, indent=4)
        print(f"Отфильтрованные вакансии сохранены в {output_file_path}")


if __name__ == '__main__':
    hh_api = HhRuVacancyAPI()
    hh_vacancies = hh_api.get_vacancies("python developer", 1000)
    vacancy = Vacancy('python', 'Москва', 100000, 150000, 'RUR', "https://hh.ru/vacancy/99433253", 'Знание pycharm','знать python')
    list_vacancies = vacancy.cast_to_object_list(hh_vacancies)
    vacancy1 = Vacancy('Крановщик', 'Новосибирск', 60000, 100000, 'RUR', '', 'Уметь водить кран', 'Не бояться высоты')

    storage = JSONVacancyStorage('vacancies.json')
    storage.add_vacancies(list_vacancies)
    storage.add_vacancy(vacancy1)
    filtered_vacancies =storage.get_vacancies({"area":'Новосибирск'})
    for vac in filtered_vacancies:
        print(json.dumps(vac, indent=4, ensure_ascii=False))
    storage.remove_vacancy({"url": "https://hh.ru/vacancy/98901908"})
    # storage.print_json('file.json')

