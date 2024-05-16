from src.class_HeadHunterAPI import HhRuVacancyAPI




class Vacancy():
    ''' Класс для работы с вакансиями - формирует список объектов класса в файл json'''
    def __init__(self, id, name, area, url, salary_from, salary_to, request, currency, responsibilities):
        self.__id = id #id  вакансии
        self.area = area #Город
        self.name = name # Наименование вакансии
        self.url = url # URL  вакансии
        self.salary_from = salary_from #Заработная от ...
        self.salary_to = salary_to  # Заработная до ...
        self.currency = currency #Курс по которому платиться заработная плата
        self.request = request #Требования к вакансии
        self.responsibilities = responsibilities #Обязанности вакансии

    def __repr__(self):
        return f'{self.__id}, {self.name}, {self.area}, {self.salary_from}, {self.salary_to}, {self.currency},  {self.url}, {self.request}, {self.responsibilities}'

    def __str__(self):
        return f'id вакансии: {self.__id}, Вакансия:{self.name}, Зарплата от: {self.salary_from}, Зарплата до: {self.salary_to}, Валют:{self.currency}, URL вакансии: {self.url}, Требования: {self.request}, Обязанности: {self.responsibilities}'

    def __eq__(self, other):
        return self.salary_from == other.salary_from and self.salary_to == other.salary_to

    def __lt__(self, other):
        return self.salary_to < other.salary_to

    def __gt__(self, other):
        return self.salary_to > other.salary_to
    # def __eq__(self, other):
    #     return self.salary_to == other.salary_to and self.salary_from == other.salary_from
    #
    # def __lt__(self, other):
    #     return self.salary_to < other.salary_to
    #
    # def __lt__(self, other):
    #     return self.salary_to < other.salary_from
    #
    # def __lt__(self, other):
    #     return self.salary_from < other.salary_from
    #
    # def __gt__(self, other):
    #     return self.salary_from > other.salary_to
    #
    # def __gt__(self, other):
    #     return self.salary_from > other.salary_from
    #
    # def __le__(self, other):
    #     return self.salary_from <= other.salary_to


    def cast_to_object_list(self, hh_vacancies):
        '''Метод класса Vacancy который создает список объектов вакансий из json полученного в калссе HhRuVacancyAPI
        В аргумент подается объект класса HhRuVacancyAPI() обработанный методом  класса get_vacancies("python", 5))
        в который подается ключевое слово для поиска вакансий и количество выводимых вакансий'''
        list_vacancies = []
        amount_vacancy = len(hh_vacancies)
        print(f'Найдено вакансий: {amount_vacancy}\n')
        for vacancy in hh_vacancies:
            id = vacancy["id"]
            name = vacancy["name"]
            salary_from = vacancy["salary"]['from']
            if salary_from is not None:
                salary_from = salary_from
            else:
                salary_from = 0
            salary_to = vacancy["salary"]['to']
            if salary_to is not None:
                salary_to = salary_to
            else:
                salary_to = 0
            currency = vacancy["salary"]['currency']
            if currency == 'RUR':
                currency = 'RUB'
            else:
                currency = currency
            alternate_url = vacancy["alternate_url"]
            request = str(vacancy['snippet']['requirement']).replace("<highlighttext>", "").replace(
                "</highlighttext>", "")
            Responsibilities = str(vacancy['snippet']['responsibility']).replace("<highlighttext>", "").replace(
                "</highlighttext>", "")
            area = vacancy["area"]["name"]
            list_vacancies.append({
                "id": id,
                "name": name,
                "area": area,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "url": alternate_url,
                "requirements": request,
                "responsibilities": Responsibilities
            })

        return list_vacancies


if __name__ == '__main__':
    vacancy1 = Vacancy(1,'python', 'Москва', '', 60000, 90000, 'Опыт', "RUB", "")
    vacancy2 = Vacancy(3,'developer', 'Новосибирск', '', 90000, 0, 'Опыт python',"RUB", "Писать код")
    # print(vacancy1)
    # print(vacancy2)
    print(vacancy1 == vacancy2)
    print(vacancy1 < vacancy2)
    print(vacancy1 > vacancy2)

    # print(vacancy1.cast_to_object_list(HhRuVacancyAPI().get_vacancies("develop", 3)))
    # progress_bar(100)

# # Запись данных в файл JSON
# folder_path = ROOT_DIR
# file_path = os.path.join(ROOT_DIR, 'data', "vacancies.json")
# # Откройте файл для записи в указанной папке
# with open(file_path, "w", encoding='utf-8') as f:
#     json.dump(vacancy, f, ensure_ascii=False, indent=4)
