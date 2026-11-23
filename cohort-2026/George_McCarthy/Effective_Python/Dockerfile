FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /usr/local/bin/uv
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt
COPY talk.py .
EXPOSE 2718
CMD ["marimo", "edit", "talk.py", "--host", "0.0.0.0", "--port", "2718", "--headless", "--no-token"]
