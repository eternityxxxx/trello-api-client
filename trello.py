
#todo  YES  1.) Добавьте рядом с названием колонки цифру, отражающую количество задач в ней.
#todo  YES  2.) Реализуйте создание колонок.
#todo  YES  3.) Обработайте совпадающие имена задач*

#? ИНФА ДЛЯ ПРОВЕРЯЮЩЕГО
#! Для проверки нужно ввести свои данные авторизации Trello или поиграться с песочницей
#! от skillfactory (ее данные уже введены)
#* Метод read() остался без изменений
#* Метод column() принимает параметр name и создает новую колонку с именем name
#* Метод create() теперь проверяет, есть ли уже задача с именем name в колонке
#* Метод move() теперь собирает задачи с именем name из всех колонок, для последующего выбора    

import sys 
import requests


base_url = "https://api.trello.com/1/{}" 
auth_params = {    
    'key': "e3af0fe8e062b2b6ca5f9c906b8dc7fd",    
    'token': "08100766b52d1e38c68c2e6002abe277062726959a3126dae5a5dbb579ed2d3a",
}
board_id = "y4ohsuNE"    


def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue
        print("Всего задач в колонке '{}': {}".format(column['name'], len(task_data)))      
        for task in task_data:      
            print('\t' + task['name'])    


def column(name):
    # Создаем новую колонку с именем name
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': name, **auth_params})


def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()       
    
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:    
        if column['name'] == column_name:
            # Вытягиваем из нужного столбца все задачи
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            # Вспомогательная переменная flag, чтобы выскочить из внешнего цикла, если бдут совпадения
            flag = True
            # Проверяем на совпадение
            for task in task_data:
                if task['name'] == name:
                    flag = False
                    print("Задача с таким именем уже создана")
                    break
            if not flag:
                break
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break  


def move(name, column_name):
    query = {}   
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Ищем все совпадения и заполяем словарь query по принципу:
    # {'Название колонки': {'name': 'Название задачи', 'id': 'ID задачи'}}      
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:
                query[column['name']] = {'name': task['name'], 'id': task['id']}    

    # UI часть
    print('Список всех найденных совпадений:')
    for key, value in query.items():
       print("В колонке '{}' найдена задача {} c ID {}".format(key, value['name'], value['id']))
    choise = input('Введи название колонки, в которой находится нужная тебе задача: ')

    # Проверяем есть ли в словаре query колонка введенная пользователем
    if choise in query:
        task_id = query[choise]['id']
        # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
        # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
        for column in column_data:
            if [column['name'] == column_name]:
                # И выполним запрос к API для перемещения задачи в нужную колонку    
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
                break
    else:
        print('Ошибка ввода')


if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'column':
        column(sys.argv[2])