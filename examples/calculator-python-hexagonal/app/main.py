from fastapi import FastAPI

from app.presentation.api.calculation.router import router as calculation_router

app = FastAPI(title="OOPforge Calculator (FastAPI hexagonal)")
app.include_router(calculation_router)
