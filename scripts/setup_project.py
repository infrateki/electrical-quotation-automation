#!/usr/bin/env python3
"""
Setup script for Electrical Quotation Automation System.
This script helps developers quickly set up their development environment.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


def run_command(command, check=True, capture_output=False):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running command: {command}[/red]")
        console.print(f"[red]{e.stderr}[/red]")
        return None


def check_python_version():
    """Check if the correct Python version is installed."""
    version = sys.version_info
    if version < (3, 11):
        console.print(
            f"[red]Python 3.11+ required, found {version.major}.{version.minor}[/red]"
        )
        return False
    console.print(f"[green]✓ Python {version.major}.{version.minor}.{version.micro}[/green]")
    return True


def check_docker():
    """Check if Docker is installed and running."""
    result = run_command("docker --version", check=False, capture_output=True)
    if result and result.returncode == 0:
        console.print(f"[green]✓ Docker: {result.stdout.strip()}[/green]")
        
        # Check if Docker daemon is running
        result = run_command("docker ps", check=False, capture_output=True)
        if result and result.returncode == 0:
            return True
        else:
            console.print("[yellow]⚠ Docker is installed but not running[/yellow]")
            return False
    else:
        console.print("[red]✗ Docker not found[/red]")
        return False


def check_git():
    """Check if Git is installed."""
    result = run_command("git --version", check=False, capture_output=True)
    if result and result.returncode == 0:
        console.print(f"[green]✓ Git: {result.stdout.strip()}[/green]")
        return True
    else:
        console.print("[red]✗ Git not found[/red]")
        return False


def create_virtual_environment():
    """Create a Python virtual environment."""
    venv_path = Path("venv")
    if venv_path.exists():
        console.print("[yellow]Virtual environment already exists[/yellow]")
        return True
    
    console.print("Creating virtual environment...")
    result = run_command(f"{sys.executable} -m venv venv")
    if result:
        console.print("[green]✓ Virtual environment created[/green]")
        return True
    return False


def activate_venv_command():
    """Get the command to activate virtual environment based on OS."""
    if platform.system() == "Windows":
        return ".\\venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"


def install_dependencies():
    """Install Python dependencies."""
    console.print("Installing Python dependencies...")
    
    # Determine pip command based on whether we're in venv
    if platform.system() == "Windows":
        pip_cmd = ".\\venv\\Scripts\\pip"
    else:
        pip_cmd = "./venv/bin/pip"
    
    # Upgrade pip first
    run_command(f"{pip_cmd} install --upgrade pip")
    
    # Install requirements
    result = run_command(f"{pip_cmd} install -r requirements.txt")
    if result:
        console.print("[green]✓ Dependencies installed[/green]")
        return True
    return False


def setup_environment_file():
    """Create .env file from example if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        console.print("[yellow].env file already exists[/yellow]")
        return True
    
    if not env_example.exists():
        console.print("[red].env.example not found[/red]")
        return False
    
    # Copy example to .env
    env_file.write_text(env_example.read_text())
    console.print("[green]✓ Created .env file from example[/green]")
    console.print("[yellow]⚠ Please update .env with your API keys![/yellow]")
    return True


def create_directories():
    """Create necessary project directories."""
    directories = [
        "logs",
        "uploads",
        "temp",
        "cache",
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
    
    console.print("[green]✓ Created project directories[/green]")
    return True


def start_docker_services():
    """Start Docker services."""
    console.print("Starting Docker services...")
    result = run_command("docker-compose up -d")
    if result:
        console.print("[green]✓ Docker services started[/green]")
        console.print("Waiting for services to be ready...")
        import time
        time.sleep(10)
        return True
    return False


def check_services_health():
    """Check if all services are healthy."""
    services = {
        "PostgreSQL": "docker exec quotation_postgres pg_isready -U quotation_user",
        "Redis": "docker exec quotation_redis redis-cli ping",
        "Neo4j": "docker exec quotation_neo4j cypher-shell -u neo4j -p neo4j_password 'RETURN 1'",
    }
    
    all_healthy = True
    for service, command in services.items():
        result = run_command(command, check=False, capture_output=True)
        if result and result.returncode == 0:
            console.print(f"[green]✓ {service} is healthy[/green]")
        else:
            console.print(f"[red]✗ {service} is not responding[/red]")
            all_healthy = False
    
    return all_healthy


def setup_pre_commit():
    """Install pre-commit hooks."""
    if platform.system() == "Windows":
        pre_commit_cmd = ".\\venv\\Scripts\\pre-commit"
    else:
        pre_commit_cmd = "./venv/bin/pre-commit"
    
    result = run_command(f"{pre_commit_cmd} install", check=False)
    if result and result.returncode == 0:
        console.print("[green]✓ Pre-commit hooks installed[/green]")
        return True
    else:
        console.print("[yellow]⚠ Could not install pre-commit hooks[/yellow]")
        return False


def print_next_steps():
    """Print next steps for the developer."""
    table = Table(title="🚀 Next Steps", show_header=False)
    table.add_column("Step", style="cyan", width=50)
    
    steps = [
        f"1. Activate virtual environment:\n   {activate_venv_command()}",
        "2. Update .env file with your API keys:\n   - OpenAI API key\n   - Other service keys",
        "3. Run database migrations:\n   alembic upgrade head",
        "4. Start the development server:\n   uvicorn api.main:app --reload",
        "5. Open API docs:\n   http://localhost:8000/docs",
        "6. Run tests:\n   pytest tests/",
    ]
    
    for step in steps:
        table.add_row(step)
    
    console.print(table)


@click.command()
@click.option('--skip-docker', is_flag=True, help='Skip Docker setup')
@click.option('--skip-deps', is_flag=True, help='Skip dependency installation')
def main(skip_docker, skip_deps):
    """Set up the Electrical Quotation Automation development environment."""
    console.print(Panel.fit(
        "⚡ Electrical Quotation Automation Setup",
        style="bold blue"
    ))
    
    # Check prerequisites
    console.print("\n[bold]Checking prerequisites...[/bold]")
    checks = {
        "Python 3.11+": check_python_version(),
        "Git": check_git(),
        "Docker": check_docker() if not skip_docker else True,
    }
    
    if not all(checks.values()):
        console.print("\n[red]Please install missing prerequisites and try again.[/red]")
        sys.exit(1)
    
    # Setup steps
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        steps = [
            ("Creating virtual environment", create_virtual_environment),
            ("Installing dependencies", install_dependencies if not skip_deps else lambda: True),
            ("Setting up environment file", setup_environment_file),
            ("Creating project directories", create_directories),
        ]
        
        if not skip_docker:
            steps.extend([
                ("Starting Docker services", start_docker_services),
                ("Checking services health", check_services_health),
            ])
        
        steps.append(("Installing pre-commit hooks", setup_pre_commit))
        
        for description, func in steps:
            task = progress.add_task(description, total=None)
            success = func()
            if success:
                progress.update(task, completed=True)
            else:
                progress.update(task, description=f"[red]✗ {description}[/red]")
                console.print("\n[red]Setup failed. Please check the errors above.[/red]")
                sys.exit(1)
    
    console.print("\n[green]✅ Setup completed successfully![/green]")
    print_next_steps()


if __name__ == "__main__":
    main()
