# 🛠️ K-SAK v2.0: Kali Swiss Army Knife CLI Tool

K-SAK is a professional-grade, multi-threaded security reconnaissance toolkit designed for Kali Linux. It centralizes advanced scanning, enumeration, and intelligence gathering modules into a single, high-performance CLI application.

![Usage Screenshot](assets/usage_screenshot.png)

## 🚀 New in v2.0

- **⚡ Atomic Speed**: Full multi-threading for all scanning and enumeration tasks.
- **💎 Rich UI**: Beautiful terminal interface with tables, color themes, and progress feedback.
- **🔍 Advanced Recon**: Integrated DNS discovery and WAF detection.
- **📂 DirHunter**: High-speed directory and file bruteforcing.
- **📄 Reporting**: Export results to structured JSON for professional analysis.

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/p0is0n3r404/-kali-cli-tool.git
   cd -kali-cli-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Modules & Usage

### 1. 🛡️ Port Scan (Threaded)

Scans target ports and attempts to grab service banners.

```bash
python main.py scan google.com -p 80 443 8080 -t 50
```

### 2. 🌐 Subdomain Enumeration

Fast discovery of subdomains using a multi-threaded resolver.

```bash
python main.py sub example.com -w www mail dev
```

### 3. 📂 DirHunter (Directory Bruteforce)

Identify hidden files and directories on a web server.

```bash
python main.py dir http://example.com/ -t 30
```

### 4. 🛰️ Service Recon (DNS & WAF)

Analyze DNS records and detect Web Application Firewalls.

```bash
python main.py recon example.com --dns --waf
```

### 5. 🔑 Hash Identification

Instantly identify the algorithm used for a given hash.

```bash
python main.py hash 5d41402abc4b2a76b9719d911017c592
```

## ⚙️ Global Options

- `-t, --threads`: Set number of concurrent threads (default: 20).
- `-o, --output`: Save results to a timestamped JSON report.

## 📂 Project Structure

- `main.py`: Entry point and module orchestration.
- `modules/`: Core security modules (scanner, dirbrute, recon, etc.).
- `utils/`: UI theme and reporting utilities.
- `assets/`: Project media and screenshots.

## ⚠️ Disclaimer

This tool is for educational and ethical testing purposes only. Usage of K-SAK for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws.

---

Developed by [p0is0n3r404](https://github.com/p0is0n3r404)
v2.0 Stable Release
