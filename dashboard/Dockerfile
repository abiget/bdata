FROM python:3.10-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install additional Python packages
RUN apt-get update && apt-get install -y libpq-dev
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy application code
COPY ./app .

# Expose the port the app runs on
EXPOSE 8501

ENV POSTGRES_HOST="postgres-db"

# Default command
CMD ["streamlit", "run", "app.py"]
