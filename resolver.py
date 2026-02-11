import socket

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"Target: {domain} --> IP: {ip}")
    except Exception as e:
        print(f"Could not resolve {domain}: {e}")

target = input("Enter a domain (e.g. google.com): ")
get_ip(target)
