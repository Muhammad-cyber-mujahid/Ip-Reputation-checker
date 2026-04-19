from rich.console import Console
from rich.prompt import Prompt
import sys

from config import ABUSEIPDB_API_KEY
from abuseipdb_client import check_ip_reputation
from reports.terminal_reports import show_mcq_menu, display_selected_reports
from reports.document_generator import generate_executive_document

console = Console()


def main():
    console.print("[bold green]🌐 IP Reputation Checker (AbuseIPDB)[/bold green]\n")

    if not ABUSEIPDB_API_KEY or ABUSEIPDB_API_KEY.startswith("your_"):
        console.print("[bold red]Please add your AbuseIPDB API key to the .env file first.[/bold red]")
        sys.exit(1)

    # Step 1: Get IP from user
    ip = Prompt.ask("Enter the IP address to check").strip()

    if not ip:
        console.print("[red]No IP entered. Exiting.[/red]")
        sys.exit(1)

    # Step 2: Fetch data from AbuseIPDB
    console.print(f"\n[cyan]🔍 Checking reputation for {ip}...[/cyan]")
    data = check_ip_reputation(ip)

    if not data:
        console.print("[red]Failed to fetch data. Please try again.[/red]")
        sys.exit(1)

    # Step 3: Show Interactive MCQ Menu
    selected = show_mcq_menu(data)

    # Step 4: Display chosen reports in terminal
    display_selected_reports(data, selected)

    # Step 5: ALWAYS generate the nice Executive PDF + DOCX (as requested)
    console.print("\n[bold yellow]Generating Professional Executive Report (PDF + DOCX)...[/bold yellow]")
    pdf_path = generate_executive_document(data, ip)

    console.print(f"[bold green]✅ Professional Reports saved:[/bold green]")
    console.print(f"   • PDF  → {pdf_path}")
    console.print(f"   • DOCX → {pdf_path.with_suffix('.docx')}")


if __name__ == "__main__":
    main()