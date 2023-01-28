FROM python:3.10-slim
WORKDIR /skywars

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY application application/
COPY templates templates/
COPY app.py .

CMD flask run -h 0.0.0.0 -p 80