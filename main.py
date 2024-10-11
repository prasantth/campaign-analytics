from fastapi import FastAPI
from app.database import Base, engine
from app.routers import campaigns, performance

# Create tables if they do not exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(campaigns.router)
app.include_router(performance.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)
