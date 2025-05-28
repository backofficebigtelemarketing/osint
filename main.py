from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.scrapers.google import search_google
from app.scrapers.namechk import check_username
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: str):
    google_results = search_google(query)
    username_results = check_username(query)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "query": query,
        "google_results": google_results,
        "username_results": username_results
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
