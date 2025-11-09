# 5 ways to write better Python code - executable ML pipeline demo
This project shows the following five Pythonic practices while building a tiny ML pipeline to predict whether a breast tumor is malignant or benign using the Breast Cancer dataset from scikit-learn:
1) Helper functions, 2) Multiple assignment, 3) Raise exceptions,
4) Comprehensions, 5) Reproducible envs (uv).

## Build & run demo
cd cohort-2025/rachel_gaffney/effective-python-demo/
docker build -t effective-python-demo .
docker run --rm effective-python-demo all

# or a specific step:
docker run --rm effective-python-demo helper
docker run --rm effective-python-demo unpack
docker run --rm effective-python-demo exception
docker run --rm effective-python-demo comprehension
docker run --rm effective-python-demo model
