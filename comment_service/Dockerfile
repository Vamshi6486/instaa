# Dockerfile for comment_service
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
# Assuming you have a Python-based Docker image



COPY . .

# Command to run the application
CMD ["python", "app.py"]
