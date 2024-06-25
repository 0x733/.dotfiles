import speedtest
import json
from datetime import datetime

def run_speedtest():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    st_results = st.results.dict()
    download_speed_mbps = st_results["download"] / 1_000_000  # Convert to Mbps
    upload_speed_mbps = st_results["upload"] / 1_000_000  # Convert to Mbps
    latency = st_results["ping"]
    return download_speed_mbps, upload_speed_mbps, latency

def display_speedtest_results(download_speed_mbps, upload_speed_mbps):
    download_speed_kbps = download_speed_mbps * 1_000  # Convert to kbps
    upload_speed_kbps = upload_speed_mbps * 1_000  # Convert to kbps

    download_results_mbps = {}
    upload_results_mbps = {}
    download_results_kbps = {}
    upload_results_kbps = {}

    # Download Speed Percentage Results (80% to 90% in 5% increments) in Mbps
    for percent in range(80, 91, 5):
        download_results_mbps[f"{percent}%"] = f"{download_speed_mbps * (percent / 100):.2f} Mbps"

    # Upload Speed Percentage Results (80% to 90% in 5% increments) in Mbps
    for percent in range(80, 91, 5):
        upload_results_mbps[f"{percent}%"] = f"{upload_speed_mbps * (percent / 100):.2f} Mbps"

    # Download Speed Increased Results (80% to 90% in 5% increments) in Mbps
    for percent in range(80, 91, 5):
        download_results_mbps[f"{percent}% Increased"] = f"{download_speed_mbps * ((100 + percent) / 100):.2f} Mbps"

    # Upload Speed Increased Results (80% to 90% in 5% increments) in Mbps
    for percent in range(80, 91, 5):
        upload_results_mbps[f"{percent}% Increased"] = f"{upload_speed_mbps * ((100 + percent) / 100):.2f} Mbps"

    # Download Speed Decreased Results (90% to 80% in 5% decrements) in Mbps
    for percent in range(90, 79, -5):
        download_results_mbps[f"{percent}% Decreased"] = f"{download_speed_mbps * (percent / 100):.2f} Mbps"

    # Upload Speed Decreased Results (90% to 80% in 5% decrements) in Mbps
    for percent in range(90, 79, -5):
        upload_results_mbps[f"{percent}% Decreased"] = f"{upload_speed_mbps * (percent / 100):.2f} Mbps"

    # Download Speed Percentage Results (80% to 90% in 5% increments) in kbps
    for percent in range(80, 91, 5):
        download_results_kbps[f"{percent}%"] = f"{download_speed_kbps * (percent / 100):.2f} kbps"

    # Upload Speed Percentage Results (80% to 90% in 5% increments) in kbps
    for percent in range(80, 91, 5):
        upload_results_kbps[f"{percent}%"] = f"{upload_speed_kbps * (percent / 100):.2f} kbps"

    # Download Speed Increased Results (80% to 90% in 5% increments) in kbps
    for percent in range(80, 91, 5):
        download_results_kbps[f"{percent}% Increased"] = f"{download_speed_kbps * ((100 + percent) / 100):.2f} kbps"

    # Upload Speed Increased Results (80% to 90% in 5% increments) in kbps
    for percent in range(80, 91, 5):
        upload_results_kbps[f"{percent}% Increased"] = f"{upload_speed_kbps * ((100 + percent) / 100):.2f} kbps"

    # Download Speed Decreased Results (90% to 80% in 5% decrements) in kbps
    for percent in range(90, 79, -5):
        download_results_kbps[f"{percent}% Decreased"] = f"{download_speed_kbps * (percent / 100):.2f} kbps"

    # Upload Speed Decreased Results (90% to 80% in 5% decrements) in kbps
    for percent in range(90, 79, -5):
        upload_results_kbps[f"{percent}% Decreased"] = f"{upload_speed_kbps * (percent / 100):.2f} kbps"

    return {
        "Download Speed Mbps": download_results_mbps,
        "Upload Speed Mbps": upload_results_mbps,
        "Download Speed kbps": download_results_kbps,
        "Upload Speed kbps": upload_results_kbps
    }

def main():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Test started at: {start_time}")

    # Run Speedtest
    download_speed_mbps, upload_speed_mbps, latency = run_speedtest()

    speedtest_results = {
        "Download Speed": f"{download_speed_mbps:.2f} Mbps",
        "Upload Speed": f"{upload_speed_mbps:.2f} Mbps",
        "Latency": f"{latency:.2f} ms",
        **display_speedtest_results(download_speed_mbps, upload_speed_mbps)
    }

    print(json.dumps(speedtest_results, indent=4))

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Test ended at: {end_time}")

if __name__ == "__main__":
    main()