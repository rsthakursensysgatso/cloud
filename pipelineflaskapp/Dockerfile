FROM python:3.6
COPY ./pipelineflaskapp/microblog/ /app
WORKDIR /app/microblog/
COPY ./pipelineflaskapp/requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

