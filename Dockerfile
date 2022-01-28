FROM python:3.8.5-alpine
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install make automake gcc g++ subversion python3-dev
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]

EXPOSE 80