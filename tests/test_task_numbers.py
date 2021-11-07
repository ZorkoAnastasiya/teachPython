# coding=utf-8
from random import randint

import httpx
import pytest

from project.task_async import app


@pytest.mark.asyncio
async def test():
    url = "/task_numbers"

    a, b = [randint(0, 100) for _ in "ab"]

    async with httpx.AsyncClient(app=app, base_url="http://asgi") as client:
        resp: httpx.Response = await client.post(url, json=a)
        assert resp.status_code == 200
        assert resp.json() == str(a)

        resp = await client.post(url, json=b)
        assert resp.status_code == 200
        assert resp.json() == str(b)

        resp = await client.post(url, json="stop")
        assert resp.status_code == 200
        assert resp.json() == a + b
