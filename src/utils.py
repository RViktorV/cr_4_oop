import os
import json
from src.class_HeadHunterAPI import HhRuVacancyAPI
from src.vacancy import Vacancy
from src.JSONVacancyStorage import JSONVacancyStorage
from config import DATA_PATH
import sys
import time
import panda as pd


def user_interaction():
    print('''Данная программа будет получать информацию о вакансиях с платформы hh.ru в России, 
сохранять ее в файл и позволять удобно работать с ней: добавлять, фильтровать, удалять\n''')
    keyword = input("Введите вакансию (например: python, python developer, back-end developer, тестировщик)\n")
    count = int(input("Введите количество вакансий для загрузки, не больше 2000:"))
    api_hh = HhRuVacancyAPI()
    hh_vacancies = api_hh.get_vacancies(keyword, count)
    # progress_bar(100)
    list_vacancies = Vacancy.cast_to_object_list(hh_vacancies)
    storage = JSONVacancyStorage('vacancies.json')
    storage.add_vacancies(list_vacancies)
    action = 1
    while action != 0:
        action = input('\n1 - Вывести вакансии в столбик на экран\n'
                       '2 - Сохранить все вакансии в json файл\n'
                       '3 - Вывести вакансии из json файла в таблицу на экран и сохранить в файл .txt\n'
                       '4 - Сохранить вакансии из json файла в файл .XLSX(Excel)\n'
                       '5 - Сортировать вакансии по зарплате по возрастанию\n'
                       '6 - Сортировать вакансии по зарплате по убыванию\n'
                       '7 - Удаление вакансии по url\n'
                       '0 - Выход\n')

        if action == "1":
            for vacancy in list_vacancies:
                print(vacancy)
                continue
        elif action == "2":
            storage.add_vacancies(list_vacancies)
            continue
        elif action == "3":
            tabulate()
            continue
        elif action == "3":
            tabulate()
            continue
        elif action == "4":
            get_exls()
            continue
        elif action == "5":
            sorted_vacancies = sorted(list_vacancies)
            for vacancy in sorted_vacancies:
                print(vacancy)
                continue
        elif action == "6":
            sorted_vacancies = sorted(list_vacancies, reverse=True)
            for vacancy in sorted_vacancies:
                print(vacancy)
                continue
        elif action == "7":
            url = input('Введите url для удаления вакансии: ')
            storage.remove_vacancy({"url": url})
            continue
        elif action == "0":
            print("Досвидание")
            exit()

def tabulate():
    """
    Вывод списка вакансий в таблицу и сохранение в файл output.txt
    :param :
    :return:
    """
    file_full_name = os.path.join(DATA_PATH, 'vacancies.json')
    with open(file_full_name, 'r', encoding='utf-8') as f:
        data1 = json.load(f)

    data = []
    for item in data1:
        transformed_item = {
            "Название": item["name"],
            "Регион": item["area"],
            "Ссылка": item["url"],
            "Зарплата от ": item["salary_from"],
            "до": item["salary_to"],
            "валюта": item["currency"],
            "Требования": item["requirement"],
            "Обязанности": item["responsibilities"]
        }
        data.append(transformed_item)

    # Получаем список всех ключей
    keys = data[0].keys() if data else []
    text_table = ''
    # Определяем ширину каждой колонки
    column_widths = {}
    for key in keys:
        column_widths[key] = max(len(str(item[key])) for item in data) if data else len(key)
        column_widths[key] = max(column_widths[key], len(key))

    # Выводим заголовки таблицы
    # with open("output.txt", "w") as f:
    for key in keys:
        text_table += (f"{key.ljust(column_widths[key])} | ")
    text_table += ('\n')

    # Выводим разделительную строку
    for key in keys:
        text_table += (f"{'-' * column_widths[key]} | ")
    text_table += ("\n")

    # Выводим данные
    for item in data:
        for key in keys:
            text_table += (f"{str(item.get(key, '')).ljust(column_widths[key])} | ")
        text_table += ('\n')

    print(text_table)
    file_full_name = os.path.join(DATA_PATH, 'output.txt')
    with open(file_full_name, "w", encoding='utf-8') as f:
        # f.write(text_table)
        print(text_table, file=f)

    print(f'Таблица сохранена в {file_full_name}')

def progress_bar(total):
    bar_length = 50
    for i in range(total + 1):
        progress = i / total
        bar = '[' + '#' * int(progress * bar_length) + ' ' * (bar_length - int(progress * bar_length)) + ']'
        sys.stdout.write('\rЗагрузка: {}% {}'.format(int(progress * 100), bar))
        sys.stdout.flush()
        time.sleep(0.1)  # Эмулируем процесс загрузки
    print('\nЗагрузка завершена.')

def get_exls():
    file_full_name = os.path.join(DATA_PATH, 'vacancies.json')
    with open(file_full_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Преобразование данных в DataFrame
    df = pd.DataFrame(data)

    # Сохранение данных в файл XLSX
    xlsx_file_path = os.path.join(DATA_PATH, "file.xlsx")
    df.to_excel(xlsx_file_path, index=False)

    print(f"Данные успешно сохранены в {xlsx_file_path}")



if __name__ == "__main__":
    user_interaction()