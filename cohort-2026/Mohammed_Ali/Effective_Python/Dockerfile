# Item 1: know which version of Python you're using, so pin it here.
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py run_all.sh ./
CMD ["bash", "run_all.sh"]
