from fastapi import FastAPI
from app.database import Base, engine
from app.routers import campaigns, performance
from utils.log import Log

# Initialize the Logger
Log.INFO("Starting the FastAPI app...")

# Create tables if they do not exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(campaigns.router)
app.include_router(performance.router)

if __name__ == "__main__":
    import uvicorn
    Log.INFO("Running the FastAPI app with Uvicorn...")  # Log application start
    uvicorn.run(app, host="0.0.0.0", port=8800)
