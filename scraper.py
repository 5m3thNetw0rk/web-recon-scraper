import requests
import re

def scrape_intel(url):
    # 1. Define our "Red Flag" keywords
    secrets_keywords = ['api_key', 'secret', 'password', 'aws_token', 'internal_only', 'config']
    
    print(f"[*] Scanning {url} for sensitive patterns...")
    
    try:
        # User-Agent header helps avoid being blocked by the website
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # --- SECRET FINDER LOGIC ---
            found_secrets = []
            for word in secrets_keywords:
                if word in content.lower():
                    found_secrets.append(word)
            
            if found_secrets:
                print(f"[!] ALERT: Found potential sensitive keywords: {found_secrets}")
            
            # --- EMAIL & LINK EXTRACTION ---
            # Finds patterns like user@domain.com
            emails = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-z]{2,}', content)
            
            # Finds patterns like http:// or https://
            links = re.findall(r'href=["\'](https?://.*?)["\']', content)

            print(f"[+] Found {len(set(emails))} unique emails.")
            print(f"[+] Found {len(set(links))} unique links.")
            
            # --- SAVE THE REPORT ---
            with open("intel_report.txt", "a") as f:
                f.write(f"\n--- Intel Report for {url} ---\n")
                f.write(f"Flagged Keywords: {found_secrets}\n")
                f.write(f"Emails: {list(set(emails))}\n")
                f.write("-" * 30 + "\n")
            
            print("[*] Results saved to intel_report.txt")
        else:
            print(f"[!] Failed to reach site. Status code: {response.status_code}")

    except Exception as e:
        print(f"[!] Error: {e}")

# --- TEST THE FUNCTION ---
# You can change this URL to any site you have permission to scan
target_url = "https://www.wikipedia.org" 
scrape_intel(target_url)
