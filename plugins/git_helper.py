from typing import List
from plugins.groq_utils import groq_generate as get_groq_client  # absolute import

def handle_git(args: List[str]) -> str:
    """Generate precise Git commands using Groq AI."""
    if not args:
        return "git status"

    simple_commands = {
        "status": "git status",
        "log": "git log --oneline -n 10",
        "branch": "git branch -vv",
        "stash": "git stash list",
        "diff": "git diff --cached",
    }

    if args[0] in simple_commands:
        return simple_commands[args[0]]

    prompt = f"""
Convert this natural language Git request to a SINGLE executable Git command.
Return ONLY the command without any explanations or formatting.

Request: git {' '.join(args)}

Command: git """

    try:
        full_command = get_groq_client(prompt)
        if full_command.startswith("git "):
            return full_command
        return f"git {full_command}"
    except Exception:
        return f"git {' '.join(args)}"
