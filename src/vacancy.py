from _ast import keyword

from src.class_HeadHunterAPI import HhRuVacancyAPI


class Vacncy(HhRuVacancyAPI):
    def __init__(self):
        self.vacancies = HhRuVacancyAPI().get_vacancies(keyword)

    def cast_to_object_list(self.vacancies):
        list_vacancies = []
        for vacancy in vacancies:
            id = vacancy["id"]  # количество вакансий
            name = vacancy["name"]  # наименование вакансии
            salary_from = vacancy["salary"]['from']  # зарплата от...
            if salary_from != None:
                salary_from = salary_from
            else:
                salary_from = 0
            salary_to = vacancy["salary"]['to']  # зарплата до...
            if salary_to != None:
                salary_to = salary_to
            else:
                salary_to = 0
            currency = vacancy["salary"]['currency']  #Валюта
            if currency == 'RUR':
                currency = 'RUB'
            else:
                currency = currency
            alternate_url = vacancy["alternate_url"]  # ссылка на вакансию
            request = str(vacancy['snippet']['requirement']).replace("<highlighttext>", "").replace(
                "</highlighttext>", "")  # Требования к вакансии
            responsibilities = str(vacancy['snippet']['responsibility']).replace("<highlighttext>", "").replace(
                "</highlighttext>", "")  #Обязанност сотрудника
            area = vacancy["area"]["name"]  # Место работы
            list_vacancies.append(vacancy)
            return list_vacancies
#             return f'''id вакансии: {id}\nНазвание: {name}\nМесто работы:{area}
# Зарплата: от {salary_from} до {salary_to}, валюта:{currency}\nСсылка:{alternate_url}
# Требования:{request}\nОбязанности:{responsibilities}\n'''


if __name__ == '__main__':
    vacncy = Vacncy()
    print(vacncy)
    print(vacncy.cast_to_object_list(vacancies))
