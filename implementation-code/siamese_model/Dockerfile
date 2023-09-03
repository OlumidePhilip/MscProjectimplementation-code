FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV PORT=80

CMD ["python3", "main.py"]