import sys
import os
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.routes.route import router

kfx = FastAPI(title="Kalki Forex Exchange")

# Include the router
kfx.include_router(router)
