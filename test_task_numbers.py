# coding=utf-8
import httpx
import pytest
from task_async import app
from random import randint


@pytest.mark.asyncio
async def test_1():
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
