from fastapi import FastAPI
from titiler.application.main import TitilerApp

app = FastAPI()

# Mount the TiTiler app at root or any path you want:
app.mount("/", TitilerApp())
