#!/usr/bin/env python3
import sys
import subprocess
import json
from pathlib import Path
import ollama
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

CONFIG_PATH = Path.home() / ".config" / "gcmd" / "config.json"
DEFAULT_MODEL = "llama3.2:3b"

console = Console()


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps({"model": DEFAULT_MODEL}, indent=2))
        console.print(f"[dim]Created config at {CONFIG_PATH}[/dim]")
    with open(CONFIG_PATH) as f:
        return json.load(f)


config = load_config()
MODEL = config.get("model", DEFAULT_MODEL)

PROMPT_TEMPLATE = (
    "Write a single bash command or function for the following task. "
    "Respond using exactly this format and nothing else:\n"
    "COMMAND: <the bash command>\n"
    "DESCRIPTION: <one sentence explanation>\n\n"
    "Task: {task}"
)


def query_model(task: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "user", "content": PROMPT_TEMPLATE.format(task=task)}],
    )
    return response["message"]["content"]


def parse_response(text: str) -> tuple[str, str]:
    command, description = "", ""
    for line in text.splitlines():
        if line.startswith("COMMAND:"):
            command = line[len("COMMAND:"):].strip()
        elif line.startswith("DESCRIPTION:"):
            description = line[len("DESCRIPTION:"):].strip()
    return command, description


def display_result(command: str, description: str):
    content = Text()
    content.append("Command     ", style="bold cyan")
    content.append(f"{command}\n", style="bold white")
    content.append("Description ", style="bold cyan")
    content.append(description, style="dim white")
    console.print(
        Panel(content, title="[bold green]gcmd[/bold green]", border_style="green"))


def run_command(cmd: str):
    console.print(f"\n[dim]Running:[/dim] [bold]{cmd}[/bold]\n")
    subprocess.run(["zsh", "-c", cmd])


def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage:[/red] gcmd <describe what you want to do>")
        sys.exit(1)

    task = " ".join(sys.argv[1:])

    while True:
        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            raw = query_model(task)

        command, description = parse_response(raw)

        if not command:
            console.print("[red]Could not parse model response:[/red]")
            console.print(raw)
            sys.exit(1)

        console.print()
        display_result(command, description)

        action = questionary.select(
            "What would you like to do?",
            choices=["Run", "Refine", "Cancel"],
        ).ask()

        if action is None or action == "Cancel":
            console.print("[dim]Cancelled.[/dim]")
            break

        if action == "Run":
            run_command(command)
            break

        if action == "Refine":
            extra = questionary.text("Additional context:").ask()
            if extra:
                task = f"{task}. {extra}"


if __name__ == "__main__":
    main()
