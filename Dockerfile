FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime packages plus build tools for packages without prebuilt wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq5 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 5010

CMD ["flask", "--app", "MyFinance.finance", "run", "--host=0.0.0.0", "--port=5010"]
