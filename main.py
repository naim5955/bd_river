from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow your frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve 'data' folder as static files at /data path
app.mount("/data", StaticFiles(directory="data"), name="data")

# Optional: Endpoint to list all TIFF files in data folder
@app.get("/files")
def list_files():
    files = [f for f in os.listdir("data") if f.endswith(".tif") or f.endswith(".tiff")]
    return {"files": files}
