FROM python:3.8-slim
WORKDIR /app
COPY templates/ /app/templates/
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
