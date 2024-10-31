# Python Multiprocessing GPU Manager

This repository contains a Python script designed to manage GPU resources for running multiple tasks concurrently, allowing for dry runs and configurations. The code dynamically allocates GPUs based on user-defined arguments and runs commands with the specified configurations.

### Features

- GPU management for concurrent tasks
- Dynamic task assignment to GPUs
- Dry-run option for command preview
- Custom argument parsing and generation of argument combinations

### Prerequisites

- Python 3.6+
- `torch` for CUDA device check (for `test.py` only)
- `Docker`

#### Usage

Run the Python file with arguments:

```bash
python main.py --available-gpus 0 1 --ntasks-per-gpu 2 --filename script.py --dry
```

| Argument            | Type         | Description                                 |
|---------------------|--------------|---------------------------------------------|
| `--available-gpus`  | List of int  | Specify GPUs for task allocation            |
| `--ntasks-per-gpu`  | int          | Number of tasks per GPU                     |
| `--filename`        | str          | Script file to execute                      |
| `--dry`             | Flag         | Preview command without execution           |

For custom arguments, add them after recognized arguments using `--arg-name value`.

#### Running in Docker

To build and run in a Docker container:

1. Build the Docker image:
   ```bash
   docker build -t gpu-manager .
   ```

2. Run the Docker container:
   ```bash
   docker run --gpus all gpu-manager python main.py --available-gpus 0 1 --ntasks-per-gpu 2 --filename script.py --dry
   ```
