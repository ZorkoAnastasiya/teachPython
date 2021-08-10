# coding=utf-8
from fastapi import FastAPI
from pydantic import BaseModel
from my_function import sum_max


app = FastAPI()


@app.get('/sum_cube/{num}')
async def cube(num: int):
    sum_cube = sum([x**3 for x in range(1, num+1)])
    return {
        "Result": sum_cube
    }


@app.get('/list_num/{start}/{finish}')
async def numbers(start: int, finish: int):
    list_num = [x for x in range(start, finish+1) if x % 2 == 0]
    return {
        "Список четных чисел": list_num
    }


@app.get('/prime_numbers/{num}')
async def prime_numbers(num: int):
    i = 2
    while i <= num//2:
        if num % i != 0:
            if i == num//2:
                return {
                    "Это число является простым": num
                }
            i += 1
        else:
            return {
                "Это число не является простым": num
            }
 
        
class Numbers(BaseModel):
    numbers: list
    

@app.get('/calc')
async def calculation(obj: Numbers):
    num = obj.numbers
    sum_value, max_value = sum_max(*num)
    return {
        "Task": "Calculation",
        "Sum of numbers": sum_value,
        "Maximum value": max_value
    }
