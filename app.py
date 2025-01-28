from time import sleep
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from markupsafe import Markup
from time import sleep
from random import randint
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sys
import json
from contextlib import asynccontextmanager

with open("models.json") as f:
    models = json.load(f)

# Load model and tokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"



@asynccontextmanager
async def lifespan(app: FastAPI):
    # To run this with a specific model, e.g. deepseek-llam-13b-chat, run:
    # python app.py deepseek-llam-13b-chat
    try:
        with open("temp/model_name.tmp") as f:
            selected_model = models[f.read().strip()]
    except:
        print("Invalid model name, using default deepseek-llm-7b-chat")
        selected_model = models["deepseek-llm-7b-chat"]

    print(f"Loading {selected_model}, this may take some time...")
    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(selected_model)
    global model
    model = AutoModelForCausalLM.from_pretrained(selected_model, device_map="auto")
    print("Model loaded successfully.")
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate_response(request: Request, prompt: str = Form(...)):
    print(prompt)
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt").to("mps")
    # Generate response using the model
    output = model.generate(**inputs, max_length=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    print(response)

    
    return templates.TemplateResponse("response.html", {"request": request, "response": response})


