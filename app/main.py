from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analytics  # import router
from app.routes import product_recomendation 
from app.routes import sentiment
from app.routes import market_basket 
from app.routes import top_brands
from app.routes import quantity_items
from app.routes import costliest_items
from app.routes import cheapest_items
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AmazoLens")  # create app instance
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "🚀 AmazoLens backend is live! And yes... I'm working fine 😎"}


app.include_router(analytics.router)  # attach routes
app.include_router(product_recomendation.router)

app.include_router(market_basket.router)
app.include_router(quantity_items.router)  # attach routes
app.include_router(costliest_items.router)  # attach routes
app.include_router(cheapest_items.router)  # attach routes
app.include_router(top_brands.router)  # attach routes
app.include_router(sentiment.router)  # attach routes
