import subprocess
import statistics

def ping(host, count):
    command = ['ping', '-c', str(count), host]
    try:
        output = subprocess.run(command, capture_output=True, text=True, timeout=60).stdout
        return output
    except subprocess.TimeoutExpired:
        return ""

def parse_ping_output(output):
    lines = output.split('\n')
    times = []
    for line in lines:
        if 'time=' in line:
            time_str = line.split('time=')[1].split(' ')[0]
            times.append(float(time_str))
    return times

def check_bufferbloat(times):
    if len(times) < 2:
        return False, 0, 0, 0, 0
    
    avg_rtt = statistics.mean(times)
    max_rtt = max(times)
    min_rtt = min(times)
    stddev_rtt = statistics.stdev(times)
    bufferbloat = max_rtt - min_rtt

    return bufferbloat > 100, avg_rtt, max_rtt, min_rtt, stddev_rtt

def main():
    host = '1.1.1.1'  # Cloudflare DNS
    count = 20
    
    print(f"Pinging {host} with {count} packets...")
    output = ping(host, count)
    times = parse_ping_output(output)
    
    if times:
        bufferbloat_detected, avg_rtt, max_rtt, min_rtt, stddev_rtt = check_bufferbloat(times)
        print(f"Average RTT: {avg_rtt:.2f} ms")
        print(f"Max RTT: {max_rtt:.2f} ms")
        print(f"Min RTT: {min_rtt:.2f} ms")
        print(f"RTT Standard Deviation (SQM): {stddev_rtt:.2f} ms")
        
        if bufferbloat_detected:
            print("Bufferbloat detected!")
        else:
            print("No bufferbloat detected.")
    else:
        print("No ping times were recorded. Please check your connection and try again.")

if __name__ == "__main__":
    main()