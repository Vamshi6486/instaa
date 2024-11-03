# Dockerfile for post_service
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create uploads directory
RUN [ -d uploads ] || mkdir uploads

# Command to run the application
CMD ["python", "app.py"]
