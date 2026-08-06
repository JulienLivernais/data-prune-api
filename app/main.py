from fastapi import FastAPI
from app.routers import imports, reports, records


app = FastAPI(
    title="DataPrune API",
    description="Automated data cleaning pipeline for heterogeneous business data.",
)

app.include_router(imports.router, tags=["Imports"])
app.include_router(reports.router, tags=["Reports"])
app.include_router(records.router, tags=["Records"])

@app.get("/")
def root():
    return {"status": "DataPrune API is running"}


