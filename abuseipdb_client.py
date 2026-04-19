import requests
from typing import Optional, Dict
from config import ABUSEIPDB_API_KEY, ABUSEIPDB_BASE_URL, MAX_AGE_DAYS

def check_ip_reputation(ip_address: str) -> Optional[Dict]:
    """Fetch detailed reputation data from AbuseIPDB."""
    if not ABUSEIPDB_API_KEY or ABUSEIPDB_API_KEY.startswith("your_"):
        print("❌ ERROR: Please add your AbuseIPDB API key to the .env file.")
        return None

    if not is_valid_ip(ip_address):
        print(f"❌ ERROR: '{ip_address}' is not a valid IP address.")
        return None

    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }

    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': MAX_AGE_DAYS,
        'verbose': True
    }

    try:
        response = requests.get(ABUSEIPDB_BASE_URL, headers=headers, params=params, timeout=15)

        if response.status_code == 429:
            print("⚠️ Rate limit reached. Try again later.")
            return None
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

        data = response.json()
        return data.get('data')

    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except requests.exceptions.ConnectionError:
        print("❌ No internet connection.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return None


def is_valid_ip(ip: str) -> bool:
    """Basic IPv4 validation."""
    try:
        parts = ip.strip().split('.')
        if len(parts) != 4:
            return False
        return all(0 <= int(p) <= 255 for p in parts)
    except:
        return False


def get_quick_summary(data: Dict) -> Dict:
    """Helper for quick display in reports."""
    if not data:
        return {}
    return {
        "ip": data.get("ipAddress"),
        "abuse_score": data.get("abuseConfidenceScore", 0),
        "country": data.get("countryName"),
        "isp": data.get("isp"),
        "usage_type": data.get("usageType"),
        "total_reports": data.get("totalReports", 0),
        "last_reported": data.get("lastReportedAt"),
        "is_tor": data.get("isTor", False),
        "is_proxy": data.get("isProxy", False),
        "is_vpn": data.get("isVpn", False)
    }