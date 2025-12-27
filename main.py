import sys
import argparse
from modules.scanner import scan_ports
from modules.hasher import identify_hash
from modules.enumerator import enumerate_subdomains
from modules.dirbrute import bruteforce_directories
from modules.recon import get_dns_info, check_waf
from utils.ui import print_banner, print_info, print_success, print_error, console
from utils.reporter import save_to_json

def main():
    print_banner()
    
    # Parent parser for global arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads to use (default: 20)")
    parent_parser.add_argument("-o", "--output", action="store_true", help="Save results to a JSON report")

    parser = argparse.ArgumentParser(description="K-SAK: Kali Swiss Army Knife CLI Tool v2.0")
    subparsers = parser.add_subparsers(dest="command", help="Available modules")

    # Scan command
    scan_parser = subparsers.add_parser("scan", parents=[parent_parser], help="Professional Port Scanner")
    scan_parser.add_argument("target", help="Target IP or hostname")
    scan_parser.add_argument("-p", "--ports", nargs="+", type=int, default=[21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080], help="Custom ports to scan")

    # Subdomain command
    sub_parser = subparsers.add_parser("sub", parents=[parent_parser], help="Subdomain Enumerator")
    sub_parser.add_argument("domain", help="Target domain")
    sub_parser.add_argument("-w", "--wordlist", nargs="+", help="Custom wordlist for subdomains")

    # DirHunter command
    dir_parser = subparsers.add_parser("dir", parents=[parent_parser], help="Directory Bruteforcer (DirHunter)")
    dir_parser.add_argument("url", help="Target URL")
    dir_parser.add_argument("-w", "--wordlist", nargs="+", help="Custom wordlist for directories")

    # Recon command (DNS & WAF)
    recon_parser = subparsers.add_parser("recon", parents=[parent_parser], help="Service Recon (DNS & WAF)")
    recon_parser.add_argument("target", help="Target domain/URL")
    recon_parser.add_argument("--dns", action="store_true", help="Run DNS reconnaissance")
    recon_parser.add_argument("--waf", action="store_true", help="Run WAF detection")

    # Hash command
    hash_parser = subparsers.add_parser("hash", parents=[parent_parser], help="Hash Identifier")
    hash_parser.add_argument("hash_string", help="Hash to identify")

    args = parser.parse_args()

    results = None
    target_name = ""

    if args.command == "scan":
        target_name = args.target
        results = scan_ports(args.target, args.ports, threads=args.threads)
    
    elif args.command == "sub":
        target_name = args.domain
        custom_subs = args.wordlist if args.wordlist else ["www", "mail", "dev", "test", "api", "smtp", "ftp", "admin", "blog"]
        results = enumerate_subdomains(args.domain, custom_subs, threads=args.threads)
    
    elif args.command == "dir":
        target_name = args.url
        results = bruteforce_directories(args.url, wordlist=args.wordlist, threads=args.threads)
    
    elif args.command == "recon":
        target_name = args.target
        results = {}
        if args.dns:
            results["dns"] = get_dns_info(args.target)
        if args.waf:
            results["waf"] = list(check_waf(args.target)) if check_waf(args.target) else []
        if not args.dns and not args.waf:
            # Run both if no flags specified
            results["dns"] = get_dns_info(args.target)
            waf_res = check_waf(args.target)
            results["waf"] = list(waf_res) if waf_res else []
    
    elif args.command == "hash":
        algo = identify_hash(args.hash_string)
        print_success(f"Identified Algorithm: [bold yellow]{algo}[/bold yellow]")
    
    else:
        parser.print_help()
        sys.exit(0)

    # Save results if output flag is set
    if args.output and results:
        save_to_json(results, target_name, args.command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nInterrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
