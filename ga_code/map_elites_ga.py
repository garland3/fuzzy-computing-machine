import random
import time
import os
import torch
import requests
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# # initialize the tokenizer and language model once and save it to be reused later
# if not os.path.exists("model.pt"):
#     tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#     model = GPT2LMHeadModel.from_pretrained("gpt2")
#     torch.save(model, "model.pt")
#     print("Language model loaded and saved")
# else:
#     model = torch.load("model.pt")
#     tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#     print("Language model loaded from disk")

# def generate_code(code, model, tokenizer):
#     # generate new code based on the existing code
#     input_ids = tokenizer.encode(code, return_tensors="pt")
#     generated_sequence = model.generate(input_ids, max_length=1024, top_k=5, top_p=0.9, early_stopping=True)
#     generated_text = tokenizer.decode(generated_sequence[0], skip_special_tokens=True)
#     return generated_text

def generate_code(code):
    # make a call to the API to generate new code based on the existing code
    response = requests.post("http://localhost:5000/generate", json={"code": code})
    if response.status_code == 200:
        return response.json()["generated_code"]
    list_or_python_keywords = ["def", "if", "else", "elif", "for", "while", "try", "except", "finally", "with", "class", "return", "yield", "import", "from", "as", "global", "nonlocal", "assert", "break", "continue", "pass", "lambda", "del", "in", "not", "is", "and", "or", "True", "False", "None", "async", "await", "as"]
    
    list_of_obj_names = ["app", "model", "tokenizer", "response", "requests", "random", "time", "os", "torch", "GPT2Tokenizer", "GPT2LMHeadModel"]
    # add some random code to the end of the code
    new_code = code +  random.choice(list_or_python_keywords) + random.choice(list_of_obj_names)
    return new_code

def evaluate(code):
    # run the code and evaluate its score
    try:
        exec(code)
        response = requests.get("http://localhost:5000/finished")
        score = 0
        if response.status_code == 200:
            score = 1
            if "localhost" in response.url:
                score += 1
            if "/finished" in response.url:
                score += 1
            # if the response has a number in it, add 1 to the score
            if any(char.isdigit() for char in response.text):
                # add  the number to the score
                score += int(response.text)
        return score, response.status_code, response.elapsed.total_seconds()
    except:
        return 0, None, None

def evolve(code):
    # make changes to the code using the language model
    mutated_code = generate_code(code)
    return mutated_code

def map_elites(population):
    # map the solutions to the cells in the map based on their features
    map = {}
    for code in population:
        score, status_code, elapsed = evaluate(code)
        if (status_code, elapsed) not in map:
            map[(status_code, elapsed)] = []
        map[(status_code, elapsed)].append((code, score))
    return map

def save_code(code, generation):
    # save the code for each generation
    with open("generation_{}.py".format(generation), "w") as f:
        f.write(code)

if __name__ == "__main__":
    # start evolving
    original_code = open(__file__).read()
    population = [original_code]
    generation = 0
    while True:
        print("Generation: {}".format(generation))
        map = map_elites(population)
        population = []
        for (status_code, elapsed), solutions in map.items():
            sorted_solutions = [x for _, x in sorted(solutions, key=lambda pair: pair[1], reverse=True)]
            population += sorted_solutions[:10]
        for mutated_code in population:
            # evaluate the new code
            score, status_code, elapsed = evaluate(mutated_code)

            # save the new code if it's better, or every 10 generations
            if score > 0 or generation % 10 == 0:
                population.append(mutated_code)
                directory = "./gen_{}_{}_{}".format(status_code, elapsed, score)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open("{}/code.py".format(directory), "w") as f:
                    f.write(str(mutated_code))
            # wait for a random amount of time before evolving the next code
            time.sleep(random.randint(1, 5))
        generation += 1

# to kill everything if it's stuck
# ps aux | grep python
# OR
# sudo kill -9 $(pgrep python)
