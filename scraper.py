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

import requests
import re
import time

# Use a 'set' for visited URLs because it automatically prevents duplicates
visited_urls = set()

def scrape_intel(url, depth=1):
    # Stop if we've reached our depth limit or already visited this URL
    if depth == 0 or url in visited_urls:
        return
    
    visited_urls.add(url)
    print(f"\n[*] [Depth {depth}] Scanning: {url}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            content = response.text
            
            # --- EXTRACT EMAILS ---
            emails = set(re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-z]{2,}', content))
            if emails:
                print(f"  [+] Found: {list(emails)}")
            
            # --- FIND INTERNAL LINKS ---
            # This regex looks for links that stay on the same domain
            links = re.findall(r'href=["\'](https?://.*?)["\']', content)
            
            # --- SAVE DATA ---
            with open("intel_report.txt", "a") as f:
                f.write(f"URL: {url}\nEmails: {list(emails)}\n\n")

            # --- RECURSIVE STEP ---
            for link in list(set(links))[:5]: # Limit to first 5 links per page to stay fast
                # We only follow links to the same site to avoid wandering off
                if "wikipedia.org" in link: # Replace with your target domain
                    time.sleep(1) # Be polite! Don't spam the server
                    scrape_intel(link, depth - 1)

    except Exception as e:
        print(f"  [!] Failed {url}: {e}")

if __name__ == "__main__":
    target = input("[?] Target URL to crawl: ")
    scrape_intel(target, depth=2) # Depth 2 means Home Page + 1 layer of subpages
    print(f"\n[!] Recon Complete. Total pages visited: {len(visited_urls)}")

# --- SMART RECURSIVE STEP ---
            # Keywords that usually lead to better "intel"
            interesting_words = ['about', 'staff', 'contact', 'login', 'admin', 'portal']

            for link in list(set(links)):
                # Check if the link is internal AND looks interesting
                if "wikipedia.org" in link: # Remember to match your target domain!
                    
                    # Only follow the link if it contains one of our interesting words
                    if any(word in link.lower() for word in interesting_words):
                        if link not in visited_urls:
                            time.sleep(1)
                            scrape_intel(link, depth - 1)
