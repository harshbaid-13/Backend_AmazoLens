from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analytics  # import router

app = FastAPI(title="AmazoLens")  # create app instance
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
@app.get("/")
def root():
    return {"message": "🚀 AmazoLens backend is live! And yes... I'm working fine 😎"}


app.include_router(analytics.router)  # attach routes
