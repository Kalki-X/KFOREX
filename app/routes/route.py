from fastapi import APIRouter
from app.services.scrapy import scrape_web, test_scrap_web, test_download_rate_sheet
from app.services.excel import get_ratesheets

router = APIRouter()


@router.get("/kfx")
def kfx():
    return "This is Kalki Forex Exchange Endpoint."


@router.get("/test&bank=sbm")
def test():
    result = test_scrap_web()
    return result

@router.get("/test&bank=mcb")
def test_mcb():
    result = get_ratesheets()
    return result

@router.get("/kfx/?a=rates&bank=sbm")
def kfx_rate():
    result = scrape_web()
    return {"rates": result}
