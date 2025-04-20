from fastapi import FastAPI
from app.routes import analytics  # import router
from app.routes import product_recomendation 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AmazoLens")  # create app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "🚀 AmazoLens backend is live! And yes... I'm working fine 😎"}


app.include_router(analytics.router)  # attach routes
app.include_router(product_recomendation.router)