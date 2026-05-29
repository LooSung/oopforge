from fastapi import FastAPI

from app.presentation.api.order.order_router import router as order_router

app = FastAPI(title="OOPforge Order Example")
app.include_router(order_router)
