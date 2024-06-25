package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
)

type Config struct {
	DNSServers    []string `json:"dnsServers"`
	SearchEngines []string `json:"searchEngines"`
	GameServers   []string `json:"gameServers"`
	Bandwidth     int      `json:"bandwidth"`  // Bant genişliği kbps cinsinden
}

func loadConfig(filename string) (*Config, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	var config Config
	err = json.Unmarshal(data, &config)
	if err != nil {
		return nil, err
	}
	return &config, nil
}

func pingTest(target string) {
	fmt.Printf("Ping test: %s\n", target)
	cmd := exec.Command("ping", "-c", "4", target)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error: %s\n", err)
	} else {
		fmt.Println(string(output))
	}
	fmt.Println()
}

func packetLossTest(target string) {
	fmt.Printf("Paket kaybı testi (mtr): %s\n", target)
	cmd := exec.Command("sudo", "mtr", "-r", "-c", "10", target)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error: %s\n", err)
	} else {
		fmt.Println(string(output))
	}
	fmt.Println()
}

func tracerouteTest(target string) {
	fmt.Printf("Traceroute testi: %s\n", target)
	cmd := exec.Command("traceroute", target)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error: %s\n", err)
	} else {
		fmt.Println(string(output))
	}
	fmt.Println()
}

func httpTest(target string) {
	fmt.Printf("HTTP erişim testi: %s\n", target)
	cmd := exec.Command("curl", "-I", target)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error: %s\n", err)
	} else {
		fmt.Println(string(output))
	}
	fmt.Println()
}

func bufferbloatTest() {
	fmt.Println("Bufferbloat testi: netperf ile")
	cmd := exec.Command("netperf", "-H", "localhost", "-l", "60", "--", "-P", "0", "-D", "1", "-o", "THROUGHPUT,MEAN_LATENCY")
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error: %s\n", err)
	} else {
		fmt.Println(string(output))
	}
	fmt.Println()
}

func calculateSQM(bandwidth int) {
	fmt.Printf("SQM Ayarları (Bant genişliği: %d kbps):\n", bandwidth)
	bw90 := bandwidth * 90 / 100
	bw85 := bandwidth * 85 / 100
	bw80 := bandwidth * 80 / 100
	fmt.Printf(" %d%%: %d kbps\n", 90, bw90)
	fmt.Printf(" %d%%: %d kbps\n", 85, bw85)
	fmt.Printf(" %d%%: %d kbps\n", 80, bw80)
	fmt.Println()
}

func runTests(targets []string) {
	for _, target := range targets {
		pingTest(target)
		packetLossTest(target)
		tracerouteTest(target)
		httpTest("http://" + target)
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: ./internet_test <config_file>")
		return
	}

	configFile := os.Args[1]
	config, err := loadConfig(configFile)
	if err != nil {
		fmt.Printf("Error loading config file: %s\n", err)
		return
	}

	fmt.Println("DNS Sunucuları test ediliyor...")
	runTests(config.DNSServers)

	fmt.Println("Arama Motorları test ediliyor...")
	runTests(config.SearchEngines)

	fmt.Println("Oyuncu Sunucuları test ediliyor...")
	runTests(config.GameServers)

	bufferbloatTest()
	calculateSQM(config.Bandwidth)

	fmt.Println("Tüm testler tamamlandı.")
}