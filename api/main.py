from fastapi import FastAPI
import torch

from transformers import GPT2Tokenizer, GPT2LMHeadModel


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

app = FastAPI()

@app.post("/finished")
async def finished(result: float):
    return {"message": f"Result received: {result}"}


@app.post("/generate")
async def generate(code: str):
    # generate new code based on the existing code
    input_ids = tokenizer.encode(code, return_tensors="pt")
    generated_sequence = model.generate(input_ids, max_length=1024, top_k=5, top_p=0.9, early_stopping=True)
    generated_text = tokenizer.decode(generated_sequence[0], skip_special_tokens=True)
    return {"generated_code": generated_text}

# uvicorn main:app --host localhost --port 5000 --reload
# TEST the finish function with 
# curl -X POST "http://localhost:5000/finished" -H "accept: application/json" -H "Content-Type: application/json" -d "1.0"