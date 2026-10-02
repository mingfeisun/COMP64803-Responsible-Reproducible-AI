# 5 ways to write better Python code
build using the following:

docker build -t python-tips:latest .

## Run tip 1: 92. Profile before optimisation
docker run --rm python-tips

## Run tip 2: 43. Consider generators instead of returning lists
docker run --rm python-tips python tip2_43.py

## Run tip 3: 117. Use Virtual Environments for Isolated and Reproducible Dependencies
docker run --rm python-tips bash tip3_117.sh

## Run tip 4: 23. Pass Iterators to 'any' & 'all' for Efficient Short-Circuiting Logic
docker run --rm python-tips python tip4_23.py

## Run tip 5: 32. Prefer Raising Exceptions to Returning None
docker run --rm python-tips python tip5_32.py