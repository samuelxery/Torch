from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch

app = FastAPI()

# allow browser to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# dummy "model" 😭
class Model:
    def predict(self, x):
        return x * 2

model = Model()


@app.get("/")
def home():
    return {"msg": "alive"}

@app.post("/predict")
def predict(data: dict):
    x = data["number"]
    result = model.predict(x)
    return {"result": result}