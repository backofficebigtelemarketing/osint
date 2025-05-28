from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/search")
def advanced_search(request: Request, input_data: str = Form(...)):
    links = [
        f"https://www.google.com/search?q={input_data}",
        f"https://www.bing.com/search?q={input_data}",
        f"https://yandex.com/search/?text={input_data}",
        f"https://www.linkedin.com/search/?text={input_data}",
        f"https://duckduckgo.com/?q={input_data}",
        f"https://namechk.com/{input_data}",
        f"https://whatsmyname.app/",
        f"https://epieos.com/?q={input_data}",
        f"https://who.is/whois/{input_data}",
        f"https://hunter.io/search/{input_data}",
        f"https://shodan.io/search?query={input_data}",
        f"https://intelx.io/?s={input_data}"
    ]
    return templates.TemplateResponse("results.html", {"request": request, "results": links, "query": input_data})
