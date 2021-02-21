from fastapi import FastAPI, Request, Response, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def dashboard(request:Request):
    """
    Displays the stock screener dashboard/homepage
    """
    return templates.TemplateResponse("dashboard.html", {"request":request, "message": "Hello world"})

@app.post("/stock")
async def create_stock():
    """
    Creates a stock and stores it in the database
    """
    return {"code":"success", "message":"stock created"}
