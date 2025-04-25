from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analytics
from app.routes import product_recomendation 
from app.routes import sentiment
from app.routes import market_basket 
from app.routes import top_brands
from app.routes import quantity_items
from app.routes import dashboard
from app.routes import costliest_items
from app.routes import cheapest_items
from app.routes import topic
from app.routes import forecasting

app = FastAPI(title="AmazoLens")

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace with specific frontend URL e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🚀 AmazoLens backend is live! And yes... I'm working fine 😎"}

# ✅ Register all your routers
app.include_router(analytics.router)
app.include_router(product_recomendation.router)
app.include_router(market_basket.router)
app.include_router(dashboard.router)
app.include_router(quantity_items.router)  # attach routes
app.include_router(costliest_items.router)  # attach routes
app.include_router(cheapest_items.router)  # attach routes
app.include_router(top_brands.router)  # attach routes
app.include_router(sentiment.router)  # attach routes
app.include_router(forecasting.router)  # attach routes
app.include_router(topic.router)
