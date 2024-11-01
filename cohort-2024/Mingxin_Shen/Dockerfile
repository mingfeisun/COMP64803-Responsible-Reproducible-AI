FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/XTM233/COMP64803-Responsible-Reproducible-AI.git

WORKDIR /app/COMP64803-Responsible-Reproducible-AI/cohort-2024/Mingxin_Shen

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

CMD ["bash"]