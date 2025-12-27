import socket
from concurrent.futures import ThreadPoolExecutor
from utils.ui import print_info, print_success, print_error, create_table, console

def check_subdomain(domain, sub):
    """resolves a single subdomain."""
    target = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(target)
        return {"subdomain": target, "ip": ip}
    except socket.gaierror:
        return None

def enumerate_subdomains(domain, subdomains, threads=30):
    """
    Checks which subdomains from a list exist using multi-threading.
    """
    print_info(f"Enumerating subdomains for: [bold cyan]{domain}[/bold cyan]")
    
    found_subdomains = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_sub = [executor.submit(check_subdomain, domain, sub) for sub in subdomains]
        for future in future_to_sub:
            res = future.result()
            if res:
                found_subdomains.append(res)

    if found_subdomains:
        table = create_table(f"Subdomains for {domain}")
        table.add_column("Subdomain", style="cyan")
        table.add_column("IP Address", style="green")
        
        for s in found_subdomains:
            table.add_row(s['subdomain'], s['ip'])
        
        console.print(table)
        print_success(f"Found {len(found_subdomains)} active subdomains.")
    else:
        print_error("No subdomains found.")
            
    return found_subdomains

if __name__ == "__main__":
    # Test enumeration
    test_subs = ["www", "mail", "dev", "test", "api"]
    enumerate_subdomains("google.com", test_subs)
