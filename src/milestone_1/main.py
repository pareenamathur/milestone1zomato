import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.milestone_1.phase_6_api.routes import router
from src.milestone_1.phase_6_api.service import get_all_restaurants
from src.milestone_1.phase_0_setup.utils import logger

app = FastAPI(
    title="AI Restaurant Recommender",
    description="Refactored Milestone-based API for AI-powered restaurant recommendations.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    """
    logger.info("Starting up AI Restaurant Recommender API...")
    # Pre-load and cache the dataset to ensure fast response times
    try:
        get_all_restaurants()
        logger.info("Dataset loaded and system ready.")
    except Exception as e:
        logger.error(f"Failed to initialize dataset: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Restaurant Recommender API", "docs": "/docs"}

if __name__ == "__main__":
    # Start the server
    uvicorn.run("src.milestone_1.main:app", host="0.0.0.0", port=8000, reload=True)
