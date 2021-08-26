# coding=utf-8
import os
import json
import traceback
import psycopg2
from contextlib import closing
from fastapi import Request
from pathlib import Path
from typing import Optional, List


def sum_cube(num: int) -> dict:
    """
        Returns the sum of the numbers from 1 to the specified number, cubed.
    """

    result = sum([x ** 3 for x in range(1, num + 1)])

    return {"The sum of the numbers cubed": result}


def series(start: int, finish: int) -> dict:
    """
        Returns two odd and even lists, selected from the specified range.
    """

    list_even_num = [x for x in range(start, finish + 1) if x % 2 == 0]
    list_odd_num = [x for x in range(start, finish + 1) if x % 2 != 0]

    return {
        "List of even numbers": list_even_num,
        "List of odd numbers": list_odd_num
    }


def prime_numbers_call(num: int) -> dict:
    """Determines whether the number is prime or not."""

    i = 2
    while i <= num // 2:
        if num % i != 0:
            if i == num // 2:
                return {"This is a prime number": num}
            i += 1
        else:
            return {"This number is not prime": num}


def gen_random_name() -> str:
    """
        Generates a random number and converts it to 16-digit number system.
    """

    return os.urandom(16).hex()


def get_user(request: Request) -> str:
    """Returns the cookie value for the key 'user'."""

    return request.cookies.get("user")


def write_file(filename: str, numbers: dict, user: str) -> None:
    """Writes data to a file."""

    file_path = Path(filename)

    if not file_path.is_file():
        with open(filename, 'w') as new_file:
            new_data = json.dumps(numbers)
            new_file.writelines(new_data)
    else:
        with open(filename) as file:
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


def read_file(filename: str, user: str) -> int:
    """Finds the sum of the numbers stored in a file."""

    with open(filename) as file:
        data = json.load(file)
        return sum(data[user])


def execute_sql(sql: list) -> List[tuple]:
    """Sends a request to the database."""

    rows = []
    dsn = os.getenv("DATABASE_URL", "")

    with closing(psycopg2.connect(dsn)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(*sql)
            connection.commit()
            try:
                rows = cursor.fetchall()
            except psycopg2.ProgrammingError:
                traceback.print_exc()
            return rows


def get_data(user: str)-> Optional[int]:
    """Retrieving data by name."""

    sql = [
        """
           SELECT number 
           FROM numbers 
           WHERE name = %s;
        """,
        (user,)
    ]

    result = execute_sql(sql)

    try:
        num = result[0][0]
    except IndexError:
        return None

    return num


def user_exists(user: str) -> bool:
    """Checking the presence of names in the database."""

    result = get_data(user)

    return result is not None


def update_number(user: str, number: int) -> None:
    """Updating the available data in the database."""

    num = get_data(user)
    num += number

    sql = [
        """
           UPDATE numbers SET number = %s 
           WHERE name = %s
           RETURNING numbers.number AS number
           ;
        """,
        (num, user)
    ]

    execute_sql(sql)


def insert_new_user(user: str, number: int) -> None:
    """Adding new data to the database."""

    sql = [
        """
           INSERT INTO numbers(name, number)
           VALUES (%s, %s)
           RETURNING numbers.number AS number
           ;
        """,
        (user, number)
    ]

    execute_sql(sql)


def save_number(user: str, number: int)-> None:
    """Saving data to the database."""

    if user_exists(user):
        update_number(user, number)
    else:
        insert_new_user(user, number)
