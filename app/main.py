from fastapi import FastAPI
from app.routes import analytics  # import router

app = FastAPI(title="AmazoLens")  # create app instance

@app.get("/")
def root():
    return {"message": "🚀 AmazoLens backend is live! And yes... I'm working fine 😎"}


app.include_router(analytics.router)  # attach routes
