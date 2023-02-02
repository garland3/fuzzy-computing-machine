FROM registry.access.redhat.com/ubi8/python-39

WORKDIR /app

RUN pip install fastapi uvicorn

COPY . .

# WORKDIR /app/api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

# to just run the uvicorn server:
# uvicorn main:app --host 0.0.0.0 --port 5000 --reload

# sudo docker build  -f "api/Dockerfile" -t evolutionhost:latest api/.

# test it with:
# sudo docker run -p 5000:5000 evolutionhost:latest
