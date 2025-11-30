from fastapi import FastAPI

app = FastAPI(title="CodeCrew Backend")

@app.get("/")
def read_root():
    return {"message": "CodeCrew backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
