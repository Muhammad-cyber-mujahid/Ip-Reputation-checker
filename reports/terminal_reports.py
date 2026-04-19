from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from config import RISK_THRESHOLDS, REPORT_TEMPLATES
from abuseipdb_client import get_quick_summary

console = Console()

def get_risk_recommendation(score: int) -> tuple:
    if score >= RISK_THRESHOLDS["BLOCK"]:
        return "BLOCK", "[bold red]BLOCK this IP immediately - High Risk[/bold red]"
    elif score >= RISK_THRESHOLDS["INVESTIGATE"]:
        return "INVESTIGATE", "[bold yellow]Investigate further - Medium Risk[/bold yellow]"
    else:
        return "LOW_RISK", "[bold green]Low Risk - Generally safe to allow[/bold green]"


def show_mcq_menu(data):
    summary = get_quick_summary(data)
    score = summary.get("abuse_score", 0)
    level, rec = get_risk_recommendation(score)

    console.print(Panel(
        f"IP: [cyan]{summary.get('ip')}[/cyan]  |  Abuse Score: [bold]{score}%[/bold]  |  Recommendation: {rec}",
        title="AbuseIPDB Report Ready", style="bold magenta"
    ))

    console.print("\n[bold]Choose Report Type:[/bold]\n")
    console.print("1. Technical Deep Dive          → Full raw data")
    console.print("2. Executive / Business Summary → Short for managers")
    console.print("3. SOC Analyst Report           → Actionable for security team")
    console.print("4. All Sections Combined\n")

    choice = Prompt.ask("Enter choice(s) separated by comma (e.g. 2 or 1,3)", default="2")
    selected = [c.strip() for c in choice.split(",") if c.strip() in REPORT_TEMPLATES]
    return selected if selected else ["2"]


def display_selected_reports(data, selected):
    score = data.get("abuseConfidenceScore", 0)
    level, rec = get_risk_recommendation(score)

    # Executive Summary (Template 2)
    if "2" in selected or "4" in selected:
        console.print("\n[bold green]=== EXECUTIVE / BUSINESS SUMMARY ===[/bold green]")
        console.print(rec)
        console.print(f"Abuse Confidence Score: {score}%")
        console.print(f"Country: {data.get('countryName')} | ISP: {data.get('isp')}")
        console.print(f"Usage Type: {data.get('usageType')}")
        console.print(f"Total Reports: {data.get('totalReports', 0)}")

    # SOC Analyst Report (Template 3)
    if "3" in selected or "4" in selected:
        console.print("\n[bold yellow]=== SOC ANALYST REPORT ===[/bold yellow]")
        console.print(f"Risk Level: {level}")
        console.print(f"Abuse Score: {score}%")
        console.print(f"Total Reports: {data.get('totalReports', 0)}")
        console.print(f"Last Reported: {data.get('lastReportedAt')}")
        console.print(f"Tor/Proxy/VPN: {data.get('isTor')}/{data.get('isProxy')}/{data.get('isVpn')}")

    # Technical Deep Dive (Template 1)
    if "1" in selected or "4" in selected:
        console.print("\n[bold cyan]=== TECHNICAL DEEP DIVE ===[/bold cyan]")
        console.print(f"IP: {data.get('ipAddress')}")
        console.print(f"Abuse Score: {score}%")
        console.print(f"Country: {data.get('countryName')} ({data.get('countryCode')})")
        console.print(f"ISP: {data.get('isp')}")
        console.print(f"Domain: {data.get('domain')}")
        console.print(f"Usage Type: {data.get('usageType')}")
        console.print(f"Total Reports: {data.get('totalReports')}")
        console.print(f"Is Public: {data.get('isPublic')}")
        # You can add reports list here later if needed