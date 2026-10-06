# ComicCraft — AI Comic Story Creator

A runnable FastAPI/Jinja2 implementation of the uploaded ComicCraft specification.

## Run on Windows
```powershell
cd D:\ComicCraft
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## AI keys
The app runs in local demo mode without keys. For live Gemini generation, put `GEMINI_API_KEY` in `.env`. `HF_API_KEY` is reserved for adding a hosted image provider; the included local fallback creates deterministic comic-style panel art so the complete workflow remains runnable on a normal machine.
