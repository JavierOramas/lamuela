from time import sleep
from typing_extensions import final
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from markupsafe import Markup
from time import sleep
from random import randint
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import string
import json
from contextlib import asynccontextmanager

with open("models.json") as f:
    models = json.load(f)

# Load model and tokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"


# To run this with a specific model, e.g. deepseek-llam-13b-chat, run:
# python app.py deepseek-llam-13b-chat
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with open("temp/model_name.tmp") as f:
            selected_model = models[f.read().strip()]
    except:
        model_name = models.keys()[0]
        print(f"Invalid model name, using default {model_name}")
        selected_model = models[model_name]

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
    output = model.generate(**inputs, max_length=1000, pad_token_id=model.config.eos_token_id)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    final_response = response.replace("\n", "<br>")

    print(final_response)
    # Remove the prompt from the beginning of the response if it is there
    if final_response.startswith(prompt):
        final_response = final_response[len(prompt):].strip()
        # Remove any punctuation symbol after it
        while final_response and final_response[0] in string.punctuation:
            final_response = final_response[1:].strip()

    
    return templates.TemplateResponse("response.html", {"request": request, "response": final_response})
