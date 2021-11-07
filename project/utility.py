# coding=utf-8
import mimetypes
from pathlib import Path
from typing import Type

from devtools import debug
from fastapi import Response, HTTPException
from starlette import status


def apply_cache_headers(response: Response) -> None:
    cache_params = (
        "immutable",
        "public",
        f"max_age={60*60}"
    )
    response.headers["Cache-Control"] = ','.join(cache_params)


def static_response(
        file_name: str,
        *,
        binary: bool = False,
        response_cls: Type[Response] = Response
) -> Response:

    def get_file_path_safe() -> Path:
        file_path = Path(file_name).resolve()
        debug(file_path)
        if not file_path.is_file():
            raise HTTPException(
                detail = f"File {file_name!r} not found!",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return file_path

    def reading_mode() -> str:
        return "rb" if binary else "r"

    def calc_media_type() -> str:
        return mimetypes.guess_type(file_name)[0] or "text/plain"

    file = get_file_path_safe()
    mode = reading_mode()
    media_type = calc_media_type()

    with file.open(mode) as stream:
        content = stream.read()
        return response_cls(content=content, media_type=media_type)
