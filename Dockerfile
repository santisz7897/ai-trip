FROM python:3.10-slim

WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy requirements file
COPY requirements.lock .

# Install dependencies with uv
RUN uv pip install -r requirements.lock

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 