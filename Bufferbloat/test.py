import requests
import time

def get_librespeed_servers():
    response = requests.get("https://librespeed.org/backend/servers.php")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching servers: {response.status_code}")
        return []

def bufferbloat_test(server):
    download_speeds = []
    upload_speeds = []
    latencies = []
    
    # Download Test
    for _ in range(3):
        start_time = time.time()
        response = requests.get(server['url'])
        end_time = time.time()
        size_mb = len(response.content) / (1024 * 1024)
        duration = end_time - start_time
        download_speed = size_mb / duration
        download_speeds.append(download_speed)
    
    # Upload Test
    for _ in range(3):
        start_time = time.time()
        response = requests.post(server['url'], data=b'x' * 1024 * 1024)
        end_time = time.time()
        size_mb = len(response.content) / (1024 * 1024)
        duration = end_time - start_time
        upload_speed = size_mb / duration
        upload_speeds.append(upload_speed)
    
    # Latency Test
    for _ in range(3):
        start_time = time.time()
        requests.get(server['url'])
        end_time = time.time()
        latency = end_time - start_time
        latencies.append(latency * 1000)  # milliseconds
    
    return {
        'download_speed_mbps': sum(download_speeds) / len(download_speeds),
        'upload_speed_mbps': sum(upload_speeds) / len(upload_speeds),
        'average_latency_ms': sum(latencies) / len(latencies),
        'bufferbloat': max(latencies) - min(latencies)
    }

def main():
    servers = get_librespeed_servers()
    if not servers:
        print("No servers found. Exiting...")
        return
    
    print("Available servers:")
    for i, server in enumerate(servers):
        print(f"{i}: {server['name']} ({server['url']})")
    
    server_index = int(input("Select server index for bufferbloat test: "))
    server = servers[server_index]
    
    print(f"Running bufferbloat test on {server['name']}...")
    results = bufferbloat_test(server)
    
    print(f"Download Speed: {results['download_speed_mbps']} Mbps")
    print(f"Upload Speed: {results['upload_speed_mbps']} Mbps")
    print(f"Average Latency: {results['average_latency_ms']} ms")
    print(f"Bufferbloat: {results['bufferbloat']} ms")

if __name__ == "__main__":
    main()