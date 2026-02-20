import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Optional
from config import load_config
from parser import parse_markdown
from converters import convert_content
from publishers import publish_to_platforms

app = typer.Typer(help="CLI tool for publishing content to multiple platforms")
console = Console()

@app.command()
def publish(
    markdown_file: Path = typer.Argument(..., help="Path to markdown file"),
    config_file: Path = typer.Option("config.yaml", help="Path to config file"),
    platforms: Optional[str] = typer.Option(None, help="Comma-separated platform names (default: all)"),
    dry_run: bool = typer.Option(False, help="Preview without publishing")
):
    """Publish markdown content to configured platforms"""
    
    if not markdown_file.exists():
        console.print(f"[red]Error: File {markdown_file} not found[/red]")
        raise typer.Exit(1)
    
    if not config_file.exists():
        console.print(f"[red]Error: Config file {config_file} not found[/red]")
        console.print("[yellow]Hint: Copy config.yaml.example to config.yaml and configure your platforms[/yellow]")
        raise typer.Exit(1)
    
    config = load_config(config_file)
    content = parse_markdown(markdown_file)
    
    target_platforms = platforms.split(",") if platforms else list(config["platforms"].keys())
    
    console.print(f"[cyan]Publishing: {content['title']}[/cyan]")
    console.print(f"[dim]Platforms: {', '.join(target_platforms)}[/dim]\n")
    
    if dry_run:
        console.print("[yellow]DRY RUN MODE - No actual publishing[/yellow]\n")
    
    results = []
    for platform_name in target_platforms:
        if platform_name not in config["platforms"]:
            console.print(f"[red]Platform {platform_name} not configured[/red]")
            continue
        
        platform_config = config["platforms"][platform_name]
        converted = convert_content(content, platform_name)
        
        if dry_run:
            console.print(f"[dim]Would publish to {platform_name}[/dim]")
            results.append((platform_name, "skipped", "dry run"))
        else:
            status, message = publish_to_platforms(platform_name, converted, platform_config)
            results.append((platform_name, status, message))
            
            if status == "success":
                console.print(f"[green]✓ {platform_name}: Published successfully[/green]")
            else:
                console.print(f"[red]✗ {platform_name}: {message}[/red]")
    
    console.print("\n[bold]Summary:[/bold]")
    table = Table()
    table.add_column("Platform")
    table.add_column("Status")
    table.add_column("Message")
    
    for platform, status, message in results:
        color = "green" if status == "success" else "red" if status == "error" else "yellow"
        table.add_row(platform, f"[{color}]{status}[/{color}]", message)
    
    console.print(table)

@app.command()
def init():
    """Create example config file"""
    example_path = Path("config.yaml.example")
    target_path = Path("config.yaml")
    
    if target_path.exists():
        console.print("[yellow]config.yaml already exists[/yellow]")
        raise typer.Exit(1)
    
    if example_path.exists():
        import shutil
        shutil.copy(example_path, target_path)
        console.print("[green]Created config.yaml from example[/green]")
    else:
        console.print("[red]config.yaml.example not found[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
