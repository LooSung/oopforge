from fastapi import FastAPI

from app.presentation.api.command_router import router as command_router
from app.presentation.api.query_router import router as query_router

app = FastAPI(title="OOPforge Calculator (FastAPI hexagonal + CQRS)")
app.include_router(command_router)
app.include_router(query_router)
