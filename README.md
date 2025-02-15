# Solar Prediction following MLOps

The goal is to develop an entire MLOps pipeline, with feature extraction, model training, automation, deployment, etc. We will predict the hours of sunlight within the next couple days for a given location.

## Features

## Clone Repo

```bash
git git@github.com:mvoss02/solar_prediction.git
cd solar_prediction
```

## Requirements

- Python 3.12+
- Docker
- Make
- uv -> An extremely fast Python package and project manager, written in Rust.
- ruff -> An extremely fast Python linter and code formatter, written in Rust.
- pre-commit
- Hopsworks -> Feature Store

## Requirements Installation

1. uv

- Linus/MacOS

```bash
# Install uv globally
wget -qO- https://astral.sh/uv/install.sh | sh
```

- Windows

```bash
# Install uv globally
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. ruff

```bash
# Install Ruff globally
uv tool install ruff@latest
```

3. pre-commit
   Installieren:

```bash
uv tool install pre-commit

pre-commit --version #Has the tool been installed correctly?
```

- `uv tool` installs tools gloablly

Tool has to be installed and file ".pre-commit-config.yaml" has to be present for next step:

```bash
pre-commit install
```

## Usage

1. New service

```bash
cd services
uv init NAME_OF_SERVICE
```

2. Packages
   2.1. Creation of package

```bash
uv init --lib MY_PACKAGE_NAME
```

- Project structure:

```
my_package/
|-- src/
    |-- my_package/
      |-- __init__.py
      |-- your_code.py  # Add your module(s) here
      |-- py.typed # empty, indicates to IDEs your code includes type annotations
|-- pyproject.toml
|-- README.md
|-- .python-version
```

2.2. Creating a package

```bash
uv build
uv pip install pip install dist/MY_PACKAGE_NAME-0.1.0-py3-none-any.whl
```

2.3. Creating package in development mode -> advantage: does not have to be installed again with each change

```bash
uv pip install -e .
```

- Additional information regarding uv packaging: [https://sarahglasmacher.com/how-to-build-python-package-uv/]
