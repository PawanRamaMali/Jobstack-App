from fastapi import FastAPI
from core.config import Settings


app = FastAPI(title = Settings.PROJECT_TITLE, version=Settings.PROJECT_VERION)

@app.get("/")
def hello_api():
        return {"detail":"hello world"}