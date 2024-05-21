import pytest
from src.vacancy import Vacancy  # Замените `your_module` на имя вашего модуля

@pytest.fixture
def sample_vacancy_data():
    return {
        "name": "Software Developer",
        "area": "Moscow",
        "salary_from": 100000,
        "salary_to": 150000,
        "currency": "RUR",
        "url": "http://example.com",
        "requirement": "Experience with Python",
        "responsibilities": "Develop software applications"
    }

def test_init(sample_vacancy_data):
    vacancy = Vacancy(**sample_vacancy_data)
    assert vacancy.name == "Software Developer"
    assert vacancy.area == "Moscow"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.currency == "RUB"
    assert vacancy.url == "http://example.com"
    assert vacancy.requirement == "Experience with Python"
    assert vacancy.responsibilities == "Develop software applications"

def test_validate(sample_vacancy_data):
    sample_vacancy_data['currency'] = 'RUR'
    sample_vacancy_data['salary_to'] = None
    vacancy = Vacancy(**sample_vacancy_data)
    vacancy.validate()
    assert vacancy.currency == 'RUB'
    assert vacancy.salary_to == 0

def test_cast_to_object_list():
    hh_vacancies = [{
        "name": "Software Developer",
        "area": {"name": "Moscow"},
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "alternate_url": "http://example.com",
        "snippet": {"requirement": "Experience with Python", "responsibility": "Develop software applications"}
    }]
    vacancies = Vacancy.cast_to_object_list(hh_vacancies)
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].name == "Software Developer"
    assert vacancies[0].area == "Moscow"
    assert vacancies[0].salary_from == 100000
    assert vacancies[0].salary_to == 150000
    assert vacancies[0].currency == "RUB"
    assert vacancies[0].url == "http://example.com"
    assert vacancies[0].requirement == "Experience with Python"
    assert vacancies[0].responsibilities == "Develop software applications"

def test_to_dict(sample_vacancy_data):
    vacancy = Vacancy(**sample_vacancy_data)
    vacancy_dict = vacancy.to_dict()
    assert vacancy_dict["name"] == "Software Developer"
    assert vacancy_dict["area"] == "Moscow"
    assert vacancy_dict["salary_from"] == 100000
    assert vacancy_dict["salary_to"] == 150000
    assert vacancy_dict["currency"] == "RUB"
    assert vacancy_dict["url"] == "http://example.com"
    assert vacancy_dict["requirement"] == "Experience with Python"
    assert vacancy_dict["responsibilities"] == "Develop software applications"