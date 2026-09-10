"""Main application entry point for FairTalent-Engine."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router

app = FastAPI(
    title="FairTalent-Engine ⚡ Algorithmic Bias & Psychometric Validity Platform",
    description=(
        "Production-grade Fair-ML analytics pipeline and psychometric audit platform. "
        "Evaluates talent selection decisions against the EEOC Four-Fifths Rule (29 CFR § 1607.4), "
        "NYC Local Law 144 AEDT standards, and EU AI Act Annex III High-Risk AI mandates. "
        "Engineered by Fabio Torres (M.Sc. Data Engineering & 10+ Years Cognitive/Behavioral Science Leadership)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
