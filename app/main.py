from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import products,sales,stock,users,vendors
import models,database
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(database.engine)

# Include the routers for different modules
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
app.include_router(stock.router, prefix="/stocks", tags=["stocks"])

@app.get('/')
def index():
    return {"message": "Welcome to MyDuka FASTAPI"}
