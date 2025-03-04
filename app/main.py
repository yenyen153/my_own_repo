from app import models, api_post_path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.databases import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_post_path.router)


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}


#uvicorn app.main:app --host localhost --port 8000 --reload
#http://localhost:8000/api/healthchecker
