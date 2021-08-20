import os
import json
from fastapi import Request
from pathlib import Path


def sum_cube(num: int):
    result = sum([x ** 3 for x in range(1, num + 1)])
    return {"Сумма чисел возведенных в куб": result}


def series(start: int, finish: int):
    list_even_num = [x for x in range(start, finish + 1) if x % 2 == 0]
    list_odd_num = [x for x in range(start, finish + 1) if x % 2 != 0]
    return {
        "Список четных чисел": list_even_num,
        "Список нечетных чисел": list_odd_num
    }


def prime_numbers_call(num: int):
    i = 2
    while i <= num // 2:
        if num % i != 0:
            if i == num // 2:
                return {"Это число является простым": num}
            i += 1
        else:
            return {"Это число не является простым": num}


def gen_random_name():
    return os.urandom(16).hex()


def get_user(request: Request):
    return request.cookies.get("user")


def write_file(filename: str, numbers: dict, user: str):
    file_path = Path(filename)
    if not file_path.is_file():
        with open(filename, 'w') as new_file:
            new_data = json.dumps(numbers)
            new_file.writelines(new_data)
    else:
        with open(filename, 'r') as file:
            old_data = json.load(file)
            with open(filename, 'w') as f1:
                if user in old_data.keys():
                    old_data[user] += numbers[user]
                    new_data = json.dumps(old_data)
                    f1.writelines(new_data)
                else:
                    old_data[user] = numbers[user]
                    new_data = json.dumps(old_data)
                    f1.writelines(new_data)


def read_file(filename: str, user: str):
    with open(filename, 'r') as file:
        data = json.load(file)
        return sum(data[user])
