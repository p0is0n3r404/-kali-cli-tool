import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from utils.ui import print_info, print_success, print_error, create_table, console

def get_banner(target_ip, port):
    """Attempts to grab the service banner from an open port."""
    try:
        s = socket.socket()
        s.settimeout(1.5)
        s.connect((target_ip, port))
        # Initial probe for banner-less services like HTTP
        if port in [80, 8080]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner if banner else "Unknown Service"
    except:
        return "No Banner Detected"

def scan_port(target_ip, port):
    """Scans a single port and returns data if open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target_ip, port))
    if result == 0:
        banner = get_banner(target_ip, port)
        s.close()
        return {"port": port, "status": "Open", "banner": banner}
    s.close()
    return None

def scan_ports(target, ports, threads=20):
    """
    Scans specified ports using multi-threading.
    """
    print_info(f"Scanning target: [bold cyan]{target}[/bold cyan]")
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print_error(f"Could not resolve hostname: {target}")
        return []

    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Using list comprehension to start threads
        future_to_port = [executor.submit(scan_port, target_ip, port) for port in ports]
        for future in future_to_port:
            res = future.result()
            if res:
                results.append(res)

    if results:
        table = create_table(f"Scan Results for {target}")
        table.add_column("Port", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Service Banner", style="yellow")
        
        for r in results:
            table.add_row(str(r['port']), r['status'], r['banner'])
        
        console.print(table)
    else:
        print_warning("No open ports found.")
        
    return results

if __name__ == "__main__":
    # Test scan on localhost
    scan_ports("127.0.0.1", [80, 443, 8080, 22])
