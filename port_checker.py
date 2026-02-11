import subprocess
from datetime import datetime

TARGETS = ["scanme.nmap.org", "wikipedia.org", "google.com"]
LOG_FILE = "scan_results.txt"

def run_analysis(target):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[+] Analyzing: {target}...")
    
    try:
        scan_process = subprocess.run(['nmap', '-F', target], capture_output=True, text=True, timeout=30)
        
        # We split the output into individual lines
        lines = scan_process.stdout.splitlines()
        
        # We only keep lines that contain the word "open"
        open_ports = [line for line in lines if "open" in line]
        
        if open_ports:
            # Join the list of open ports into one string
            result_summary = "\n".join(open_ports)
            log_entry = f"--- {timestamp} | {target} ---\n{result_summary}\n"
            
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
            print(f"  [v] Found {len(open_ports)} open ports. Saved.")
        else:
            print(f"  [-] No open ports found on {target}.")
            
    except Exception as e:
        print(f"  [!] Error: {e}")
        
for t in TARGETS:
    run_analysis(t)

print(f"\n[***] Done. Check {LOG_FILE} for the full report.")
__version__ = "1.1.0"
__author__ = "5m3thNetw0rk"
# ... (your imports and function stay the same) ...

__version__ = "1.1.0"

# 3. The "Engine" (The Loop)
if __name__ == "__main__":
    # This line "announces" the version exactly once
    print(f"====================================")
    print(f"   ReconTool v{__version__} - Active")
    print(f"====================================")

    for t in TARGETS:
        run_analysis(t)

    print("\n[***] All scans complete. Systems clear.")
