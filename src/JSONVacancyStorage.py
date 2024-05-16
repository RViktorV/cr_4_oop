from abc import ABC, abstractmethod
from src.class_HeadHunterAPI import HhRuVacancyAPI
from src.vacancy import Vacancy
from config import ROOT_DIR
import json
import os

class VacancyStorage(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass

class JSONVacancyStorage(VacancyStorage):
    def __init__(self, list_vacancies):
        self.list_vacancies = list_vacancies
        self.filepath = os.path.join(ROOT_DIR, 'data', "vacancy_storage.json")
        # Откройте файл для записи в указанной папке
        with open(self.filepath, "w", encoding='utf-8') as f:
            json.dump(self.list_vacancies, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            self.filepath = json.load(file)

        vacancy_storage.append(vacancy)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.filepath, file, ensure_ascii=False, indent=4)

    def get_vacancies(self, **criteria):
        with open(self.filepath, 'r') as file:
            vacancies = json.load(file)

        results = [vacancy for vacancy in vacancies if
                   all(vacancy.get(key) == value for key, value in criteria.items())]
        return results

    def delete_vacancy(self, vacancy_id):
        with open(self.filepath, 'r') as file:
            vacancies = json.load(file)

        vacancies = [vacancy for vacancy in vacancies if vacancy.get('id') != vacancy_id]

        with open(self.filepath, 'w') as file:
            json.dump(vacancies, file)



vacancy = Vacancy( 1,'python',"", '80000-100000', 'опыт работы от 3х лет')
vacancies = vacancy.cast_to_object_list(HhRuVacancyAPI().get_vacancies("develop", 3))

    # Создаем экземпляр класса
storage = JSONVacancyStorage(vacancies)
print(storage)
#
# # Добавляем вакансии
# storage.add_vacancy({'id': 1, 'title': 'Python Developer', 'company': 'Example Corp', 'location': 'New York'})
# with open('vacancy_storage.json', 'r', encoding='utf-8') as file:
#     vacancies = json.load(file)
#     print(vacancies)  # Должен содержать добавленную вакансию
# storage.add_vacancy({'id': 2, 'title': 'Data Scientist', 'company': 'Data Inc', 'location': 'San Francisco'})
#
# with open('vacancy_storage.json', 'r', encoding='utf-8') as file:
#     vacancies = json.load(file)
#     print(vacancies)  # Должен содержать обе добавленные вакансии












# class JSONVacancyStorage(VacancyStorage):
#     def __init__(self, filepath):
#         self.filepath = filepath
#         if not os.path.exists(filepath):
#             folder_path = ROOT_DIR
#             filepath = os.path.join(folder_path, 'data', "vacancies.json")
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 json.dump([], file, ensure_ascii=False, indent=4)  # Создаем пустой список в файле
#
#     def add_vacancy(self, vacancy):
#         with open(self.filepath, 'r') as file:
#             vacancies = json.load(file)
#
#         vacancies.append(vacancy)
#
#         with open(self.filepath, 'w') as file:
#             json.dump(vacancies, file)
#
#     def get_vacancies(self, **criteria):
#         with open(self.filepath, 'r') as file:
#             vacancies = json.load(file)
#
#         results = [vacancy for vacancy in vacancies if
#                    all(vacancy.get(key) == value for key, value in criteria.items())]
#         return results
#
#     def delete_vacancy(self, vacancy_id):
#         with open(self.filepath, 'r') as file:
#             vacancies = json.load(file)
#
#         vacancies = [vacancy for vacancy in vacancies if vacancy.get('id') != vacancy_id]
#
#         with open(self.filepath, 'w') as file:
#             json.dump(vacancies, file)
#
# if __name__ == '__main__':
#     # Создаем экземпляр класса
#
#     storage = JSONVacancyStorage()
#
#     # Добавляем вакансии
#     storage.add_vacancy({'id': 1, 'title': 'Python Developer', 'company': 'Example Corp', 'location': 'New York'})
#     with open('vacancy_storage.json', 'r', encoding='utf-8') as file:
#         vacancies = json.load(file)
#         print(vacancies)  # Должен содержать добавленную вакансию
#     storage.add_vacancy({'id': 2, 'title': 'Data Scientist', 'company': 'Data Inc', 'location': 'San Francisco'})
#
#     with open('vacancy_storage.json', 'r', encoding='utf-8') as file:
#         vacancies = json.load(file)
#         print(vacancies)  # Должен содержать обе добавленные вакансии