from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    analytics,  # import router
    product_recomendation,
    top_brands,
    topic,
)

app = FastAPI(title="AmazoLens")  # create app instance
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def root():
    return {"message": "🚀 AmazoLens backend is live! And yes... I'm working fine 😎"}


app.include_router(analytics.router)  # attach routes
app.include_router(product_recomendation.router)
app.include_router(top_brands.router)  # attach routes
app.include_router(topic.router)
