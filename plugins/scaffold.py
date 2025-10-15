import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()

def ask_choice(title, choices):
    console.print(Panel(Text(title, justify="center", style="bold cyan")))
    for i, choice in enumerate(choices, start=1):
        console.print(f"[yellow]{i}[/]. {choice}")
    while True:
        try:
            selected = int(input("Enter your choice: "))
            if 1 <= selected <= len(choices):
                return choices[selected - 1]
        except ValueError:
            pass
        console.print("[red]Invalid input. Please enter a valid number.[/red]")

def create_project():
    console.print(Panel("[bold cyan]🚀 Welcome to the AI Project Generator![/bold cyan]\n"))

    # Ask for inputs
    tech_stack = ask_choice("Choose your tech stack:", ["React (Vite)", "Node.js (Express)", "Next.js", "Flask (Python)", "FastAPI (Python)"])
    project_name = Prompt.ask("Project name", default="my-app")
    language = ask_choice("Choose language:", ["TypeScript", "JavaScript"])
    init_git = Prompt.ask("Initialize git repository? (yes/no)", default="yes").lower().startswith("y")

    project_dir = Path.cwd() / project_name
    console.print("\n🔨 [yellow]Creating your project...[/yellow]")
    project_dir.mkdir(exist_ok=True)
    os.chdir(project_dir)

    # Scaffold based on selection
    if "React" in tech_stack:
        subprocess.run(["npm", "create", "vite@latest", ".", "--", "--template", f"react-{language.lower()}"])
    elif "Node.js" in tech_stack:
        subprocess.run(["npm", "init", "-y"])
        with open("server.js", "w") as f:
            f.write("const express = require('express');\nconst app = express();\napp.listen(3000, () => console.log('Server running'));")
        subprocess.run(["npm", "install", "express"])
    elif "Flask" in tech_stack:
        subprocess.run(["python3", "-m", "venv", "venv"])
        with open("app.py", "w") as f:
            f.write("from flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello Flask!'\n\nif __name__ == '__main__':\n    app.run(debug=True)")
    elif "FastAPI" in tech_stack:
        subprocess.run(["pip", "install", "fastapi", "uvicorn"])
        with open("main.py", "w") as f:
            f.write("from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'message': 'Hello FastAPI!'}")

    if init_git:
        subprocess.run(["git", "init"])

    console.print("\n📦 [green]Installed dependencies[/green]")
    console.print(f"✓ Project created successfully!\n\n📁 Project: {project_name}")
    console.print(f"📍 Location: {project_dir}\n")

    console.print("🚀 [bold]Next steps:[/bold]\n")
    console.print(f"   cd {project_name}")
    if "React" in tech_stack:
        console.print("   npm run dev")
    elif "Node.js" in tech_stack:
        console.print("   node server.js")
    elif "Flask" in tech_stack:
        console.print("   source venv/bin/activate && python app.py")
    elif "FastAPI" in tech_stack:
        console.print("   uvicorn main:app --reload")

    console.print("\n✨ [bold magenta]Happy coding![/bold magenta] ✨")
