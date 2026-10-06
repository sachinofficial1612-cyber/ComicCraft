from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from .schemas import PromptRequest
from .gemini_client import generate_outline, generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf
router=APIRouter()

@router.get("/",response_class=HTMLResponse)
async def home(request: Request): return request.app.state.templates.TemplateResponse("index.html",{"request":request})

async def pipeline(req):
    outline=await generate_outline(req); story=await generate_story(outline,req)
    images=[generate_image(p["image_prompt"],p["panel_number"]) for p in outline]
    layout=build_comic_layout(outline,story,images); pdf=save_pdf(layout)
    return layout,pdf

@router.post("/generate",response_class=HTMLResponse)
async def generate(request: Request, story_prompt: str=Form(...), character_name: str=Form(...), setting: str=Form(...), tone: str=Form(...), art_style: str=Form(...)):
    req=PromptRequest(story_prompt=story_prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style)
    layout,pdf=await pipeline(req)
    return request.app.state.templates.TemplateResponse("comic_preview.html",{"request":request,"layout":layout,"pdf":pdf})

@router.post("/generate-comic/json")
async def generate_json(req: PromptRequest):
    layout,pdf=await pipeline(req); return JSONResponse({"layout":layout,"pdf":pdf})

@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request: Request): return request.app.state.templates.TemplateResponse("export_success.html",{"request":request})

@router.get("/test-image")
async def test_image(prompt: str="brave fox in an enchanted forest"): return {"image":generate_image(prompt,1)}
