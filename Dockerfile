FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./main.py .
EXPOSE 80
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80","--reload"]
