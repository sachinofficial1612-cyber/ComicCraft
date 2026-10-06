from __future__ import annotations
import json, re
import httpx
from .config import settings

async def _generate(prompt: str, model: str) -> str | None:
    if not settings.gemini_api_key:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"contents":[{"parts":[{"text":prompt}]}]}
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            r = await client.post(url, params={"key": settings.gemini_api_key}, json=body)
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None

def _extract_json(text: str):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.I|re.M).strip()
    start, end = text.find("["), text.rfind("]")
    if start >= 0 and end > start:
        return json.loads(text[start:end+1])
    return json.loads(text)

async def generate_outline(req) -> list[dict]:
    prompt = f'''Create exactly 5 comic panels as JSON array. Story: {req.story_prompt}. Character: {req.character_name}. Setting: {req.setting}. Tone: {req.tone}. Art style: {req.art_style}. Each object must have panel_number, title, scene_description, image_prompt.'''
    raw = await _generate(prompt, settings.gemini_text_model)
    if raw:
        try: return _extract_json(raw)
        except Exception: pass
    return fallback_outline(req)

async def generate_story(outline, req) -> list[dict]:
    prompt = f'''Expand this five-panel comic into concise narration, caption and dialogue for each panel. Return JSON array with panel_number, narration, caption, dialogue. Character {req.character_name}; tone {req.tone}. Outline: {json.dumps(outline)}'''
    raw = await _generate(prompt, settings.gemini_story_model)
    if raw:
        try: return _extract_json(raw)
        except Exception: pass
    return fallback_story(outline, req)

def fallback_outline(req):
    p=req.story_prompt; c=req.character_name; s=req.setting
    beats=[("The Spark","A mysterious clue appears and pulls the hero into the adventure."),("Into the Unknown","The hero enters a dangerous part of the setting and discovers a secret."),("The Challenge","A powerful obstacle blocks the path, forcing the hero to make a brave choice."),("The Turning Point","The hero uses courage and cleverness to change the situation."),("A New Beginning","The adventure ends with a memorable discovery and a promise of more to come.")]
    return [{"panel_number":i+1,"title":t,"scene_description":d,"image_prompt":f"{req.art_style} comic panel, {c} in {s}, story: {p}, {d}, cinematic composition, expressive character, clean line art"} for i,(t,d) in enumerate(beats)]

def fallback_story(outline, req):
    return [{"panel_number":p["panel_number"],"narration":f"{req.character_name} faces the moment with determination. {p['scene_description']}","caption":f"Meanwhile, in {req.setting}...","dialogue":f'{req.character_name}: "There has to be a way forward."'} for p in outline]
