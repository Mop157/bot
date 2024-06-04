
Понял, давайте перечислим все доступные функции и классы модуля `datetime` в Python:

### Классы:

1. **`date`**: Представляет дату (год, месяц, день).
   - `datetime.date(year, month, day)`: Создает объект `date` для указанной даты.
   - Методы:
     - `date.today()`: Возвращает текущую дату.
     - `date.fromisoformat(iso_string)`: Создает объект `date` из строки в формате ISO (например, `'YYYY-MM-DD'`).

2. **`time`**: Представляет время (часы, минуты, секунды, микросекунды).
   - `datetime.time(hour, minute, second, microsecond)`: Создает объект `time` для указанного времени.
   - Методы:
     - `time.min`: Минимально возможное время.
     - `time.max`: Максимально возможное время.

3. **`datetime`**: Представляет комбинацию даты и времени.
   - `datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)`: Создает объект `datetime` для указанной даты и времени.
   - Методы:
     - `datetime.now()`: Возвращает текущую дату и время.
     - `datetime.combine(date, time)`: Сочетает объекты `date` и `time` в объект `datetime`.
     - `datetime.strptime(date_string, format)`: Преобразует строку в объект `datetime` с заданным форматом.

4. **`timedelta`**: Представляет разницу между двумя датами или временем.
   - `datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)`: Создает объект `timedelta`.
   - Позволяет выполнять арифметические операции с датами и временем (например, сложение и вычитание).

### Функции:

1. **Функции для работы с текущим временем и датой**:
   - `datetime.today()`: Возвращает текущую дату и время (аналог `datetime.now()` без учета часового пояса).
   - `datetime.now(tz=None)`: Возвращает текущую дату и время с учетом часового пояса, если указан.

2. **Функции форматирования**:
   - `strftime(format)`: Преобразует объект `date` или `datetime` в строку с заданным форматом.
   - `strptime(date_string, format)`: Преобразует строку в объект `date` или `datetime` с заданным форматом.

3. **Функции для работы с часовыми поясами**:
   - `datetime.timezone(offset, name=None)`: Создает объект часового пояса для указанного смещения времени от UTC.

4. **Другие полезные функции**:
   - `datetime.combine(date, time)`: Сочетает объекты `date` и `time` в объект `datetime`.
   - `datetime.fromtimestamp(timestamp, tz=None)`: Возвращает объект `datetime` для указанной временной метки.

Это полный список классов и функций модуля `datetime` в Python. Вы можете использовать эти возможности для работы с датами, временем и выполнения различных операций, связанных с временем в ваших программах. Если у вас есть конкретные вопросы по использованию каких-либо из этих функций или классов, не стесняйтесь спрашивать!

Конечно! Модуль `os` в Python предоставляет широкий набор функций для взаимодействия с операционной системой. Давайте рассмотрим все его функции подробно:

1. `os.name`: Возвращает строку, указывающую на тип операционной системы.

2. `os.environ`: Возвращает словарь с переменными окружения в виде пар ключ-значение.

3. `os.getcwd()`: Получает текущий рабочий каталог.

4. `os.chdir(path)`: Изменяет текущий рабочий каталог на указанный.

5. `os.listdir(path='.')`: Возвращает список файлов и каталогов в указанном каталоге.

6. `os.mkdir(path, mode=0o777, *, dir_fd=None)`: Создает новый каталог с указанным именем.

7. `os.makedirs(name, mode=0o777, exist_ok=False)`: Создает каталоги с заданным именем и вложенной структурой.

8. `os.remove(path, *, dir_fd=None)`: Удаляет файл по указанному пути.

9. `os.rmdir(path, *, dir_fd=None)`: Удаляет каталог.

10. `os.removedirs(path)`: Удаляет каталоги и подкаталоги с заданным именем и вложенной структурой.

11. `os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)`: Переименовывает файл или каталог.

12. `os.renames(old, new)`: Переименовывает каталоги и подкаталоги с заданным именем и вложенной структурой.

13. `os.replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None)`: Заменяет файл или каталог.

14. `os.walk(top, topdown=True, onerror=None, followlinks=False)`: Генерирует имена файлов в дереве каталогов.

15. `os.path.join(path, *paths)`: Объединяет пути в один.

16. `os.path.exists(path)`: Проверяет существует ли файл или каталог.

17. `os.path.isdir(path)`: Проверяет является ли путь каталогом.

18. `os.path.isfile(path)`: Проверяет является ли путь файлом.

19. `os.path.abspath(path)`: Возвращает абсолютный путь.

20. `os.path.basename(path)`: Возвращает имя файла или каталога из пути.

21. `os.path.dirname(path)`: Возвращает имя родительского каталога из пути.

22. `os.path.split(path)`: Разбивает путь на кортеж, содержащий имя каталога и имя файла.

23. `os.path.splitext(path)`: Разделяет путь на базовый путь и расширение файла.

24. `os.path.getsize(path)`: Возвращает размер файла в байтах.

25. `os.path.isabs(path)`: Проверяет, является ли путь абсолютным.

26. `os.path.join(path, *paths)`: Объединяет пути в один, учитывая особенности разделителя в файловых системах.

27. `os.path.normpath(path)`: Нормализует путь, удаляя двойные и одинарные точки, а также обрабатывая символы "..".

28. `os.path.realpath(path)`: Возвращает каноническое имя пути.

29. `os.path.relpath(path, start=os.curdir)`: Возвращает относительный путь от стартового пути до указанного пути.

30. `os.path.samefile(path1, path2)`: Проверяет, указывают ли два пути на один и тот же файл.

##################################

import sqlite3

# Подключение к базе данных или создание новой, если она не существует
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Создание таблицы пользователей
c.execute('''CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )''')

# Добавление новых пользователей
c.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ('john_doe', 'john@example.com', 30))
c.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ('jane_smith', 'jane@example.com', 25))
conn.commit()

# Изменение возраста пользователя
c.execute("UPDATE users SET age = 35 WHERE username = 'john_doe'")
conn.commit()

# Удаление пользователя
c.execute("DELETE FROM users WHERE username = 'jane_smith'")
conn.commit()

# Выборка данных из таблицы
c.execute("SELECT * FROM users")
rows = c.fetchall()

# Вывод результатов
for row in rows:
    print(row)

# Закрытие соединения с базой данных
conn.close()



##################################

# Создание

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER
);

# добавление

INSERT INTO books (title, author, year) VALUES ('Harry Potter', 'J.K. Rowling', 1997);
INSERT INTO books (title, author, year) VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 1925);
INSERT INTO books (title, author, year) VALUES ('To Kill a Mockingbird', 'Harper Lee', 1960);

# вивод на консоль

SELECT * FROM books;

# итог

id |      title       |        author        | year
---|------------------|----------------------|-----
1  | Harry Potter     | J.K. Rowling         | 1997
2  | The Great Gatsby | F. Scott Fitzgerald | 1925
3  | To Kill a Mockingbird | Harper Lee    | 1960

# обновления информации

UPDATE books SET year = 2000 WHERE id = 1;

# удаление через айди

DELETE FROM books WHERE id = 3;


##################################

import requests

# Отправляем GET-запрос на веб-сайт для получения HTML-кода главной страницы
response = requests.get('https://www.example.com')

# Получаем код состояния ответа
print("Код состояния:", response.status_code)

# Получаем текст ответа (HTML-код страницы)
html_content = response.text
print("HTML-код страницы:", html_content[:200])  # Выводим только первые 200 символов HTML-кода

# Попытка интерпретировать ответ как JSON
try:
    json_data = response.json()
    print("JSON-данные:", json_data)
except ValueError:
    print("Невозможно интерпретировать ответ как JSON")

# Получаем заголовки ответа
headers = response.headers
print("Заголовки ответа:", headers)

# Получаем URL-адрес ресурса
url = response.url
print("URL ресурса:", url)

# Проверяем, успешен ли запрос (код состояния в диапазоне 200-299)
if response.ok:
    print("Запрос успешен")
else:
    print("Запрос завершился ошибкой")

# Выводим куки, отправленные сервером в ответе
cookies = response.cookies
print("Куки:", cookies)


##################################

num = "12345"
alpha = "abcde"
alnum = "123abc"
lower = "abc"
upper = "ABC"

print(num.isdigit())  # Выведет: True
print(alpha.isalpha())  # Выведет: True
print(alnum.isalnum())  # Выведет: True
print(lower.islower())  # Выведет: True
print(upper.isupper())  # Выведет: True

text = "Это строка с несколькими словами словами"
print(text.count("слова"))  # Выведет: 2

text = "Это пример строки для поиска"
print(text.find("строки"))  # Выведет: 9
print(text.index("поиска"))  # Выведет: 23

text = "Это пример строки"
print(text.startswith("Это"))  # Выведет: True
print(text.endswith("строки"))  # Выведет: False

text = "привет, мир!"
print(text.capitalize())  # Выведет: Привет, мир!

text = "Это строка"
print(text.upper())  # Выведет: ЭТО СТРОКА
print(text.lower())  # Выведет: это строка

message = "Привет, мир!"
print(message.replace("мир", "Миша"))  # Выведет: Привет, Миша!

text = "   Пробелы в начале и в конце   "
print(text.strip())  # Выведет: Пробелы в начале и в конце

words = ['Это', 'пример', 'строки', 'для', 'демонстрации', 'метода', 'join']
new_sentence = " ".join(words)  # Объединяем элементы списка в строку, разделяя их пробелом
print(new_sentence)  # Выведет: Это пример строки для демонстрации метода join

sentence = "Это пример строки для демонстрации метода split"
words = sentence.split()  # Разбиваем строку на список слов
print(words)  # Выведет: ['Это', 'пример', 'строки', 'для', 'демонстрации', 'метода', 'split']

#  2. **Режимы открытия файлов**:
   - `'r'`: открытие файла для чтения. Файл должен существовать.
   - `'w'`: открытие файла для записи. Если файл не существует, он будет создан. Если файл существует, его содержимое будет перезаписано.
   - `'a'`: открытие файла для добавления данных в конец файла. Если файл не существует, он будет создан.
   - `'b'`: открытие файла в бинарном режиме.
   - `'t'` (по умолчанию): открытие файла в текстовом режиме.
   - `'+'`: открытие файла для обновления (чтения и записи).                        3. **Чтение из файла**:
   - Для чтения данных из файла можно использовать методы `read()`, `readline()` или `readlines()`.
   - Метод `read()` читает весь файл в одну строку.
   - Метод `readline()` читает одну строку из файла.
   - Метод `readlines()` читает все строки из файла в список строк. 

##################################

my_list = [1, 2, 3, 4, 5]
for number in my_list:
    print(number)
# перебов списка, итог 1 2 3 4 5

my_string = "Hello"
for char in my_string:
    print(char)
# перебор строки, итог h e l l o

my_dict = {'a': 1, 'b': 2, 'c': 3}
for key in my_dict:
    print(key, my_dict[key])
# перебов элементов словника

my_list = ['a', 'b', 'c']
for index, value in enumerate(my_list):
    print(index, value)
# Этот код использует функцию enumerate(), чтобы получить и индекс, и значение элемента списка.

for i in range(5):
    print(i)
# итог 0 1 2 3 4

numbers = [1, 2, 3, 4, 5]
squared = [x ** 2 for x in numbers]
print(squared)  # Выведет: [1, 4, 9, 16, 25]

numbers = [1, 2, 2, 3, 3, 4, 5]
unique_numbers = {x for x in numbers}
print(unique_numbers)  # Выведет: {1, 2, 3, 4, 5}

numbers = [1, 2, 3, 4, 5]
squared_dict = {x: x ** 2 for x in numbers}
print(squared_dict)  # Выведет: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

numbers = [1, 2, 3, 4, 5]
squared_tuple = tuple(x ** 2 for x in numbers)
print(squared_tuple)  # Выведет: (1, 4, 9, 16, 25)



##################################

x = 5
name = "John"

+, -, *, /, а также операторы сравнения: ==, !=, <, >, <=, >=.

a = 10
b = 3
c = a + b  # 13

##################################

# Запрос имени пользователя
name = input("Введите ваше имя: ")

# Приветствие пользователя
print("Привет, " + name + "!")

##################################

x = 10

if x > 5:
    print("x больше 5")

x = 10

if x > 5:
    print("x больше 5")
else:
    print("x меньше или равно 5")

x = 10

if x > 10:
    print("x больше 10")
elif x == 10:
    print("x равно 10")
else:
    print("x меньше 10")

##################################

# Перебор элементов списка
fruits = ["яблоко", "банан", "вишня"]
for fruit in fruits:
    print(fruit)

##################################

# Печать чисел от 1 до 5
num = 1
while num <= 5:
    print(num)
    num += 1
    
##################################

# Использование оператора break
num = 1
while True:
    print(num)
    num += 1
    if num > 5:
        break

##################################

# Использование оператора continue
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

def greet(name):
    print("Привет, " + name + "!")
    

# Вызов функции с аргументом
greet("Анна")

##################################

def add(a, b):
    return a + b

# Вызов функции и использование возвращаемого значения
result = add(3, 5)
print(result)  # Выведет: 8

##################################

fruits = ["яблоко", "банан", "вишня"]

point = (10, 20)

person = {"имя": "Иван", "возраст": 30, "город": "Москва"}

unique_numbers = {1, 2, 3, 4, 5}

##################################

with open("example.txt", "r") as file:
    content = file.read()
    print(content)

##################################

try:
    x = 10 / 0
except ZeroDivisionError:
    print("Деление на ноль невозможно")

##################################

x = -1

if x < 0:
    raise ValueError("Число должно быть положительным")

##################################

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Привет, меня зовут", self.name, "и мне", self.age, "лет")

# Создание объекта класса Person
person1 = Person("Иван", 30)

# Вызов метода объекта
person1.greet()

##################################

import numpy as np

# Создание массива NumPy
arr = np.array([1, 2, 3, 4, 5])

# Использование функций NumPy
mean_value = np.mean(arr)
print("Среднее значение:", mean_value)

##################################

import requests

# Выполнение GET-запроса к сайту
response = requests.get("https://api.github.com")

# Вывод статуса запроса
print("Статус запроса:", response.status_code)

# Вывод содержимого ответа
print("Ответ:", response.text)

##################################

# Открытие файла для чтения
file = open("example.txt", "r")

# Открытие файла для записи
file = open("example.txt", "w")

# Открытие файла для добавления данных
file = open("example.txt", "a")

# Чтение всего содержимого файла
content = file.read()

# Чтение одной строки из файла
line = file.readline()

# Чтение всех строк из файла в список
lines = file.readlines()

# Запись строки в файл
file.write("Hello, world!\n")

# закрить файл
file.close()

##################################

import os

# Получение текущей директории
current_directory = os.getcwd()

# Создание новой директории
os.mkdir("new_directory")

# Переход в другую директорию
os.chdir("new_directory")

# Получение списка файлов и директорий в текущей директории
files = os.listdir()

##################################

import sys

# Вывод сообщения об ошибке в stderr
sys.stderr.write("Это сообщение об ошибке\n")

# Прерывание выполнения программы с указанием кода ошибки
sys.exit(1)

##################################

import sys

# Получение списка аргументов командной строки
args = sys.argv

# Первый аргумент - имя скрипта
script_name = args[0]

# Последующие аргументы - переданные данные
other_args = args[1:]

##################################

import threading

# Определение функции для выполнения в отдельном потоке
def print_numbers():
    for i in range(5):
        print(i)

# Создание нового потока
thread = threading.Thread(target=print_numbers)

# Запуск потока
thread.start()

# Ожидание завершения потока
thread.join()

##################################

import asyncio

# Определение корутины для выполнения асинхронно
async def print_numbers():
    for i in range(5):
        print(i)
        await asyncio.sleep(1)

# Запуск цикла событий для выполнения корутин
asyncio.run(print_numbers())

##################################

import tkinter as tk

# Создание главного окна
root = tk.Tk()
root.title("Мое первое окно")

# Создание метки (Label) с текстом
label = tk.Label(root, text="Привет, мир!")
label.pack()

# Запуск главного цикла обработки событий
root.mainloop()

##################################

from flask import Flask

# Создание экземпляра Flask
app = Flask(__name__)

# Определение маршрута (route) и представления (view)
@app.route('/')
def hello_world():
    return 'Привет, мир!'

# Запуск веб-приложения
if __name__ == '__main__':
    app.run(debug=True)

##################################

from sklearn.linear_model import LinearRegression
import numpy as np

# Создание обучающих данных
X_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([2, 4, 6, 8, 10])

# Создание модели линейной регрессии
model = LinearRegression()

# Обучение модели на обучающих данных
model.fit(X_train, y_train)

# Вывод коэффициентов модели
print("Коэффициенты модели:", model.coef_)

# Прогнозирование значений
X_test = np.array([[6], [7], [8]])
predictions = model.predict(X_test)
print("Прогнозы модели:", predictions)



import nltk
from nltk.tokenize import word_tokenize

# Загрузка ресурсов NLTK
nltk.download('punkt')

# Пример текста
text = "NLTK makes it easy to work with human language data."

# Токенизация текста
tokens = word_tokenize(text)

# Вывод токенов
print("Токены:", tokens)
