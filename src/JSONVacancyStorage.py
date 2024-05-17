from abc import ABC, abstractmethod
import json
import os
import logging
from src.class_HeadHunterAPI import HhRuVacancyAPI
from src.vacancy import Vacancy
from config import ROOT_DIR


class AbstractVacancyStorage(ABC):
    '''Абстрактный класс для добавления, чтения и удаления вакансий'''

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

    def __init__(self, list_vacancies):
        self.file_path = os.path.join(ROOT_DIR, 'data', "vacancies_storage.json")
        # Запись данных в файл JSON
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump([(vac) for vac in list_vacancies], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        '''Метод который добавляет вакансию в файл "vacancies_storage.json"'''
        try:
            # Чтение существующих данных из файла
            with open(self.file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []

        # Добавление новой вакансии в список
        data.append(vars(vacancy))

        # Запись обновленного списка данных обратно в файл
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_vacancies(self, criteria: dict) -> list:
        '''Метод для извлечения данных из файла на основе заданных критериев'''
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        return [vacancy for vacancy in data if all(vacancy.get(key) == value for key, value in criteria.items())]

    def remove_vacancy(self, criteria):
        '''Метод для удаления информации о вакансиях из файла по указанным критериям'''
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        remaining_vacancies = [vacancy for vacancy in data if
                               not all(vacancy.get(key) == value for key, value in criteria.items())]

        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(remaining_vacancies, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    vacancy1 = Vacancy(1, 'python', 'Саратов', 50000, 70000, 'EUR', '', 'Знание pycharm', 'знать python')
    list_vacancies = vacancy1.cast_to_object_list(HhRuVacancyAPI().get_vacancies("python", 5))

    storage = JSONVacancyStorage(list_vacancies)

    vacancy2 = Vacancy(3, 'developer', 'Новосибирск', 50000, 95000, "RUB", '', 'Опыт python', "Писать код")
    vacancy3 = Vacancy(4, 'python_developer', 'Самара', 75000, 90000, 'RUB', '', 'Пунктуальность',
                       "Писать код на Python")
    vacancy4 = Vacancy(2, 'Тестировщик', 'Красноярск', 55000, 85000, "EUR", '', 'Опыт', "Читать код")

    storage.add_vacancy(vacancy2)
    storage.add_vacancy(vacancy3)
    storage.add_vacancy(vacancy4)

    result = storage.get_vacancies({"name": "python_developer"})
    print(result)
    storage.remove_vacancy({"area": "Красноярск"})

