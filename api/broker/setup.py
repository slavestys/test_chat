from contextlib import asynccontextmanager
import typing

from fastapi import FastAPI

from .producer import producer


@asynccontextmanager
async def lifespan(fast_app: FastAPI) -> typing.AsyncGenerator[None, None]:
    async with producer:
        yield
