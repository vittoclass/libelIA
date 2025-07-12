from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx, os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")

class Evaluacion(BaseModel):
    alumno: str
    evaluacion: str
    rubrica: str

@app.post("/evaluar")
async def evaluar(data: Evaluacion):
    prompt = f"""EVALUACIÓN IA

Alumno: {data.alumno}
Rúbrica: {data.rubrica}
Texto del estudiante: {data.evaluacion}

Responde con feedback, puntaje y análisis en JSON"""

    headers = {"Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"}
    body = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": { "type": "json_object" }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.mistral.ai/v1/chat/completions", json=body, headers=headers)
        data = res.json()
    return data

@app.get("/memoria/{alumno}")
async def memoria(alumno: str):
    # Dummy context response (será real con base de datos)
    return {"learningContext": f"Memoria del alumno {alumno} aún no implementada."}

@app.post("/guardar")
async def guardar(data: dict):
    # Aquí se guardará en Supabase o PostgreSQL
    return {"status": "Guardado (ficticio por ahora)"}