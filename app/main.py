from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import imports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DataPrune API")

app.include_router(imports.router)


@app.get("/")
def root():
    return {"status": "DataPrune API is running"}