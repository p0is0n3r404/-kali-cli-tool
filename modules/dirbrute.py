import requests
from concurrent.futures import ThreadPoolExecutor
from utils.ui import print_info, print_success, print_error, create_table, console

# A small built-in wordlist for quick scans
DEFAULT_WORDLIST = [
    "admin", "login", "config", "backup", "api", "v1", "v2", "db", "upload", 
    "setup", "secret", "private", "dev", "test", "staging", "logs", "phpinfo",
    ".env", ".git", ".htaccess", "robots.txt", "wp-admin", "cgi-bin"
]

def check_directory(url, directory):
    """Checks if a single directory exists on the target URL."""
    target_url = f"{url.rstrip('/')}/{directory}"
    try:
        response = requests.get(target_url, timeout=2, allow_redirects=False)
        if response.status_code in [200, 204, 301, 302, 307, 403]:
            return {"directory": directory, "status": response.status_code, "url": target_url}
    except requests.RequestException:
        pass
    return None

def bruteforce_directories(url, wordlist=None, threads=20):
    """
    Bruteforces directories on a target URL using multi-threading.
    """
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
        
    print_info(f"Starting DirHunter for: [bold cyan]{url}[/bold cyan]")
    
    directories = wordlist if wordlist else DEFAULT_WORDLIST
    found_dirs = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_dir = [executor.submit(check_directory, url, d) for d in directories]
        for future in future_to_dir:
            res = future.result()
            if res:
                found_dirs.append(res)

    if found_dirs:
        table = create_table(f"Directories found on {url}")
        table.add_column("Directory", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Full URL", style="yellow")
        
        for d in found_dirs:
            table.add_row(d['directory'], str(d['status']), d['url'])
        
        console.print(table)
        print_success(f"Discovered {len(found_dirs)} directories/files.")
    else:
        print_error("No directories discovered.")
        
    return found_dirs
