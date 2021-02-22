#!/usr/bin/env python

import models
from models import Stock
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
from fastapi import FastAPI, Request, Response, Body, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schemas import StockRequest
from background import fetch_stock_data


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def dashboard(request:Request):
    """
    Displays the stock screener dashboard/homepage
    """
    return templates.TemplateResponse("dashboard.html", {"request":request})

@app.post("/stock")
async def create_stock(stock_request:StockRequest, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Creates a stock and stores it in the database
    """
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()
    background_task.add_task(fetch_stock_data, stock.id)
    return {"code":"success", "message":"stock created"}
