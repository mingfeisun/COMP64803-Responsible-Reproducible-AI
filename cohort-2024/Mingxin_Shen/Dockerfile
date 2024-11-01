FROM python:3.10-slim

WORKDIR /app

RUN git clone https://github.com/mingfeisun/COMP64803-Responsible-Reproducible-AI.git

WORKDIR /app/COMP64803-Responsible-Reproducible-AI/cohort-2024/Mingxin_Shen

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

CMD ["bash"]