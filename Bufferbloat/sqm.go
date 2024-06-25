package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "math"
    "os"
    "os/exec"
    "sort"
    "strconv"
    "strings"
    "time"
)

// SpeedtestResult speedtest-cli çıktısını tutar
type SpeedtestResult struct {
    Download float64 `json:"download"`
    Upload   float64 `json:"upload"`
    Ping     float64 `json:"ping"`
    Server   struct {
        ID   int    `json:"id"`
        Name string `json:"name"`
        Host string `json:"host"`
    } `json:"server"`
    Jitter      float64 `json:"jitter,omitempty"`
    PacketLoss float64 `json:"packetLoss,omitempty"`
}

// ServerInfo speedtest sunucu bilgilerini tutar
type ServerInfo struct {
    ID       int
    Sponsor  string
    Name     string
    Country  string
    Distance string
    Latency  int
}

func runSpeedtest(serverID *int) (*SpeedtestResult, error) {
    args := []string{"--json"}
    if serverID != nil {
        args = append(args, "--server", strconv.Itoa(*serverID))
    }
    cmd := exec.Command("speedtest-cli", args...)
    output, err := cmd.Output()
    if err != nil {
        return nil, fmt.Errorf("speedtest hatası: %v", err)
    }

    var result SpeedtestResult
    err = json.Unmarshal(output, &result)
    if err != nil {
        return nil, fmt.Errorf("JSON ayrıştırma hatası: %v", err)
    }

    return &result, nil
}

func getServerList() ([]ServerInfo, error) {
    cmd := exec.Command("speedtest-cli", "--list")
    output, err := cmd.Output()
    if err != nil {
        return nil, fmt.Errorf("sunucu listesi alınamadı: %v", err)
    }

    var servers []ServerInfo
    scanner := bufio.NewScanner(strings.NewReader(string(output)))
    for scanner.Scan() {
        line := scanner.Text()
        if strings.HasPrefix(line, "  ") {
            fields := strings.Fields(line)
            if len(fields) >= 6 {
                id, _ := strconv.Atoi(fields[0])
                latency, _ := strconv.Atoi(fields[5])
                servers = append(servers, ServerInfo{
                    ID:       id,
                    Sponsor:  fields[1],
                    Name:     fields[2],
                    Country:  fields[3],
                    Distance: fields[4],
                    Latency:  latency,
                })
            }
        }
    }
    return servers, nil
}

func chooseServer() (*int, error) {
    servers, err := getServerList()
    if err != nil {
        return nil, err
    }

    fmt.Println("Sunucu seçmek ister misiniz? (e/h):")
    reader := bufio.NewReader(os.Stdin)
    input, _ := reader.ReadString('\n')
    input = strings.TrimSpace(input)

    if input == "e" {
        for i, server := range servers {
            fmt.Printf("%d. %s (%s) - %s\n", i+1, server.Name, server.Sponsor, server.Country)
        }
        fmt.Print("Sunucu numarasını girin: ")
        input, _ := reader.ReadString('\n')
        input = strings.TrimSpace(input)
        serverIndex, _ := strconv.Atoi(input)
        if serverIndex > 0 && serverIndex <= len(servers) {
            return &servers[serverIndex-1].ID, nil
        } else {
            return nil, fmt.Errorf("geçersiz sunucu seçimi")
        }
    } else {
        fmt.Println("En iyi sunucu otomatik olarak seçiliyor...")
        return findBestServer(servers)
    }
}

func findBestServer(servers []ServerInfo) (*int, error) {
    sort.Slice(servers, func(i, j int) bool {
        return servers[i].Latency < servers[j].Latency
    })
    if len(servers) > 0 {
        return &servers[0].ID, nil
    }
    return nil, fmt.Errorf("sunucu bulunamadı")
}

func calculateJitter(host string) (float64, error) {
    cmd := exec.Command("ping", "-c", "10", host)
    output, err := cmd.Output()
    if err != nil {
        return 0, fmt.Errorf("ping hatası: %v", err)
    }

    var times []float64
    for _, line := range strings.Split(string(output), "\n") {
        if strings.Contains(line, "time=") {
            fields := strings.Fields(line)
            for _, field := range fields {
                if strings.HasPrefix(field, "time=") {
                    timeStr := strings.TrimPrefix(field, "time=")
                    timeStr = strings.Split(timeStr, " ")[0]
                    time, _ := strconv.ParseFloat(timeStr, 64)
                    times = append(times, time)
                    break
                }
            }
        }
    }

    if len(times) > 1 {
        var sum, sumSquares float64
        for _, t := range times {
            sum += t
            sumSquares += t * t
        }
        mean := sum / float64(len(times))
        variance := sumSquares/float64(len(times)) - mean*mean
        return math.Sqrt(variance), nil
    }
    return 0, fmt.Errorf("yeterli ping yanıtı alınamadı")
}

func calculatePacketLoss(host string) (float64, error) {
    cmd := exec.Command("ping", "-c", "10", host)
    output, err := cmd.Output()
    if err != nil {
        return 0, fmt.Errorf("ping hatası: %v", err)
    }
    for _, line := range strings.Split(string(output), "\n") {
        if strings.Contains(line, "packet loss") {
            fields := strings.Fields(line)
            for i, field := range fields {
                if field == "packet" && i < len(fields)-1 && fields[i+1] == "loss" {
                    lossStr := strings.TrimSuffix(fields[i+2], "%")
                    loss, _ := strconv.ParseFloat(lossStr, 64)
                    return loss, nil
                }
            }
        }
    }
    return 0, nil
}

func analyzeResults(result *SpeedtestResult) {
    // ... (Python örneğindekiyle aynı)
}

func saveResults(result *SpeedtestResult, filename string) error {
    // ... (Python örneğindekiyle aynı)
}

func main() {
    serverID, err := chooseServer()
    if err != nil {
        fmt.Println("Hata:", err)
        return
    }

    result, err := runSpeedtest(serverID)
    if err != nil {
        fmt.Println("Hata:", err)
        return
    }

    analyzeResults(result)

    jitter, err := calculateJitter(result.Server.Host)
    if err != nil {
        fmt.Println("Jitter hesaplanamadı:", err)
    } else {
        result.Jitter = jitter
        fmt.Printf("Jitter: %.2f ms\n", jitter)
    }

    packetLoss, err := calculatePacketLoss(result.Server.Host)
    if err != nil {
        fmt.Println("Paket kaybı hesaplanamadı:", err)
    } else {
        result.PacketLoss = packetLoss
        fmt.Printf("Paket Kaybı: %.2f%%\n", packetLoss)
    }

    err = saveResults(result, "hiz_testi_sonuclari.json")
    if err != nil {
        fmt.Println("Hata:", err)
    }
}