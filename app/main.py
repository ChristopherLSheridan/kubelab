import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Kubelab API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/environment")
def environment():
    return {"environment": os.getenv("APP_ENV", "unknown")}
