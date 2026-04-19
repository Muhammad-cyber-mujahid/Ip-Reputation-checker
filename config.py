import os
from dotenv import load_dotenv
from pathlib import Path



# Load environment variables from .env file
load_dotenv()

# AbuseIPDB Settings
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "").strip()

ABUSEIPDB_BASE_URL = "https://api.abuseipdb.com/api/v2/check"
MAX_AGE_DAYS = int(os.getenv("MAX_AGE_DAYS", 90))

# Output Directory
OUTPUT_DIR = Path("output_reports")
OUTPUT_DIR.mkdir(exist_ok=True)

# Risk Level Thresholds
RISK_THRESHOLDS = {
    "BLOCK": 80,
    "INVESTIGATE": 50,
    "LOW_RISK": 0
}

# Report Templates
REPORT_TEMPLATES = {
    "1": "technical_deep_dive",
    "2": "executive_summary",
    "3": "soc_analyst_report",
    "4": "all"
}

# Debug information
if ABUSEIPDB_API_KEY:
    print(f"✅ API Key loaded successfully (length: {len(ABUSEIPDB_API_KEY)} characters)")
else:
    print("❌ WARNING: No API Key found in .env file!")

print("✅ Configuration loaded successfully")