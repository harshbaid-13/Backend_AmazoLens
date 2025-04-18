from fastapi import FastAPI
from app.routes import analytics  # import router

app = FastAPI(title="AmazoLens")  # create app instance

app.include_router(analytics.router)  # attach routes
