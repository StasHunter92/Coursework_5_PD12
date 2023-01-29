FROM python:3.10-slim
WORKDIR /skywars

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY application application/
COPY static static/
COPY templates templates/
COPY app.py .
COPY wsgi.py .

CMD flask run -h 0.0.0.0 -p 5050