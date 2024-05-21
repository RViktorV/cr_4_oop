import os
import json
import pytest
from src.vacancy import Vacancy
from src.JSONVacancyStorage import JSONVacancyStorage  # Замените `your_module` на имя вашего модуля
from config import DATA_PATH

@pytest.fixture
def sample_vacancy():
    return Vacancy(
        name="Software Developer",
        area="Moscow",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        url="http://example.com",
        requirement="Experience with Python",
        responsibilities="Develop software applications"
    )

@pytest.fixture
def storage():
    file_name = "test_vacancies.json"
    storage = JSONVacancyStorage(file_name)
    yield storage
    # Удаление файла после тестов
    os.remove(storage.file_path)

def test_add_vacancies(storage, sample_vacancy):
    storage.add_vacancies([sample_vacancy])
    with open(storage.file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]["name"] == "Software Developer"

def test_add_vacancy(storage, sample_vacancy):
    storage.add_vacancy(sample_vacancy)
    with open(storage.file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]["name"] == "Software Developer"

def test_get_vacancies(storage, sample_vacancy):
    storage.add_vacancies([sample_vacancy])
    criteria = {"name": "Software Developer"}
    results = storage.get_vacancies(criteria)
    assert len(results) == 1
    assert results[0]["name"] == "Software Developer"

def test_remove_vacancy(storage, sample_vacancy):
    storage.add_vacancies([sample_vacancy])
    criteria_remove = {"name": "Software Developer"}
    storage.remove_vacancy(criteria_remove)
    with open(storage.file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert len(data) == 0

def test_remove_vacancy_not_found(storage, sample_vacancy):
    storage.add_vacancies([sample_vacancy])
    criteria_remove = {"name": "Non-existent"}
    storage.remove_vacancy(criteria_remove)
    with open(storage.file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]["name"] == "Software Developer"