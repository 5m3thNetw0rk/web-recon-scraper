import subprocess
import socket
import json # New import for structured data
from datetime import datetime

# ... (grab_banner and analyze_intelligence functions stay the same) ...

def save_as_json(data):
    """Saves scan data into a structured JSON file."""
    filename = "intelligence_feed.json"
    try:
        # 1. Read existing data
        with open(filename, "r") as f:
            feed = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        feed = []

    # 2. Add new data and save
    feed.append(data)
    with open(filename, "w") as f:
        json.dump(feed, f, indent=4)

def run_analysis(target):
    # Create a 'Report' object for this scan
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "findings": []
    }
    
    # ... (your existing nmap scan logic here) ...
    # When you find an open port, add it to the report:
    finding = {
        "port": port_num,
        "banner": banner,
        "intel": analyze_intelligence(banner)
    }
    report["findings"].append(finding)

    # After the loop, export the intelligence
    if report["findings"]:
        save_as_json(report)

import subprocess
import socket
from datetime import datetime

# --- CONFIGURATION ---
TARGETS = ["scanme.nmap.org", "8.8.8.8"]
LOG_FILE = "scan_results.txt"
__version__ = "1.2.0"

def grab_banner(ip, port):
    """Attempt to knock on the door and see who answers."""
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        # Receive up to 1024 bytes of the 'greeting'
        banner = s.recv(1024).decode(errors='ignore').strip()
        return banner if banner else "Connected (No banner sent)"
    except:
        return "No response"
    finally:
        s.close()

def run_analysis(target):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[+] Analyzing: {target}...")
    
    try:
        # Run a fast scan to find open doors
        scan_process = subprocess.run(['nmap', '-F', target], capture_output=True, text=True, timeout=30)
        lines = scan_process.stdout.splitlines()
        
        found_data = []
        for line in lines:
            if "open" in line:
                # Extract port (e.g., '22' from '22/tcp')
                port_num = int(line.split('/')[0])
                # Now, use our new Banner Grabbing skill
                banner = grab_banner(target, port_num)
                
                result = f"Port {port_num}: {banner}"
                print(f"  [!] {result}")
                found_data.append(result)

        # Logging the intelligence
        if found_data:
            with open(LOG_FILE, "a") as f:
                f.write(f"--- {timestamp} | {target} ---\n" + "\n".join(found_data) + "\n\n")
            
    except Exception as e:
        print(f"  [!] Error scanning {target}: {e}")

if __name__ == "__main__":
    print(f"====================================")
    print(f"   ReconTool v{__version__} - Active")
    print(f"====================================")

    for t in TARGETS:
        run_analysis(t)
