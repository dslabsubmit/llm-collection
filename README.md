# LLM Collection

A small evaluation harness that runs multiple code LLMs to convert vulnerability PoCs into Metasploit Ruby modules and saves the generated outputs for later review.

## Requirements

- Python 3
- GPU + CUDA recommended for large models
- Python deps: see `requirements.txt`

Install:

```bash
pip install -r requirements.txt
```

## Supported models

CLI names (pass as the first argument to `main.py`):

- `codet5p`
- `starcoder`
- `secgpt`
- `codellama`
- `codellama_70b`
- `mixtral`
- `deepseekcoder_v2`

Example:

```bash
CUDA_VISIBLE_DEVICES=0,1 python3 main.py starcoder
```

## How it works

- Datasets live under `dataset/<Language>/<CVE>/<exp>/...`
- `eval_llm.py` currently uses `exp = 3` only and runs 3 repeats per CVE
- Outputs are written to:
  - `result/<mode>/<model_type>_<repeat>/<Language>/<CVE>.txt`
- Logs are written to `log/`

Prompting behavior is controlled in `config.py`:

- `mode = "weak"` uses a generic prompt
- `mode = "strong"` loads per-language prompts from `prompt/user-prompt-*.txt`

## Validation with verify.py (external)

The verification script lives outside this repo:

- `/home/verify.py`

It can validate generated Ruby modules against local/remote Vulhub environments. It depends on Docker and Netmiko, and reads configuration from:

- `/home/config.ini`

Common usage patterns:

1) Validate a single record from a JSONL file (each line should include `name`, `content`, `model`, `ip`, `port`):

```bash
python3 /home/verify.py \
  --single --jsonl /path/to/data.jsonl --line 1 --mode 1
```

2) Validate a single Ruby file directly:

```bash
python3 /home/verify.py \
  --single --name http_example_cve_2020_0000 \
  --content-file /path/to/module.rb \
  --model 0 --ip 127.0.0.1 --port 8080 --mode 1
```

3) Batch mode:

```bash
python3 /home/verify.py
```

Notes:
- Batch mode uses hard-coded `model_names` inside `verify.py`. Edit that list to point at your JSONL files.
- Ensure `config.ini` paths and Docker/Vulhub settings match your environment.
