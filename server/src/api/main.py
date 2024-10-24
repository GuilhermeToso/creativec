from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.src.api.text import router as text
from server.src.api.images import router as images

app = FastAPI(
    title="CreatiVec API",
    description="API for CreatiVec",
    version="0.0.1",
    root_path="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the frontend's origin here instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router)
app.include_router(images.router)
