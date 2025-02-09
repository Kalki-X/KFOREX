import sys
import os
from dotenv import load_dotenv
from fastapi_utilities import repeat_at
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.routes.route import router

kfx = FastAPI(title="Kalki Forex Exchange")

file_path = 'app/models/mcdb.json'


@router.on_event('startup')
@repeat_at(cron="0 9 * * *")
async def clean_jsonfile():
    # Check if file exists before deleting
    if os.path.exists(file_path):
        # Empty the file using truncate()
        with open(file_path, "r+") as file:
            file.truncate(0)
        print(f"{file_path} has been emptied.")
    else:
        print("File not found!")

# Include the router
kfx.include_router(router)
