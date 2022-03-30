import sqlite3
import csv
import datetime as dt
from datetime import datetime


connect = sqlite3.connect('database.db')
cursor = connect.cursor()

#создание таблицы
def init():
    cursor.execute('''
        CREATE TABLE if not exists hist_users(
            name varchar(128),
            lastname varchar(128),
            age integer,
            salary integer,
            deleted_flg integer default 0,
            start_dttm datetime default current_timestamp,
            end_dttm datetime default (datetime('2999-12-31 23:59:59'))
        )
    ''')

# Функция добавляет пользователя. Если пользователь с таким именем и фамилией уже есть, то новая запись
# считается актуальной версией информации о пользователе, т.е в предыдущей записи end_dttm меняется на
# datetime('now', '-1 second'), а новой end_dttm присваивается значение технической бесконечности
# datetime('2999-12-31 23:59:59')
def addUser(name, lastname, age, salary):
	cursor.execute('''
		select
			count(*)
		from hist_users
		where name = ? 
		and lastname = ?
		and age = ?
		and salary = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [name, lastname, age, salary])

	if cursor.fetchone()[0] != 0:
		return

	cursor.execute(''' 
		UPDATE hist_users 
		set end_dttm = datetime('now', '-1 second')
		where name = ?
		and lastname = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [name, lastname])

	cursor.execute(''' 
		INSERT INTO hist_users (name, lastname, age, salary)
		VALUES (?, ?, ?, ?)
	''', [name, lastname, age, salary])

	connect.commit()

# Логически удалить пользователя (по имени и фамилии)
def delete(name, lastname):
    cursor.execute('''
        UPDATE hist_users
        set deleted_flg = 1
        where name = ?
        and lastname = ?
    ''', [name, lastname])
    connect.commit()


def showUsers():
	cursor.execute('select * from hist_users')
	for row in cursor.fetchall():
		print(row)



# Функция сохраняет актуальные данные в csv файл. Актуальными считаются те записи, значение dttm которых находится между
# start_dttm и end_dttm, при этом в названии сохраненного файла указываются введенные дата и время.

# Если dttm введен в неверном формате, в csv файл сохраняются все записи из таблицы hist_users, при этом файлу
# присваивается имя all_out.csv.

# Ести выбран вариант не указывать дату и время, то в csv файл сохраняются актуальные на момент вызова функции записи,
# при этом в названии сохраненного файла указываются дата и время на момент вызова функции. Актуальными считаются те
# записи, значение dttm которых находится между start_dttm и end_dttm.
def sql2csvdttm():
	question = input('Введите дату и время (Y/N)?:\n')
	if question.lower() == 'y':
		dttm = input('Введите дату и время в формате yyyy-mm-dd hh:mm:ss\n')
		try:
			cursor.execute('''
				select * from hist_users 
				where ? between start_dttm and end_dttm
			''', (dttm, ))
			with open(dt.datetime.strptime(dttm, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d_%H%M%S_out.csv'), 'w', newline='') as csv_file:
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow([i[0] for i in cursor.description])
				csv_writer.writerows(cursor)
		except ValueError:
			sql2csv()
	else:
		cursor.execute('''
					select * from hist_users 
					where ? between start_dttm and end_dttm
				''', (datetime.now(), ))
		with open(datetime.now().strftime('%Y%m%d_%H%M%S_out.csv'), 'w', newline='') as csv_file:
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in cursor.description])
			csv_writer.writerows(cursor)


# Функция сохраняет все записи в csv файл.
def sql2csv():
	cursor.execute('select * from hist_users')
	with open('all_out.csv', 'w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([i[0] for i in cursor.description])
		csv_writer.writerows(cursor)


init()
addUser('Mike', 'Petrov', 26, 25600)
addUser('Andrey', 'Ivanov', 30, 57500)
addUser('Oleg', 'Sokolov', 35, 25000)
addUser('Denis', 'Chernikov', 45, 67000)
#delete('Mike', 'Petrov')
sql2csvdttm()
showUsers()
#sql2csv()

