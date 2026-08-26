FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install python dependencies
COPY requirements.txt .
# Add the extra requirements we installed along the way
RUN pip install -r requirements.txt email-validator langchain-google-genai psycopg2-binary

COPY . .

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
