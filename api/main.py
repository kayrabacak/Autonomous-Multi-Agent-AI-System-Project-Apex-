import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent.executor import run_agent

app = FastAPI(title="Project Apex API")

# Rapor klasörünü oluştur (hata önlemek için)
if not os.path.exists("reports"):
    os.makedirs("reports")

# Statik dosyaları (grafikler vb.) dışarı aç
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    goal: str

@app.get("/")
def read_root():
    return {"message": "Project Apex Hazır! /run endpointine POST isteği atın."}

@app.post("/run")
def run_project_apex(request: Request):
    """
    Ajanı tetikler ve sonucu JSON olarak döner.
    """
    result = run_agent(request.goal)
    return result