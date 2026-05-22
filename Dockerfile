FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

# Create logs folder
RUN mkdir -p logs

EXPOSE 8000

CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]