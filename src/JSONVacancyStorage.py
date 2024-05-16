from abc import ABC, abstractmethod
from src.class_HeadHunterAPI import HhRuVacancyAPI
from src.vacancy import Vacancy
from config import ROOT_DIR
import json
import os

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
        # Запись данных в файл JSON
        self.file_path = os.path.join(ROOT_DIR, 'data', "vacancies_storage.json")
        # Откройте файл для записи в указанной папке
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(list_vacancies, f, ensure_ascii=False, indent=4)
    def add_vacancy(self, vacancy):
        '''Метод который добавляет вакансию в файл "vacancies_storage.json"'''
        with open(self.file_path, "a", encoding='utf-8') as f:
            json.dump(vars(vacancy), f, ensure_ascii=False, indent=4)
            f.write('\n')


    def get_vacancies(self, criteria):
        '''Метод для получения данных из файла по указанным критериям'''
        with open(self.file_path, "r", encoding='utf-8') as f:
            vacancies = []
            for line in f:
                data = json.loads(line)
                if all(data.get(key) == value for key, value in criteria.items()):
                    vacancies.append(data)
        return vacancies

    def remove_vacancy(self, criteria):
        '''Метод для удаления информации о вакансиях из файла по указанным критериям'''
        with open(self.file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        with open(self.file_path, "w", encoding='utf-8') as f:
            for line in lines:
                data = json.loads(line)
                if not all(data.get(key) == value for key, value in criteria.items()):
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.write('\n')

if __name__ == '__main__':
    vacancy1 = Vacancy(1,'python', 'Москва', '', 60000, 90000, 'Опыт', "RUB", "")
    list_vacancies = vacancy1.cast_to_object_list(HhRuVacancyAPI().get_vacancies("python", 3))
    # Пример использования:
    storage = JSONVacancyStorage(list_vacancies)
    vacancy2 = Vacancy(3,'developer', 'Новосибирск', '', 90000, 0, 'Опыт python',"RUB", "Писать код")
    # storage.add_vacancy(vacancy2)
    criteria = {"name": "python"}
    criteria2 = {"area": "Москва"}
    print(storage.get_vacancies(criteria))
    storage.remove_vacancy(criteria2)
