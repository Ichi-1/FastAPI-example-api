from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, user, auth, votes

app = FastAPI()
origins = ['https://www.google.ru']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
