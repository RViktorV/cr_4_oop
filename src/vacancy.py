from src.class_HeadHunterAPI import HhRuVacancyAPI
class Vacancy():
    ''' Класс для работы с вакансиями - формирует список объектов класса в файл json'''
    def __init__(self, name, area, salary_from, salary_to, currency, url, requirement, responsibilities):
        self.name = name # Наименование вакансии
        self.area = area  # Город
        self.salary_from = salary_from #Заработная от ...
        self.salary_to = salary_to  # Заработная до ...
        self.currency = currency #Курс по которому платиться заработная плата
        self.url = url  # URL  вакансии
        self.requirement = requirement #Требования к вакансии
        self.responsibilities = responsibilities #Обязанности вакансии
        self.validate()

    def validate(self):
        self.salary_to = self.salary_to if self.salary_to is not None else 0
        self.salary_from = self.salary_from if self.salary_from is not None else 0
        self.currency = 'RUB' if self.currency == 'RUR' else self.currency
        self.requirement = self.requirement if self.requirement is not None else ""
        self.responsibilities = self.responsibilities if self.responsibilities is not None else ""


    def __repr__(self):
        return f'{self.name}, {self.area}, {self.salary_from}, {self.salary_to}, {self.currency}, {self.url}, {self.requirement}, {self.responsibilities}'

    def __str__(self):
        return (f'Вакансия:{self.name}\n'
                f'Город: {self.area}\n'
                f'Зарплата от: {self.salary_from}\n'
                f'Зарплата до: {self.salary_to}\n'
                f'Валюта: {self.currency}\n'
                f'URL вакансии: {self.url}\n'
                f'Требования: {self.requirement}\n'
                f'Обязанности: {self.responsibilities}\n')
    def __eq__(self, other):
        return self.salary_from == other.salary_from and self.salary_to == other.salary_to

    def __lt__(self, other):
        if self.salary_from != other.salary_from:
            return self.salary_from < other.salary_from
        return self.salary_to < other.salary_to
    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        '''Метод класса Vacancy который создает список объектов вакансий из json полученного в классе HhRuVacancyAPI'''
        list_vacancies = []
        amount_vacancy = len(hh_vacancies)
        print(f'Найдено вакансий: {amount_vacancy}\n')
        for vac in hh_vacancies:
            name = vac["name"]
            salary_from = vac["salary"]['from'] if vac["salary"] else 0
            salary_to = vac["salary"]['to'] if vac["salary"] else 0
            currency = vac["salary"]['currency'] if vac["salary"] else 0
            alternate_url = vac["alternate_url"]
            requirement = (str(vac['snippet']['requirement'])
                           .replace("<highlighttext>", "")
                           .replace("</highlighttext>", "") if vac['snippet']['requirement'] else "")
            responsibilities = (str(vac['snippet']['responsibility'])
                                .replace("<highlighttext>", "")
                                .replace("</highlighttext>", "") if vac['snippet']['responsibility'] else "")
            area = vac["area"]["name"]
            vacancy = cls(name, area, salary_from, salary_to, currency, alternate_url, requirement, responsibilities)

            list_vacancies.append(vacancy)
        return list_vacancies

    def to_dict(self):
        '''Метод коорый преобрзует объекты в словарь для дальнейшей его записи в файл json'''
        return {
            "name": self.name,
            "area": self.area,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "url": self.url,
            "requirement": self.requirement,
            "responsibilities": self.responsibilities
        }


if __name__ == '__main__':
    hh_api = HhRuVacancyAPI()
    hh_vacancies = hh_api.get_vacancies("python developer", 10)
    list_vacancies = Vacancy.cast_to_object_list(hh_vacancies)
    for vacancy in list_vacancies:
        print(vacancy)
    print('____________________________________________________________________\n')
    sorted_vacancies = sorted(list_vacancies)
    for vacancy in sorted_vacancies:
        print(vacancy)

    vacancy1 = Vacancy('python', 'Саратов', 50000, 80000, 'EUR', '', 'Знание pycharm', 'знать python')
    vacancy2 = Vacancy('developer', 'Новосибирск', 50000, 70000, "RUB", '', 'Опыт python', "Писать код")
    print(vacancy1)
    print(vacancy2)
    print(vacancy1 == vacancy2)
    print(vacancy1 < vacancy2)
    print(vacancy1 > vacancy2)
