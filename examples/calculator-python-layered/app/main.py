from fastapi import FastAPI

from app.calculator.router.calculator_router import router as calculator_router

app = FastAPI(title="OOPforge Calculator (FastAPI layered)")
app.include_router(calculator_router)
