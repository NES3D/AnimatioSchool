import re
import logging
import os
import datetime
from logging.handlers import RotatingFileHandler

def filepath(path):
    def decorator(function):
        def wrapper():
            function(path)
        return wrapper
    return decorator

# Декоратор для логирования
def logger(log_dir):
    def decorator(function):
        def wrapper(input_filename):
            # Создаем директорию для логов, если ее еще нет
            os.makedirs(log_dir, exist_ok=True)

            # Создаем имя лог-файла с текущей датой и временем
            log_filename = os.path.join(log_dir, f'log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

            # Настройка логирования с использованием RotatingFileHandler
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)

            handler = RotatingFileHandler(log_filename, maxBytes=2000, backupCount=5)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # Логируем пути к файлам
            output_filename = input_filename.replace('.txt', '_filtered.txt')
            logger.info(f'Input file: {input_filename}')
            logger.info(f'Output file: {output_filename}\n')

            function(input_filename)

            # Удаляем все обработчики, чтобы не дублировать записи в логах при последующих вызовах
            logger.removeHandler(handler)
            handler.close()
        return wrapper
    return decorator

@filepath('D:\\Art\\AnimationSchoolDev\\DEV\\hw9.txt')
@logger('D:\\Art\\AnimationSchoolDev\\DEV\\logs')
def check_numbers(input_filename):
    output_filename = input_filename.replace('.txt', '_filtered.txt')
    # Чтение данных из файла
    with open(input_filename, 'r') as file:
        data = [line.strip() for line in file.readlines()] # Удаление пробелов

    valid_number = re.compile(r'^0$|^[-+]?0*(?:[1-9]\d{0,5})$|^1000000$|^([1-9]\d*|0*)\.0*(?:[1-9]\d*)$')

    # Запись правильных чисел в файл
    with open(output_filename, 'w') as output_file:
        first_number_written = False
        for i, number in enumerate(data):
            # Проверка, соответствует ли строка паттерну
            if valid_number.match(number):
                # Если соответствует, записываем в файл
                if first_number_written:
                    output_file.write('\n')  # Пишем новую строку, если уже было записано число
                else:
                    first_number_written = True  # Устанавливаем флаг первой записи числа
                output_file.write(number)  # Записываем число
                logging.info(f'Line {i+1}: {number}, testPassed: 1')
            else:
                logging.info(f'Line {i+1}: {number}, testPassed: 0')
check_numbers()