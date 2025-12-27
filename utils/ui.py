from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# Custom theme for K-SAK
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red",
    "success": "bold green",
    "header": "bold magenta",
    "banner": "bold bright_cyan",
})

console = Console(theme=custom_theme)

BANNER_TEXT = r"""
 /$$   /$$        /$$$$$$   /$$$$$$  /$$   /$$
| $$  /$$/       /$$__  $$ /$$__  $$| $$  /$$/
| $$ /$$/       | $$  \__/| $$  \ $$| $$ /$$/ 
| $$$$$/ /$$$$$$|  $$$$$$ | $$$$$$$$| $$$$$/  
| $$  $$|______/ \____  $$| $$__  $$| $$  $$  
| $$\  $$        /$$  \ $$| $$  | $$| $$\  $$ 
| $$ \  $$      |  $$$$$$/| $$  | $$| $$ \  $$
|__/  \__/       \______/ |__/  |__/|__/  \__/
"""

def print_banner():
    """Prints the professional K-SAK banner."""
    console.print(Panel(
        Text(BANNER_TEXT, style="banner"),
        subtitle="[bold green]v2.0 - Kali Swiss Army Knife[/bold green]",
        title="[bold yellow]Created by p0is0n3r404[/bold yellow]",
        border_style="magenta",
        padding=(1, 1)
    ))

def print_info(message):
    console.print(f"[info]\[*][/info] {message}")

def print_success(message):
    console.print(f"[success]\[+][/success] {message}")

def print_warning(message):
    console.print(f"[warning]\[!][/warning] {message}")

def print_error(message):
    console.print(f"[danger]\[-][/danger] {message}")

def create_table(title):
    return Table(title=title, header_style="header", border_style="magenta")
