package main

import (
	"encoding/json"
	"fmt"
	"golang.org/x/net/html"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

const bbk = "0000000000"
const url = "https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod=" + bbk + "&datatype=checkAddress"

func checkPortStatus() bool {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("İstek hatası:", err)
		return false
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Body okuma hatası:", err)
		return false
	}

	var data map[string]interface{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		fmt.Println("JSON ayrıştırma hatası:", err)
		return false
	}

	portValue := data["6"].(map[string]interface{})["flexList"].(map[string]interface{})["flexList"].([]interface{})[2].(map[string]interface{})["value"].(string)
	errorCode := data["6"].(map[string]interface{})["hataKod"].(string)
	message := data["6"].(map[string]interface{})["hataMesaj"].(string)

	portStatus := "YOK"
	if portValue == "1" {
		portStatus = "VAR"
	}

	currentTime := time.Now().Format("2006-01-02 15:04:05")
	logMessage := fmt.Sprintf("[%s] Port Durumu: %s, Hata Kodu: %s, Mesaj: %s", currentTime, portStatus, errorCode, message)
	fmt.Println(logMessage)

	// JSON verisini HTML formatına dönüştür
	jsonHTML := `<html><body><pre>` + string(body) + `</pre></body></html>`

	// HTML dosyasını kaydet
	filename := fmt.Sprintf("port_status_%s.html", currentTime)
	err = ioutil.WriteFile(filename, []byte(jsonHTML), 0644)
	if err != nil {
		fmt.Println("HTML dosyası yazma hatası:", err)
		return false
	}
	fmt.Println("HTML dosyası kaydedildi:", filename)

	return portValue == "1"
}

func main() {
	for {
		if checkPortStatus() {
			break // Doğru çıktıyı verdiğinde döngüyü sonlandır
		}
		time.Sleep(1 * time.Second) // Her saniye kontrol et
	}

	fmt.Println("Program sonlandı.")
}