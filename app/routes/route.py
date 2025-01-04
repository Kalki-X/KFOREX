from fastapi import APIRouter
from app.services.scrapy import scrape_web, test_scrap_web
from app.services.excel import get_ratesheets

router = APIRouter()

@router.get("/kfx")
def kfx():
    return "This is Kalki Forex Exchange Endpoint."

@router.get("/kfx&bank=sbm")
def test():
    result = test_scrap_web()
    return result

@router.get("/kfx&bank=mcb")
def kfx_mcb():
    result = get_ratesheets()
    return result

@router.get("/kfx/?a=rates&bank=sbm")
def kfx_rate():
    result = scrape_web()
    return {"rates": result}
