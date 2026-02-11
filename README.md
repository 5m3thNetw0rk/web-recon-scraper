# Web Recon Scraper

# Ethical Recon Spider v2.0

A multi-threaded, recursive web scraper built in Python for security research and reconnaissance. This tool identifies emails and internal links while simulating real browser behavior to avoid basic bot detection.

## 🚀 Features
* **Multi-threading:** Uses `ThreadPoolExecutor` for high-speed concurrent scanning.
* **Recursion:** Automatically "spiders" into sub-links to a specified depth.
* **Stealth:** Randomizes User-Agent headers to mimic Chrome, Firefox, and Safari.
* **Logging:** Automatically generates `intel_report.txt` with found data.

## 🛠️ Requirements
* Python 3.x
* `requests` library

## 📖 How to Use
1. Run the script: `python3 scraper.py`
2. Enter the target URL when prompted (e.g., `https://example.com`)
3. View the results in `intel_report.txt`

## ⚠️ Disclaimer
This tool is for educational and ethical security testing only. Always obtain permission before scanning a target.

### Requirements
This tool requires the following to be installed on your system:
* **Python 3.x**
* **Nmap** (Install via: `sudo apt install nmap`)

### Setup
To automate the scanner every hour, add the script to your crontab:
1. Run `crontab -e`
2. Add: `0 * * * * /usr/bin/python3 /path/to/your/port_checker.py`
