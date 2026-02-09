import requests
import re

def scrape_intel(url):
    # 1. Define our "Red Flag" keywords
    secrets_keywords = ['api_key', 'secret', 'password', 'aws_token', 'internal_only', 'config']
    
    print(f"[*] Scanning {url} for sensitive patterns...")
    
    try:
        # User-Agent header helps avoid being blocked
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
            emails = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-z]{2,}', content)
            links = re.findall(r'href=["\'](https?://.*?)["\']', content)

            # --- API KEY REGEX PATTERNS ---
            google_keys = re.findall(r'AIza[0-9A-Za-z\\-_]{35}', content)
            aws_keys = re.findall(r'AKIA[0-9A-Z]{16}', content)

            if google_keys:
                print(f"[!!!] POTENTIAL GOOGLE API KEY FOUND: {google_keys}")
            if aws_keys:
                print(f"[!!!] POTENTIAL AWS KEY FOUND: {aws_keys}")

            print(f"[+] Found {len(set(emails))} unique emails.")
            print(f"[+] Found {len(set(links))} unique links.")
            
            # --- SAVE THE REPORT ---
            with open("intel_report.txt", "a") as f:
                f.write(f"\n--- Intel Report for {url} ---\n")
                f.write(f"Flagged Keywords: {found_secrets}\n")
                f.write(f"Emails: {list(set(emails))}\n")
                if google_keys: f.write(f"Google Keys: {google_keys}\n")
                f.write("-" * 30 + "\n")
            
            print("[*] Results saved to intel_report.txt")
        else:
            print(f"[!] Failed to reach site. Status code: {response.status_code}")

    except Exception as e:
        # This block catches connection errors, timeouts, etc.
        print(f"[!] Error: {e}")

# --- TEST THE FUNCTION ---
# These lines have NO spaces before them!
# --- INTERACTIVE SECTION ---
# This replaces the hardcoded URL with a prompt for the user
if __name__ == "__main__":
    print("\n" + "="*30)
    print(" WEB RECON SCRAPER v1.0 ")
    print("="*30)
    
    user_url = input("[?] Which URL would you like to scan today? (Include http/https): ")
    
    if user_url.startswith("http"):
        scrape_intel(user_url)
    else:
        print("[!] Error: Please enter a valid URL starting with http:// or https://")
