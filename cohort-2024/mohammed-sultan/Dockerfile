FROM python:3.10

WORKDIR /app

RUN git clone https://github.com/mohummudh/comp64803.git /app

WORKDIR /app/cohort-2024/mohammed-sultan

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

CMD ["bash"]
