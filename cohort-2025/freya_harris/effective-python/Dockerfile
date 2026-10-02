# minimal python docker image
FROM python:3.12-slim

# create a working directory
WORKDIR /app

# copy all files to working directory
COPY . /app 

# install required packages
RUN pip install numpy

# run the demo file when the container starts
CMD ["python", "demo_main.py"] 
