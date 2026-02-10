import requests
import re
import time
import random
import concurrent.futures

# --- 1. SETUP & MEMORY ---
# These keep track of where we've been and who we are pretending to be
visited_urls = set()
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
]

def scrape_intel(url, depth=1):
    """
    This is the core function. It visits a URL, finds emails/links, 
    and then calls itself to dive deeper.
    """
    # Safety checks: stop if depth is 0 or if we already visited this link
    if depth == 0 or url in visited_urls:
        return
    
    visited_urls.add(url)
    links_to_follow = [] # Initializing this here prevents the 'not defined' error
    
    try:
        # 1. Prepare the request
        headers = {'User-Agent': random.choice(user_agents)}
        print(f"[*] Thread exploring: {url}")
        
        # 2. Make the connection
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # 3. Extract Emails
            emails = set(re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-z]{2,}', content))
            
            # 4. Extract all potential Links
            all_links = re.findall(r'href=["\'](https?://.*?)["\']', content)
            
            # 5. Save results to the file immediately
            if emails:
                with open("intel_report.txt", "a") as f:
                    f.write(f"URL: {url}\nEmails Found: {list(emails)}\n\n")
            
            # 6. Filter for "Internal" links (Change 'wikipedia.org' if target is different!)
            for link in all_links:
                if "wikipedia.org" in link and link not in visited_urls:
                    links_to_follow.append(link)
            
            # 7. Recursive step: visit the first 3 links we found
            for next_link in links_to_follow[:3]:
                time.sleep(1) # Wait 1 second to be 'stealthy' and polite
                scrape_intel(next_link, depth - 1)
        else:
            print(f"[!] {url} returned Status: {response.status_code}")

    except Exception as e:
        print(f"[!] Error connecting to {url}: {e}")

# --- 2. THE ENGINE ROOM ---
if __name__ == "__main__":
    print("\n" + "="*45)
    print("      ETHICAL RECON SPIDER - VERSION 2.0")
    print("="*45)
    
    start_url = input("[?] Enter starting URL: ")
    
    # This section manages our 'Worker Threads'
    # We use 3 workers so it's fast but doesn't crash your machine
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(scrape_intel, start_url, depth=2)

    print(f"\n[!] Mission Complete. {len(visited_urls)} pages mapped.")
    print("[*] Results recorded in 'intel_report.txt'")
