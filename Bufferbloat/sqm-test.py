import subprocess
import time
import speedtest
import dns.resolver
import json
from datetime import datetime

def run_speedtest():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    st_results = st.results.dict()
    download_speed = st_results["download"]  # in bits per second
    upload_speed = st_results["upload"]  # in bits per second
    latency = st_results["ping"]
    return download_speed, upload_speed, latency

def run_ping_test(host):
    result = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True)
    return result.stdout

def run_traceroute_test(host):
    result = subprocess.run(["traceroute", host], capture_output=True, text=True)
    return result.stdout

def run_dns_test(dns_servers):
    results = {}
    for dns_server in dns_servers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        start_time = time.time()
        try:
            resolver.resolve('google.com')
            end_time = time.time()
            query_time = end_time - start_time
            results[dns_server] = query_time
        except Exception as e:
            results[dns_server] = str(e)
    return results

def display_speedtest_results(download_speed, upload_speed):
    download_speed_kbps = download_speed / 1000  # Convert to kbps
    upload_speed_kbps = upload_speed / 1000  # Convert to kbps
    download_results = {}
    upload_results = {}
    
    # Download Speed Percentage Results (80% to 90% in 5% increments)
    for percent in range(80, 91, 5):
        download_results[f"{percent}%"] = f"{download_speed_kbps * (percent / 100):.2f} kbps"

    # Upload Speed Percentage Results (80% to 90% in 5% increments)
    for percent in range(80, 91, 5):
        upload_results[f"{percent}%"] = f"{upload_speed_kbps * (percent / 100):.2f} kbps"

    # Download Speed Decreased Results (90% to 80% in 5% decrements)
    for percent in range(90, 79, -5):
        download_results[f"{percent}%"] = f"{download_speed_kbps * (percent / 100):.2f} kbps"

    # Upload Speed Decreased Results (90% to 80% in 5% decrements)
    for percent in range(90, 79, -5):
        upload_results[f"{percent}%"] = f"{upload_speed_kbps * (percent / 100):.2f} kbps"

    return download_results, upload_results

def check_internet_connection():
    try:
        response = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True)
        if response.returncode == 0:
            return "Connected"
        else:
            return "Disconnected"
    except Exception as e:
        return f"Error: {e}"

def save_results_to_file(results, filename="network_test_results.json"):
    with open(filename, "w") as file:
        json.dump(results, file, indent=4)

def main():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Test started at: {start_time}")
    
    # Check Internet Connection
    internet_status = check_internet_connection()
    print(f"Internet Connection Status: {internet_status}")

    # Run Speedtest
    download_speed, upload_speed, latency = run_speedtest()
    download_speed_mbps = download_speed / 1_000_000  # Convert to Mbps
    upload_speed_mbps = upload_speed / 1_000_000  # Convert to Mbps

    speedtest_results = {
        "Download Speed": f"{download_speed_mbps:.2f} Mbps ({download_speed:.2f} bps)",
        "Upload Speed": f"{upload_speed_mbps:.2f} Mbps ({upload_speed:.2f} bps)",
        "Latency": f"{latency:.2f} ms",
        "Download Speed Results": display_speedtest_results(download_speed, upload_speed)[0],
        "Upload Speed Results": display_speedtest_results(download_speed, upload_speed)[1]
    }

    print(json.dumps(speedtest_results, indent=4))

    # Run Ping Test
    host = "8.8.8.8"
    print(f"Ping Test to {host}:")
    ping_results = run_ping_test(host)
    print(ping_results)

    # Run Traceroute Test
    print(f"Traceroute Test to {host}:")
    traceroute_results = run_traceroute_test(host)
    print(traceroute_results)

    # Run DNS Test
    dns_servers = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
    print(f"DNS Test to servers: {', '.join(dns_servers)}")
    dns_results = run_dns_test(dns_servers)
    print(json.dumps(dns_results, indent=4))

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Test ended at: {end_time}")

    # Save results to file
    results = {
        "start_time": start_time,
        "end_time": end_time,
        "internet_status": internet_status,
        "speedtest_results": speedtest_results,
        "ping_results": ping_results,
        "traceroute_results": traceroute_results,
        "dns_results": dns_results
    }
    save_results_to_file(results)

if __name__ == "__main__":
    main()