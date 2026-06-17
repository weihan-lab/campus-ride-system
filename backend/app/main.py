import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.database import engine, Base
from .logging import LoggingMiddleware
from .security import SecurityMiddleware
from api.routers import student, driver, bus, taxi, bicycle

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Campus Ride API", 
    version="0.2.0",
    lifespan=lifespan
)

# Add Middlewares
app.add_middleware(LoggingMiddleware)
#app.add_middleware(SecurityMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Transit Routers
app.include_router(student.router, prefix="/api/v1")
app.include_router(driver.router, prefix="/api/v1")
app.include_router(bus.router, prefix="/api/v1")
app.include_router(taxi.router, prefix="/api/v1")
app.include_router(bicycle.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok", "database": "connected"}

# ==========================================

# ==========================================
if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 8080))
    

    uvicorn.run("main:app", host="0.0.0.0", port=port)
