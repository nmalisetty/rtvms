from fastapi import FastAPI
from .router import log

app = FastAPI()
app.include_router(log.router)
