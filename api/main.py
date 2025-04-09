from fastapi import FastAPI

import messages
import users
import groups
from broker.setup import lifespan


app = FastAPI(
    lifespan=lifespan,
    root_path='/api/v1',
    title='Chat service',
    description='Test chat',
)
app.include_router(messages.router, prefix='/messages')
app.include_router(users.router, prefix='/users')
app.include_router(groups.router, prefix='/groups')
