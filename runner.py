# coding=utf-8
import uvicorn
from task_async import app

if __name__ == '__main__':
    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 8000,
        log_level = "debug"
    )
