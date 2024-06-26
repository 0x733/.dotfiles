use reqwest;
use serde_json::Value;
use std::fs::File;
use std::io::Write;
use std::process::Command;
use tempfile::NamedTempFile;

#[tokio::main]
async fn main() {
    // Kullanıcıdan BBK kodunu al
    println!("Lütfen sorgulamak istediğiniz BBK kodunu girin: ");
    let mut bbk_kod = String::new();
    std::io::stdin().read_line(&mut bbk_kod).expect("Failed to read line");
    let bbk_kod = bbk_kod.trim();

    // Sorguyu yap ve sonucu işle
    sorgula_ve_html_olustur(bbk_kod).await;
}

async fn sorgula_ve_html_olustur(bbk_kod: &str) {
    let sorgu_url = format!(
        "https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={}&datatype=checkAddress",
        bbk_kod
    );

    let yanit = reqwest::get(&sorgu_url).await;

    match yanit {
        Ok(response) => {
            if response.status().is_success() {
                let veri: Value = response.json().await.unwrap();

                // flexList'i ayrıştır
                if let Some(flex_list) = veri.get("flexList") {
                    // HTML oluşturma
                    let mut html_icerik = String::from(
                        r#"<!DOCTYPE html>
<html>
<head>
    <title>BBK Sorgulama Sonucu</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
    </style>
</head>
<body>
    <h1>BBK Sorgulama Sonucu</h1>
    <h2>flexList Verisi</h2>
    <table>
        <tr>
            <th>Anahtar</th>
            <th>Değer</th>
        </tr>
"#,
                    );

                    for item in flex_list.as_array().unwrap() {
                        for (key, value) in item.as_object().unwrap() {
                            html_icerik.push_str(&format!(
                                "<tr><td>{}</td><td>{}</td></tr>",
                                key, value
                            ));
                        }
                    }

                    html_icerik.push_str(
                        r#"
    </table>
</body>
</html>
"#,
                    );

                    // Geçici HTML dosyası oluştur ve yaz
                    let mut gecici_dosya = NamedTempFile::new().expect("Failed to create temp file");
                    gecici_dosya
                        .write_all(html_icerik.as_bytes())
                        .expect("Failed to write to temp file");

                    // HTML dosyasını tarayıcıda aç
                    let dosya_yolu = gecici_dosya.path().to_str().unwrap();
                    if webbrowser::open(dosya_yolu).is_err() {
                        println!("Failed to open the file in the default web browser.");
                    }
                }
            } else {
                println!("Sorgulama başarısız oldu. Lütfen BBK kodunu kontrol edin veya daha sonra tekrar deneyin.");
            }
        }
        Err(e) => {
            println!("HTTP isteği başarısız oldu: {}", e);
        }
    }
}