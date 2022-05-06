# from typing import Optional
import models
import yfinance
from fastapi import FastAPI, Query, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel
from models import Stock
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class StockRequest(BaseModel):
    symbol: str

def get_db():
    try:
        db =  SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """

    Displays the stock screener dashboard / homepage
    """

    stocks = db.query(Stock).all()

    print(stocks)


    return templates.TemplateResponse("dashboard.html", {"request": request, "stocks": stocks } )



def fetch_stock_data(id: int):
    db = SessionLocal()

    stock = db.query(Stock).filter(Stock.id == id).first()

    yahoo_data = yfinance.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    # stock.dividend_yield = yahoo_data.info['dividendYield'] * 100

    db.add(stock)
    db.commit()

@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks,  db: Session = Depends(get_db)):
    """

    Created a stock and stores it in the database
    """
    stock = Stock()
    stock.symbol = stock_request.symbol

    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {"code": "success", "message": "stock created"}



