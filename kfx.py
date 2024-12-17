from fastapi import FastAPI
from app.routes.route import router

kfx = FastAPI(title="Kalki Forex Exchange")

# Include the router
kfx.include_router(router)
