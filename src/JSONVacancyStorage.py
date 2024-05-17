from abc import ABC, abstractmethod
from src.class_HeadHunterAPI import HhRuVacancyAPI
from src.vacancy import Vacancy
from config import ROOT_DIR
import logging
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


    def get_vacancies(self, criteria: dict) -> list:
        """
        Метод для извлечения данных из файла на основе заданных критериев.

        :param criteria: Словарь пар ключ-значение для фильтрации данных
        :return: Список словарей, соответствующих критериям
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            '''Файл, путь к которому указан в self.file_path, 
            открывается в режиме чтения с кодировкой UTF-8.'''
            vacancies = [] #Инициализация списка вакансий
            for line in file: #Чтение и обработка каждой строки файла
                line = line.strip()  # Удалить конечные символы новой строки
                if not line:
                    continue
                try: #Строка пытается преобразоваться в словарь с помощью json.loads. Если строка не является корректным JSON, генерируется предупреждение и строка пропускается.
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    logging.warning(f"Пропуск недействительной строки JSON: {e}")
                    continue

                if all(data.get(key) == value for key, value in criteria.items()):
                    '''Каждая строка (уже преобразованная в словарь) проверяется на соответствие критериям. 
                    Если все ключи и их значения из criteria совпадают с данными в словаре, 
                    этот словарь добавляется в список vacancies'''
                    vacancies.append(data)

        return vacancies #Возвращается список словарей, которые соответствуют критериям фильтрации

    def remove_vacancy(self, criteria):
        '''Метод для удаления информации о вакансиях из файла по указанным критериям'''
        remaining_vacancies = []
        '''Создается пустой список remaining_vacancies, куда будут добавляться вакансии, 
        которые не соответствуют критериям удаления.'''

        with open(self.file_path, "r", encoding='utf-8') as f:
            '''Файл, путь к которому указан в self.file_path, 
            открывается в режиме чтения с кодировкой UTF-8. 
            Все строки файла считываются и сохраняются в список lines.'''

            lines = f.readlines()

        for line in lines:
            '''Происходит итерация по каждой строке файла. 
            Строки обрезаются от пробельных символов. 
            Пустые строки пропускаются. Если строка не является корректным JSON, она пропускается.'''
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not all(data.get(key) == value for key, value in criteria.items()):
                '''Каждая строка (уже преобразованная в словарь) 
                проверяется на соответствие критериям. 
                Если данные не соответствуют всем ключам и значениям из criteria, 
                вакансия добавляется в список remaining_vacancies.'''
                remaining_vacancies.append(data)

        with open(self.file_path, "w", encoding='utf-8') as f:
            '''Файл открывается в режиме записи с кодировкой UTF-8. 
            Все вакансии из remaining_vacancies записываются обратно в файл. 
            Каждая вакансия сериализуется в строку JSON с использованием json.dump 
            и записывается в файл с последующим добавлением новой строки.'''
            for vacancy in remaining_vacancies:
                json.dump(vacancy, f, ensure_ascii=False, indent=4)
                f.write('\n')


if __name__ == '__main__':
    vacancy1 = Vacancy(1,'python', 'Саратов', 50000, 70000, 'EUR', '', 'Знание pycharm', 'знать python')
    list_vacancies = vacancy1.cast_to_object_list(HhRuVacancyAPI().get_vacancies("python", 1))
    # Пример использования:
    storage = JSONVacancyStorage(list_vacancies)
    vacancy2 = Vacancy(3,'developer', 'Новосибирск', 50000, 95000, "RUB",'', 'Опыт python', "Писать код")
    vacancy3 = Vacancy(4, 'python_developer', 'Самара', 75000, 90000, 'RUB ', '', 'Пунктуальность', "Писать код на Python")
    vacancy4 = Vacancy(2, 'Тестировщик', 'Красноярск', 55000, 85000, "EUR", '', 'Опыт', "Читать код")
    storage.add_vacancy(vacancy2)
    storage.add_vacancy(vacancy3)
    storage.add_vacancy(vacancy4)
    # print(storage.get_vacancies({"name": "Тестировщик"}))
    # storage.remove_vacancy({"currency": "EUR"})
