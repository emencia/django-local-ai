# Django local AI

Run a local AI from Django with [Llama.cpp](https://github.com/ggerganov/llama.cpp)

## Install

Clone the repository and install the dependencies:

```bash
git clone https://github.com/emencia/django-local-ai
cd django-local-ai
make install
```

In case of an error *Failed to build llama-cpp-python* try this and run again:

```bash
source .venv/bin/activate
export SETUPTOOLS_USE_DISTUTILS=stdlib
pip install --upgrade --force-reinstall setuptools
```

## Get a language model

To make this work you need a Llama.cpp gguf quantitized language model. We
will use Mistral 7B Instruct from [this repository](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF):

```bash
cd some/dir/where/to/put/your/models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

## Settings

Change the `LLM_MODELS_DIR` setting in `main/settings.py` to your model directory path.

Change the `LLM_DEFAULT_MODEL` setting in `main/settings.py` if you
want to use another model. Use an absolute path.

## Run

Run the http server:

```bash
make run
```

Create a superuser:

```bash
make superuser
```

Open the frontend at `localhost:8000` and the admin at `localhost:8000/admin/`
