FROM python:3.11-slim

WORKDIR /app
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt

COPY . .
CMD ["pytest", "--cov=laya", "--cov-report=term-missing", "--cov-fail-under=60", "tests/"]
