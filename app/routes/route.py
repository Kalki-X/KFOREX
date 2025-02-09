from fastapi import APIRouter
# from app.services.scrapy import scrape_web, test_scrap_web
from app.services.excel import main_mrates

router = APIRouter()

@router.get("/kfx")
def kfx():
    return "This is Kalki Forex Exchange Endpoint."

# @router.get("/test")
# def test():
#     x = excel_line()
#     return x

@router.get("/kfx&bank=mcb")
def kfx_mcb():
    result = main_mrates()
    return result

# @router.get("/kfx&bank=sbm")
# def kfx_rate():
#     result = scrape_web()
#     return {"rates": result}
