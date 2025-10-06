#!bin/bash/

make html 
python -m http.server --directory ./build/html/