# from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def dashboard(request: Request):
    """

    Displays the stock screener dashboard / homepage
    """
    return templates.TemplateResponse("dashboard.html", {"request": request} )


@app.post("/stock")
def create_stock():
     """

    Created a stock and stores it in the database
    """
     return {"code": "success", "message": "stock created"}



