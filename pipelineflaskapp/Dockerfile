FROM python:3.6
COPY ./pipelineflaskapp/microblog/ /app
WORKDIR /app/microblog/
COPY ./pipelineflaskapp/requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD pipelinenginx/index.nginx-debian.html /var/www/html
ADD https://get.aquasec.com/microscanner .
RUN chmod +x microscanner
RUN ./microscanner OGY0NGQ3MTI3NmQ4
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

