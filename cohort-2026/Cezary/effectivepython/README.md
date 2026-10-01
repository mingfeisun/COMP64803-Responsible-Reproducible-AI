## Build the image

```
docker build -t python-examples .
```

## Start the container

```
docker run -it --rm python-examples
```

## Run the files

List the files and run any of them with Python:

```
ls
python <file_name>.py
```

To run the static type checker on a file, for example the typing (i90.py) example:

```
mypy <file_name>.py
```
