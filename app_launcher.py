import os
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# =============================
# 🗂 تعریف مسیرهای اپلیکیشن‌ها
# =============================
APPS = {
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "notepad++": r"C:\Program Files\Notepad++\notepad++.exe",
    "vscode": r"C:\Users\$USER\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "calc": r"C:\Windows\System32\calc.exe",
    "paint": r"C:\Windows\System32\mspaint.exe",
}

def resolve_path(path: str) -> str:
    """جایگزینی $USER با نام کاربری واقعی و بررسی وجود فایل"""
    if "$USER" in path:
        path = path.replace("$USER", os.getlogin())
    return path

def is_valid_app(app_name: str) -> bool:
    """بررسی اینکه آیا اپلیکیشن وجود دارد یا نه"""
    raw_path = APPS.get(app_name.lower())
    if not raw_path:
        return False
    real_path = resolve_path(raw_path)
    return os.path.isfile(real_path)

def launch_app(app_name: str):
    """اجرای اپلیکیشن انتخاب‌شده"""
    raw_path = APPS[app_name.lower()]
    real_path = resolve_path(raw_path)
    try:
        os.startfile(real_path)
        return True
    except Exception as e:
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"[red]❌ Failed to launch '{app_name}': {e}[/red]")
        else:
            print(f"❌ Failed to launch '{app_name}': {e}")
        return False

def show_menu():
    """نمایش منوی زیبا"""
    if RICH_AVAILABLE:
        console = Console()
        table = Table(title="🚀 Available Applications", title_style="bold cyan")
        table.add_column("App Name", style="green")
        table.add_column("Status", style="yellow")

        for app in APPS:
            status = "✅ Installed" if is_valid_app(app) else "⚠️ Not Found"
            table.add_row(app.capitalize(), status)

        console.print(table)
        console.print("\n[dim]Type the app name to launch it, or 'exit' to quit.[/dim]\n")
    else:
        print("\n=== Available Applications ===")
        for app in APPS:
            status = "✅" if is_valid_app(app) else "❌"
            print(f"{status} {app.capitalize()}")
        print("\nType an app name to launch, or 'exit' to quit.\n")

def main():
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("✨ Application Launcher v2.0\nFast • Clean • Extensible", 
                                title="Welcome", border_style="bright_blue"))
    else:
        print("✨ Application Launcher v2.0")
        print("Fast • Clean • Extensible")
        print("-" * 30)

    while True:
        show_menu()
        if RICH_AVAILABLE:
            command = Prompt.ask("[bold yellow]Enter command[/bold yellow]").strip().lower()
        else:
            command = input("Enter command: ").strip().lower()

        if command in ("exit", "quit"):
            if RICH_AVAILABLE:
                console.print("[bold green]👋 Goodbye! Have a great day![/bold green]")
            else:
                print("👋 Goodbye! Have a great day!")
            break

        if command in APPS:
            if is_valid_app(command):
                if RICH_AVAILABLE:
                    console = Console()
                    console.print(f"[bold green]Launching {command.capitalize()}... ✅[/bold green]")
                else:
                    print(f"Launching {command.capitalize()}... ✅")
                launch_app(command)
            else:
                if RICH_AVAILABLE:
                    console.print(f"[red]⚠️ '{command}' is not installed or path is invalid.[/red]")
                else:
                    print(f"⚠️ '{command}' is not installed or path is invalid.")
        else:
            if RICH_AVAILABLE:
                console.print(f"[red]❌ Unknown command: '{command}'. Type 'exit' to quit.[/red]")
            else:
                print(f"❌ Unknown command: '{command}'. Type 'exit' to quit.")

if __name__ == "__main__":
    main()