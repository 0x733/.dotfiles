use reqwest;
use serde::Deserialize;
use std::collections::HashMap;
use chrono::Local;

#[derive(Deserialize)]
struct SpeedTestResult {
    download: f64,
    upload: f64,
    ping: f64,
}

async fn hiz_testi_yap() -> Result<(f64, f64, f64), Box<dyn std::error::Error>> {
    let response = reqwest::get("https://www.speedtest.net/api/js/servers?engine=js")
        .await?
        .json::<Vec<HashMap<String, String>>>()
        .await?;

    // Hız testi yapmak için ilk sunucuyu seçiyoruz (gerçek bir uygulamada daha iyi seçim yapılabilir)
    let server = &response[0];
    let url = &server["url"];

    // Hız testi API'sine istek gönderiyoruz
    let response = reqwest::get(url).await?;
    let result: SpeedTestResult = response.json().await?;

    Ok((result.download / 1_000_000.0, result.upload / 1_000_000.0, result.ping))
}

fn hiz_testi_sonuclarini_goster(indirme_hizi_mbps: f64, yukleme_hizi_mbps: f64) -> HashMap<String, HashMap<String, HashMap<String, String>>> {
    let indirme_hizi_kbps = indirme_hizi_mbps * 1_000.0;
    let yukleme_hizi_kbps = yukleme_hizi_mbps * 1_000.0;

    let mut sonuclar = HashMap::new();
    let mut indirme_hizi = HashMap::new();
    let mut yukleme_hizi = HashMap::new();
    let mut azaltılmış_indirme = HashMap::new();
    let mut artırılmış_indirme = HashMap::new();
    let mut azaltılmış_yukleme = HashMap::new();
    let mut artırılmış_yukleme = HashMap::new();

    for yuzde in (80..=90).step_by(5) {
        azaltılmış_indirme.insert(format!("{}%", yuzde), format!("{:.2f} Mbps", indirme_hizi_mbps * (yuzde as f64 / 100.0)));
        artırılmış_indirme.insert(format!("{}%", yuzde), format!("{:.2f} Mbps", indirme_hizi_mbps * ((100 + yuzde) as f64 / 100.0)));
        azaltılmış_indirme.insert(format!("{}% kbps", yuzde), format!("{:.2f} kbps", indirme_hizi_kbps * (yuzde as f64 / 100.0)));
        artırılmış_indirme.insert(format!("{}% kbps", yuzde), format!("{:.2f} kbps", indirme_hizi_kbps * ((100 + yuzde) as f64 / 100.0)));

        azaltılmış_yukleme.insert(format!("{}%", yuzde), format!("{:.2f} Mbps", yukleme_hizi_mbps * (yuzde as f64 / 100.0)));
        artırılmış_yukleme.insert(format!("{}%", yuzde), format!("{:.2f} Mbps", yukleme_hizi_mbps * ((100 + yuzde) as f64 / 100.0)));
        azaltılmış_yukleme.insert(format!("{}% kbps", yuzde), format!("{:.2f} kbps", yukleme_hizi_kbps * (yuzde as f64 / 100.0)));
        artırılmış_yukleme.insert(format!("{}% kbps", yuzde), format!("{:.2f} kbps", yukleme_hizi_kbps * ((100 + yuzde) as f64 / 100.0)));
    }

    indirme_hizi.insert("Azaltılmış".to_string(), azaltılmış_indirme);
    indirme_hizi.insert("Artırılmış".to_string(), artırılmış_indirme);
    yukleme_hizi.insert("Azaltılmış".to_string(), azaltılmış_yukleme);
    yukleme_hizi.insert("Artırılmış".to_string(), artırılmış_yukleme);

    sonuclar.insert("İndirme Hızı".to_string(), indirme_hizi);
    sonuclar.insert("Yükleme Hızı".to_string(), yukleme_hizi);

    sonuclar
}

#[tokio::main]
async fn main() {
    let baslangic_zamani = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
    println!("Test başladı: {}", baslangic_zamani);

    match hiz_testi_yap().await {
        Ok((indirme_hizi_mbps, yukleme_hizi_mbps, gecikme)) => {
            let mut hiz_testi_sonuclari = HashMap::new();

            hiz_testi_sonuclari.insert("İndirme Hızı".to_string(), format!("{:.2f} Mbps", indirme_hizi_mbps));
            hiz_testi_sonuclari.insert("Yükleme Hızı".to_string(), format!("{:.2f} Mbps", yukleme_hizi_mbps));
            hiz_testi_sonuclari.insert("Gecikme".to_string(), format!("{:.2f} ms", gecikme));
            
            let sonuclar = hiz_testi_sonuclarini_goster(indirme_hizi_mbps, yukleme_hizi_mbps);
            hiz_testi_sonuclari.extend(sonuclar);

            println!("{}", serde_json::to_string_pretty(&hiz_testi_sonuclari).unwrap());
        }
        Err(e) => {
            eprintln!("Hız testi başarısız oldu: {}", e);
        }
    }

    let bitis_zamani = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
    println!("Test bitti: {}", bitis_zamani);
}