# first-agent

A small command-line AI coding agent built on Google's Gemini API. Give it a
prompt and it works through a tool-calling loop to inspect and modify files in a
sandboxed working directory.

## What it can do

The agent has access to four tools, all scoped to a fixed working directory:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files (with optional arguments)

## Setup

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your-key-here
```

## Usage

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to print token usage and the result of each function call:

```bash
uv run main.py "fix the bug in calculator.py" --verbose
```

The agent loops up to 20 times, calling tools as needed, then prints its final
response.
