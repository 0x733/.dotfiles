import subprocess
import time
import speedtest
import dns.resolver

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

def run_dns_test(dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    start_time = time.time()
    try:
        resolver.resolve('google.com')
        end_time = time.time()
        query_time = end_time - start_time
        return query_time
    except Exception as e:
        return str(e)

def display_speedtest_results(download_speed):
    download_speed_kbps = download_speed / 1000  # Convert to kbps
    for percent in range(90, 79, -5):
        print(f"{percent}% of download speed: {download_speed_kbps * (percent / 100):.2f} kbps")

def main():
    download_speed, upload_speed, latency = run_speedtest()
    download_speed_mbps = download_speed / 1_000_000  # Convert to Mbps
    upload_speed_mbps = upload_speed / 1_000_000  # Convert to Mbps

    print(f"Original Download Speed: {download_speed_mbps:.2f} Mbps ({download_speed:.2f} bps)")
    print(f"Original Upload Speed: {upload_speed_mbps:.2f} Mbps ({upload_speed:.2f} bps)")
    print(f"Latency: {latency:.2f} ms")

    display_speedtest_results(download_speed)

    host = "8.8.8.8"
    print(f"Ping Test to {host}:")
    print(run_ping_test(host))

    print(f"Traceroute Test to {host}:")
    print(run_traceroute_test(host))

    dns_server = "8.8.8.8"
    print(f"DNS Test to {dns_server}:")
    dns_time = run_dns_test(dns_server)
    print(f"DNS query time: {dns_time:.2f} seconds")

if __name__ == "__main__":
    main()