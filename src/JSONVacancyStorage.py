from abc import ABC, abstractmethod
import json
from data import vacancies
class AbstractVacancyStorage(ABC):
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
    def __init__(self, filename=vacancies):
        self.filename = filename

    def add_vacancy(self, vacancy:dict):
        with open(self.filename, 'a') as f:
            json.dump(vacancy, f)
            f.write('\n')

    def get_vacancies(self, criteria):
        with open(self.filename, 'r') as f:
            vacancies = []
            for line in f:
                data = json.loads(line)
                if all(data[key] == value for key, value in criteria.items()):
                    vacancies.append(data)
            return vacancies

    def remove_vacancy(self, criteria):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        with open(self.filename, 'w') as f:
            for line in lines:
                data = json.loads(line)
                if not all(data[key] == value for key, value in criteria.items()):
                    json.dump(data, f)
                    f.write('\n')

# Пример использования:
storage = JSONVacancyStorage("vacancies.json")
print(storage)
storage.add_vacancy({"title": "Python Developer", "link": "https://example.com/vacancy1", "salary": 100000, "description": "Looking for a Python developer with experience in Django."})
storage.add_vacancy({"title": "Data Scientist", "link": "https://example.com/vacancy2", "salary": 120000, "description": "Seeking a data scientist proficient in machine learning."})

print(storage.get_vacancies({"title": "Python Developer"}))
storage.remove_vacancy({"title": "Python Developer"})
print(storage.get_vacancies({"title": "Python Developer"}))