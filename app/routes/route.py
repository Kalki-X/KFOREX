from fastapi import APIRouter
from app.services.scrapy import scrape_web, test_scrap_web

router = APIRouter()


@router.get("/kfx")
def kfx():
    return "This is Kalki Forex Exchange Endpoint."


@router.get("/test")
def test():
    result = test_scrap_web()
    return result

@router.get("/kfx/sbm")
def kfx_rate():
    result = scrape_web()
    return {"rates": result}
