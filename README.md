# Medtrack

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: djLint](https://img.shields.io/badge/html%20style-djLint-blue.svg)](https://github.com/djlint/djlint)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit)
<!-- [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) -->
<!-- [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier) -->

[**Blog post**](https://hoochlef.github.io/blog/medtrack-part-one/) | [**Screenshots**](https://github.com/hoochlef/medtrack/tree/main/screenshots)

Upload a picture of a medication and get the essential information.

> [!CAUTION]
> **Medical Disclaimer:** This project is for **educational and technical demonstration purposes only**. The information provided by the AI should not be used for medical diagnosis, treatment, or as a substitute for professional medical advice. Always consult a healthcare professional for medication concerns.

> [!NOTE]
> This repository was built as a personal exploration to experiment with new technologies and does not represent a production-ready medical tool.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)

- Python 3.12+
- Refer to [Ollama download page](https://ollama.com/download/) to download Ollama according to your operating system
- [Setup](#ollama-model-setup) your local model

## Ollama Model Setup

1. **Pull a Small model from ollama**

```bash

ollama pull llama3.2:3b
```

2.**Setup a [Modelfile](https://docs.ollama.com/modelfile) with a customized prompt**

See [Modelfile](https://github.com/hoochlef/medtrack/tree/main/Modelfile) used in this project.

## Getting Started

1.**Clone the repository**

```bash
git clone https://github.com/hoochlef/medtrack
cd medtrack

```

2.**Sync dependencies**

This command creates a virtual environment and installs all dependencies automatically.

```bash
uv sync

```

For the folks that don't use uv, there's a ```requirements.txt``` file at the root of the project.

3.**Environment Setup**

Copy the example environment file and update your variables.

```bash
cp .env.example .env

```

4.**Start Development Server**

```bash
uv run python manage.py runserver

```

## Tech Stack

- **Framework:** Django 5.2.8
- **Smart tools (ML tools):** paddleocr, ollama
- **Dev tools:** uv, ruff
- **Other:** check [dependencies](https://github.com/hoochlef/medtrack/tree/main/requirements.txt)

## License

This repository is licensed under the [MIT License](https://github.com/hoochlef/medtrack/tree/main/LICENSE)
