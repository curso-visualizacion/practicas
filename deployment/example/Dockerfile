from python:3.9-slim

RUN pip install flask
COPY ./app.py /app/app.py
WORKDIR /app
EXPOSE 5000
CMD ["flask", "run"]
