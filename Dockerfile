FROM python:3.10-slim

WORKDIR /app

COPY run.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "run:app"]
