from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/search")
def search_google(request: Request, query: str = Form(...)):
    google_links = [f"https://www.google.com/search?q={query}"]
    return templates.TemplateResponse("results.html", {"request": request, "results": google_links, "title": "Google Search"})

@app.post("/epieos")
def epieos_search(request: Request, identifier: str = Form(...)):
    epieos_url = f"https://epieos.com/?q={identifier}"
    return templates.TemplateResponse("results.html", {"request": request, "results": [epieos_url], "title": "Epieos Lookup"})

@app.post("/whois")
def whois_lookup(request: Request, domain: str = Form(...)):
    whois_url = f"https://who.is/whois/{domain}"
    return templates.TemplateResponse("results.html", {"request": request, "results": [whois_url], "title": "Whois Info"})

@app.post("/image")
def image_search(request: Request, image: UploadFile = File(...)):
    return templates.TemplateResponse("results.html", {"request": request, "results": ["https://images.google.com", "https://yandex.com/images"], "title": "Reverse Image Search"})
