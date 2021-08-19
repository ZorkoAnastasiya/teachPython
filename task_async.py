# coding=utf-8
import my_function
from collections import defaultdict
from fastapi import FastAPI, Body, Request, Response

app = FastAPI()


@app.get('/')
async def hello():
    return {"Message": "Hello World!"}
    

@app.get('/sum_cube/{num}')
async def cube(num: int):
    return my_function.sum_cube(num)


@app.get('/list_num/{start}/{finish}')
async def numbers_list(start: int, finish: int):
    return my_function.series(start, finish)


@app.get('/prime_numbers/{num}')
async def prime_numbers(num: int):
    return my_function.prime_numbers_call(num)
 

@app.post('/task/add_number')
async def handler(request: Request, response: Response, data: str = Body(...)):
    filename = "Numbers.py"
    numbers = defaultdict(list)
    user = my_function.get_user(request) or my_function.gen_random_name()
    response.set_cookie("user", user)
    if data == "stop":
        return my_function.read_file(filename, user)
    else:
        assert data.isdigit()
        numbers[user].append(int(data))
        my_function.write_file(filename, numbers, user)
        return {"Введеное число": numbers[user]}
