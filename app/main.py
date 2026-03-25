from fastapi import FastAPI
from app.redis_client import connect_redis, disconnect_redis
from app.controllers.cart_controller import router as cart_router

app = FastAPI(title="Cart Microservice")

@app.on_event("startup")
async def startup():
    await connect_redis()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_redis()

app.include_router(cart_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
