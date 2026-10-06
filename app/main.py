from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import router

ROOT=Path(__file__).resolve().parent.parent
app=FastAPI(title="ComicCraft AI Comic Story Creator",version="1.0.0")
app.mount("/static",StaticFiles(directory=ROOT/"static"),name="static")
app.state.templates=Jinja2Templates(directory=str(ROOT/"templates"))
app.include_router(router)

@app.get("/health")
async def health(): return {"status":"ok","service":"ComicCraft"}
