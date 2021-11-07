# coding=utf-8
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from fastapi import Body
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.responses import HTMLResponse

from project import my_function
from project import utility

app = FastAPI()
TypeNumber = Union[int, Dict[str, List[int]]]


@app.get("/", response_class=HTMLResponse)
async def _(response: Response) -> Response:
    utility.apply_cache_headers(response)
    return utility.static_response(
        "project/resources/index.html", response_cls=HTMLResponse
    )


@app.get("/img", response_class=Response)
async def img(response: Response) -> Response:
    utility.apply_cache_headers(response)
    return utility.static_response(
        "project/resources/Green_Python.jpg", binary=True
    )


@app.get("/js", response_class=Response)
async def js(response: Response) -> Response:
    utility.apply_cache_headers(response)
    return utility.static_response("project/resources/index.js")


@app.get("/sum_cube/{num}")
async def cube(num: int) -> Dict[str, str]:
    result: str = my_function.sum_cube(num)
    return {"data": result}


@app.get("/list_num/{start}/{finish}")
async def numbers_list(start: int, finish: int) -> Dict[str, List[int]]:
    return my_function.series(start, finish)


@app.get("/prime_numbers/{num}")
async def prime_numbers(num: int) -> Dict[str, str]:
    result: Optional[str] = my_function.prime_numbers_call(num)
    return {"data": result}


@app.post("/task/add_number")
async def handler(
    request: Request, response: Response, data: str = Body(...)
) -> TypeNumber:
    filename = "Numbers.txt"
    numbers = defaultdict(list)
    user = my_function.get_user(request) or my_function.gen_random_name()
    response.set_cookie("user", user)

    if data == "stop":
        return my_function.read_file(filename, user)
    else:
        assert data.isdigit()
        numbers[user].append(int(data))
        my_function.write_file(filename, numbers, user)
        return {"Number entered": numbers[user]}


@app.post("/task_numbers")
async def handler_2(
    request: Request, response: Response, data: str = Body(...)
) -> Union[Optional[int], str]:
    user = my_function.get_user(request) or my_function.gen_random_name()
    response.set_cookie("user", user)

    if data == "stop":
        return my_function.get_data(user)
    else:
        assert data.isdigit()
        my_function.save_number(user, int(data))
        return data
