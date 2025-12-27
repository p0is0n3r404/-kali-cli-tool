import dns.resolver
import requests
from utils.ui import print_info, print_success, print_error, create_table, console

def get_dns_info(domain):
    """Retrieves DNS records (A, MX, TXT, NS)."""
    print_info(f"Retrieving DNS records for: [bold cyan]{domain}[/bold cyan]")
    records = {}
    record_types = ['A', 'MX', 'TXT', 'NS']
    
    table = create_table(f"DNS Records for {domain}")
    table.add_column("Type", style="cyan")
    table.add_column("Value", style="yellow")

    for r_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, r_type)
            records[r_type] = [str(rdata) for rdata in answers]
            for val in records[r_type]:
                table.add_row(r_type, val)
        except Exception:
            pass
            
    if records:
        console.print(table)
    else:
        print_error("Could not retrieve DNS records.")
    
    return records

def check_waf(url):
    """Detects common WAFs by checking HTTP headers and responses."""
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
        
    print_info(f"Checking for WAF on: [bold cyan]{url}[/bold cyan]")
    
    waf_signatures = {
        "Cloudflare": ["__cfduid", "cf-ray", "cloudflare"],
        "Akamai": ["akamai", "ak-grn"],
        "Sucuri": ["sucuri", "x-sucuri-id"],
        "ModSecurity": ["mod_security", "NOYB"],
        "Fortinet": ["fortiwafsidecookie"],
        "F5 BIG-IP": ["bigipserver", "F5"],
        "AWS WAF": ["aws-waf-token", "x-amzn-waf-action"]
    }

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        server = headers.get("Server", "").lower()
        
        detected_wafs = []

        # Check in headers
        for waf, sigs in waf_signatures.items():
            for sig in sigs:
                if any(sig in str(val).lower() for val in headers.values()) or sig in server:
                    detected_wafs.append(waf)
                    break

        if detected_wafs:
            waf_list = ", ".join(set(detected_wafs))
            print_success(f"WAF Detected: [bold red]{waf_list}[/bold red]")
            return set(detected_wafs)
        else:
            print_info("No specific WAF signatures detected.")
            return None

    except Exception as e:
        print_error(f"Error checking WAF: {e}")
        return None
