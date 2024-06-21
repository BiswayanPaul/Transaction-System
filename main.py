from fastapi import FastAPI
from routes.credit_routes import router as credit_router
from routes.service_routes import router as service_router

app = FastAPI()

app.include_router(credit_router, prefix="/credits", tags=["credits"])
app.include_router(service_router, prefix="/services", tags=["services"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
