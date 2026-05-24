# gcmd

Generate and run bash commands from natural language descriptions using a local LLM via Ollama.

## What it does

Describe what you want to do in plain English, and gcmd will generate the appropriate bash command, show you what it does, and let you run it or refine it.

Example:
```
gcmd find all pdf files larger than 10MB in my home directory
```

## Installation

1. Install dependencies:
```bash
pip install ollama questionary rich
```

2. Install [Ollama](https://ollama.com) and pull your preferred model (default: `llama3.2:3b`)
```bash
ollama pull llama3.2:3b
```

3. Make it executable and optionally add to your PATH:
```bash
chmod +x gcmd.py
# Then symlink or add to your PATH
```

## Configuration

On first run, a config file is created at `~/.config/gcmd/config.json`:

```json
{
  "model": "llama3.2:3b"
}
```

Edit this file to use a different Ollama model.

## Usage

```bash
gcmd <describe your task>
```

After the command is generated, you can:
- **Run** - execute the command
- **Refine** - add more context to get a better command
- **Cancel** - exit without running
