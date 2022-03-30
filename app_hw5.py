import json
import sqlite3
connect = sqlite3.connect('database.db')
cursor = connect.cursor()

# Функция, которая создает таблицу client если она ежу есть, необходимо вывести об этом сообщение в консоль.
def init():
    try:
        cursor.execute('''
            CREATE TABLE client(
                name varchar(128),
                lastname varchar(128),
                age integer,
                PRIMARY KEY (name, lastname)
            )
        ''')
    except sqlite3.OperationalError:
        print('Такая таблица уже существует')

# Функция, которая добавляет клиентов в таблицу (если клиента с такими фамилией и именем нет в таблице).
def addClient(name, lastname, age):
    try:
        cursor.execute('''
            INSERT INTO client (name, lastname, age)
                VALUES (?, ?, ?)
            ''', [name, lastname, age])
    except sqlite3.IntegrityError:
        print('Клиент с такими именем и фамилией уже существует')
    connect.commit()

# Функция, которая возвращает средний возраст клиентов.
def avgClient():
    cursor.execute('SELECT ROUND(AVG(age),1) FROM client')
    for row in cursor.fetchone():
        print('Средний возраст клиентов:', row)

# Функция, которая получив путь до JSON файла и добавляет клиентов в таблицу (только тех, которые по фамилии и имени отсутствуют в таблице).
def addJs():
    with open('HW_5.json', 'r') as data_file:
        data = json.load(data_file)
    for i in data:
        try:
            cursor.execute('''
                INSERT INTO client (name, lastname, age)
                    VALUES (?, ?, ?)
                ''', [i["name"], i["lastname"], i["age"]])
        except sqlite3.IntegrityError:
            print('Клиент с такими именем и фамилией уже существует')
    connect.commit()

#----------------
def show():
    cursor.execute('SELECT * FROM client')
    for row in cursor.fetchall():
        print(row)



init()
addClient('mike', 'petrov2', 25)
addClient('mike', 'petrov1', 16)
addClient('mike', 'petrov', 54)
addJs()
avgClient()
show()