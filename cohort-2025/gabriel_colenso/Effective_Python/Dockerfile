FROM python:3.12

WORKDIR /app 

RUN git https://github.com/gabecol7/COMP64803-Responsible-Reproducible-AI.git /app

WORKDIR /app/cohort-2025/gabriel_colenso/Effective_Python 

RUN python3 -m pip install -r requirements.txt

CMD ["/bin/bash"] 