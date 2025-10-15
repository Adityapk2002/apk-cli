#!/usr/bin/env python3
import os
import yaml
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich import box


console = Console()
session = PromptSession(history=FileHistory('.my_cli_history'))


def load_config():
    try:
        with open("config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        api_key = input("Enter the Groq API key: ").strip()
        config = {"GROQ_API_KEY": api_key}
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)
        return config

config = load_config()
os.environ["GROQ_API_KEY"] = config["GROQ_API_KEY"]
from plugins.scaffold import create_project

from openai import OpenAI
client = OpenAI(api_key=config["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")

def get_active_models() -> list[str]:
    """Fetch currently active Groq models for fallback."""
    try:
        data = client.models.list()
       
        text_models = [m.id for m in data.data if any(x in m.id.lower() for x in ["llama", "qwen", "mixtral", "gemma"])]
        return text_models if text_models else [m.id for m in data.data]
    except Exception as e:
        console.print(f"[red]Failed to fetch models:[/] {e}")
        return []

def groq_generate(prompt: str, max_tokens: int = 1024) -> str:
    """Generate response using Groq AI with fallback models."""
    
    active_models = get_active_models()
    
    
    fallback_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    
    model_list = active_models if active_models else fallback_models
    
    for model in model_list:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            console.print(f"[dim yellow]Model {model} failed, trying next...[/]")
            continue
    
    return "Error: Unable to generate response with available models."

def groq_chat(prompt: str) -> str:
    """Generate response using Groq AI with fallback models."""
    return groq_generate(prompt, max_tokens=1024)

def explain_command(cmd: str) -> str:
    prompt = f"Explain this shell command in one line:\n{cmd}"
    return groq_chat(prompt)

def get_current_dir() -> str:
    """Shorten home directory paths for display."""
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    return cwd.replace(home, "~")

class HybridCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith("?"):
            yield Completion(
                "ask",
                start_position=-len(text),
                display="?Ask APK Bot anything"
            )
        elif text.startswith("cmd:"):
            partial = text[4:]
            for cmd in ["explain", "git", "find", "help"]:
                if cmd.startswith(partial):
                    yield Completion(
                        cmd[len(partial):],
                        start_position=len(partial),
                        display=f"cmd:{cmd} - AI helper"
                    )
        else:
            yield from PathCompleter().get_completions(document, complete_event)


def execute_command(cmd: str):
    try:
        if cmd.startswith("?"):
            response = groq_chat(cmd[1:])
            console.print(Panel.fit(response, title="APK Bot", border_style="blue", width=80))

        elif cmd.startswith("!explain"):
            explanation = explain_command(cmd[9:].strip())
            console.print(Panel.fit(explanation, title="Explanation", border_style="yellow", width=80))

        elif cmd.startswith("!git"):
            try:
                from plugins.git_helper import handle_git
                suggestion = handle_git(cmd[4:].strip().split())
                console.print(Panel.fit(suggestion, title="Git Suggestion", border_style="green", width=80))
            except ImportError:
                console.print("[red]Plugin 'git_helper' not found[/]")

        elif cmd.startswith("!find"):
            try:
                from plugins.file_search import handle_find
                search_cmd = handle_find(cmd[6:].strip())
                console.print(Panel.fit(search_cmd, title="File Search", border_style="cyan", width=80))
            except ImportError:
                console.print("[red]Plugin 'file_search' not found[/]")

        elif cmd.startswith("cd"):
            try:
                path = os.path.expanduser(cmd[3:].strip() or "~")
                os.chdir(path)
                console.print(f"[green]Changed to {get_current_dir()}[/]")
            except Exception as e:
                console.print(f"[red]Error:[/] {e}")
        
        elif cmd.startswith("!create"):
            try:
                create_project()
            except Exception as e:
                console.print(f"[red]Error running project generator:[/] {e}")


        elif cmd == "!help":
            console.print(Panel.fit(
                Text.from_markup(
                    """
[b]COMMAND HELP[/b]
[cyan]?[query][/]         - Ask APK Bot anything
[yellow]!explain [cmd][/] - Explain shell commands
[green]!git [action][/]     - Smart Git helper
[magenta]!find [query][/]    - Natural language file search
[blue]!models[/]           - List available AI models
[bold white]!create[/]         - Launch project generator (React, Node, Flask, etc.)
[dim]exit/quit[/]         - Exit shell
                    """),
                title="Help",
                border_style="blue",
                width=80
            ))

        elif cmd == "!models":
            models = get_active_models()
            if models:
                model_list = "\n".join([f"• {m}" for m in models])
                console.print(Panel.fit(model_list, title="Available Models", border_style="cyan", width=80))
            else:
                console.print("[red]No models available[/]")

        else:
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(f"[red]{result.stderr}[/]")

            if result.returncode != 0:
                fix = groq_chat(f"Fix this shell error concisely:\nCommand: {cmd}\nError: {result.stderr}\nProvide ONLY the corrected command")
                console.print(Panel.fit(fix.strip(), title="Try This", border_style="red", width=80))

    except Exception as e:
        console.print(Panel.fit(f"Error: {str(e)}\nType [b]!help[/] for assistance", border_style="red", width=80))



def run_cli():
    console.print(Panel.fit(
        Text.from_markup("[bold green]🤖 APK Smart CLI[/] [dim](type !help for commands)"),
        title="APK CLI",
        border_style="magenta",
        subtitle=f"{get_current_dir()}",
        subtitle_align="right"
    ))

    while True:
        try:
            user_input = session.prompt(
                f"APK CLI {get_current_dir()}> ",
                completer=HybridCompleter(),
                auto_suggest=AutoSuggestFromHistory()
            ).strip()

            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                console.print("[green]Goodbye! 👋[/]")
                break

            execute_command(user_input)

        except KeyboardInterrupt:
            console.print(Panel.fit(Text.from_markup("\n[yellow]Use 'exit' to quit[/]")))
        except EOFError:
            console.print("\n[green]Goodbye! 👋[/]")
            break



def render_markdown(content: str, width: int = 80) -> Panel:
    return Panel(
        Markdown(content.strip()),
        border_style="blue",
        box=box.ROUNDED,
        width=min(width, os.get_terminal_size().columns - 4),
        padding=(1, 2)
    )


if __name__ == "__main__":
    run_cli()


#!/usr/bin/env python3 → shebang line to tell the OS to use Python 3.