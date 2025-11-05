FROM python:3.13-slim AS base
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files (include src before sync)
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY app ./app

# Install dependencies
RUN uv sync --frozen --no-cache

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
