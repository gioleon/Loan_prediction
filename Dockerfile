FROM python:3.9

RUN pip install -U pip

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p app

COPY ./app app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.", "--port", "8080"]