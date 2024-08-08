import os
import subprocess
import typer
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from pathlib import Path

app = typer.Typer()
console = Console()

ENV_VAR_NAME = "GIT_DEFAULT_USER"

def get_default_username() -> str:
    default_user = os.getenv(ENV_VAR_NAME)
    if not default_user:
        default_user = console.input(f"[bold yellow]Enter the default GitHub username:[/bold yellow] ")
        os.environ[ENV_VAR_NAME] = default_user
        with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
            bashrc.write(f'\nexport {ENV_VAR_NAME}="{default_user}"\n')
        console.print(f"[bold green]Default username set to: {default_user}[/bold green]")
    return default_user

def run_command(command: str):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        console.print(f"[bold red]Error:[/bold red] {result.stderr.strip()}")
        raise typer.Exit(1)
    return result.stdout.strip()

def format_repo_urls(repos: list[str], default_user: str) -> list[str]:
    formatted_repos = []
    for repo in repos:
        if '/' not in repo:
            repo = f"{default_user}/{repo}"
        if not repo.startswith("https://"):
            repo = f"https://github.com/{repo}.git"
        formatted_repos.append(repo)
    return formatted_repos

def create_remote_repo(new_repo_name: str, public: bool = True):
    visibility_flag = "--public" if public else "--private"
    run_command(f"gh repo create {new_repo_name} {visibility_flag} --clone")
    console.print(f"[bold green]Remote repository '{new_repo_name}' created on GitHub[/bold green]")

def merge_repos(repos: list[str], new_repo_name: str):
    new_repo_path = Path(new_repo_name)
    
    if not new_repo_path.exists():
        new_repo_path.mkdir(exist_ok=True)
    
    console.print(f"[bold green]Repository directory: {new_repo_name}[/bold green]")

    with console.status(f"[bold cyan]Initializing new Git repository...[/bold cyan]"):
        run_command(f"cd {new_repo_name} && git init")
        run_command(f"cd {new_repo_name} && git commit --allow-empty -m 'Initial dummy commit'")

    with Progress() as progress:
        task = progress.add_task("[cyan]Merging repositories...", total=len(repos))
        
        for repo_url in repos:
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            progress.console.print(f"[bold cyan]Merging {repo_name}...[/bold cyan]")

            run_command(f"cd {new_repo_name} && git remote add --fetch {repo_name} {repo_url}")
            run_command(f"cd {new_repo_name} && git merge {repo_name}/master --allow-unrelated-histories")

            repo_dir = new_repo_path / repo_name
            repo_dir.mkdir(exist_ok=True)

            run_command(f"cd {new_repo_name} && git mv $(ls -A | grep -v {repo_name}) {repo_name}/")
            run_command(f"cd {new_repo_name} && git commit -m 'Move {repo_name} files into subdir'")
            
            progress.advance(task)
    
    console.print(f"[bold green]Repositories merged successfully into {new_repo_name}[/bold green]")

@app.command()
def main(
    repos: list[str] = typer.Argument(..., help="List of Git repositories to merge"),
    new_repo_name: str = typer.Argument(..., help="Name of the new repository"),
    public: bool = typer.Option(True, "--public/--private", help="Set the visibility of the new repository")
):
    """
    Merges multiple Git repositories into a new one and creates a remote repository on GitHub.
    """
    default_user = get_default_username()
    repos = format_repo_urls(repos, default_user)
    
    table = Table(title="Repositories to Merge")
    table.add_column("Repo URL", justify="left", style="cyan")
    for repo in repos:
        table.add_row(repo)
    
    console.print(table)

    create_remote_repo(new_repo_name, public)
    merge_repos(repos, new_repo_name)

if __name__ == "__main__":
    app()
