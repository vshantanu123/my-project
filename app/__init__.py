import os

from fastapi import FastAPI

from dependencies import life_span

os.makedirs("./uploaded_documents", exist_ok=True)
os.makedirs("./logs/", exist_ok=True)

# start the application by instantiating the FastAPI class, this calls the life_span function
# from dependencies.py

app = FastAPI(lifespan=life_span)
