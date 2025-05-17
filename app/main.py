from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Import our logging system
from app.utils.logger import get_app_logger
from app.utils.middleware_logs import (
    RequestLoggingMiddleware,
    ResponseTimeLoggingMiddleware,
    get_request_logger,
)

# Create application logger
logger = get_app_logger(module_name="main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Application startup")
    yield
    # Shutdown logic
    logger.info("Application shutdown")


app = FastAPI(
    title="Japan Honeymoon Travel Assistant",
    description="A telegram bot providing comprehensive travel assistance for honeymooners in Japan",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ResponseTimeLoggingMiddleware)


@app.get("/")
async def root():
    """Health check endpoint."""
    logger.info("Health check called")
    return {
        "status": "online",
        "message": "Japan Honeymoon Travel Assistant API is running",
    }


@app.get("/item/{item_id}")
async def read_item(item_id: int, request: Request):
    logger.info(f"Getting item by ID: {item_id}")
    return {"item_id": item_id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_items(request: Request, skip: int = 0, limit: int = 10):
    logger.info(f"Listing items with skip={skip}, limit={limit}")
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_itemp(
    item_id: str, request: Request, q: str | None = None, short: bool = False
):
    logger = get_request_logger(request=request)
    logger.info(f"Getting item details for ID: {item_id}, q={q}, short={short}")
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item, request: Request):
    logger.info(f"Creating item: {item.name}")
    return item


# Example of endpoint that raises an exception
@app.get("/error")
async def trigger_error(request: Request):
    """Endpoint to demonstrate error logging."""
    logger.info("Error endpoint called - will raise exception")
    # This will be caught by the logging middleware
    raise ValueError("This is a test error")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting application server")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
