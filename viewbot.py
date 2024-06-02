import requests
import random
import time
from bs4 import BeautifulSoup

def load_proxies(proxy_file):
    with open(proxy_file, 'r') as f:
        prioxies = [line.strip() for line in f if line.strip()]
    return proxies

def get_random_proxy(proxies):
    return random.choice(proxies)

def create_proxy_dict(proxy):
    return {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }

def check_livestream_status(url, proxy):
    proxy_dict = create_proxy_dict(proxy)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        response.raise_for_status()
        
        # Check if the livestream is still active by analyzing the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        is_live = soup.find('span', {'class': 'yt-badge-live'})
        
        if is_live:
            return True
        return False
    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code
        if status_code == 403:
            print(f'Proxy {proxy} is blocked by YouTube (403 Forbidden).')
        elif status_code == 429:
            print(f'Proxy {proxy} is rate-limited by YouTube (429 Too Many Requests).')
        else:
            print(f'HTTP error occurred with proxy {proxy}: {http_err}')
        return False
    except requests.exceptions.ProxyError:
        print(f'Proxy {proxy} is unreachable or blocked.')
        return False
    except requests.exceptions.SSLError:
        print(f'SSL error occurred with proxy {proxy}. It may be blocked by YouTube.')
        return False
    except requests.exceptions.RequestException as err:
        print(f'Error with proxy {proxy}: {err}')
        return False

def watch_livestream(url, proxies, watch_duration_hours=12):
    end_time = time.time() + watch_duration_hours * 3600  # Calculate end time
    while time.time() < end_time:
        proxy = get_random_proxy(proxies)
        
        if check_livestream_status(url, proxy):
            print(f'Livestream is active with proxy {proxy}. Watching...')
        else:
            print(f'Failed to connect or livestream has ended with proxy {proxy}. Retrying with a different proxy...')
        
        # Wait for a few seconds before the next check to simulate continuous watching
        time.sleep(5)

def main():
    proxy_file = 'prox.txt'
    proxies = load_proxies(proxy_file)
    url = 'https://www.youtube.com/watch?v=aOfeFBDqNxU'  # Replace with actual livestream URL
    
    while True:
        print("Starting new 12-hour watching session...")
        watch_livestream(url, proxies)
        print("12-hour watching session completed. Restarting...")

if __name__ == '__main__':
    main()
