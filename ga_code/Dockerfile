FROM registry.access.redhat.com/ubi8/python-39

WORKDIR /app


RUN pip install torch transformers requests

RUN python -c "import transformers;from transformers import GPT2Tokenizer,  GPT2LMHeadModel;tokenizer = GPT2Tokenizer.from_pretrained('gpt2');model = GPT2LMHeadModel.from_pretrained('gpt2')"

COPY . .


CMD ["python", "map_elites_ga.py"]

# to just run the code:
# python map_elites_ga.py


 # sudo docker build --pull --rm -f "ga_code/Dockerfile" -t evolutioncode:latest ga_code/.