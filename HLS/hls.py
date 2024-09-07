import scrapy
import re
import subprocess

class XHRVideoSpider(scrapy.Spider):
    name = "xhr_video_ffmpeg"

    def __init__(self, user_url=None, *args, **kwargs):
        super(XHRVideoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [user_url]  # Kullanıcıdan gelen URL'yi başlangıç URL'si yapıyoruz

    # Playwright middleware'i kullanarak istek gönder
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",  # chromium, firefox veya webkit seçilebilir
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    async def parse(self, response):
        """
        Sayfadaki tüm XHR isteklerini kontrol eder ve video bağlantılarını yakalar.
        """
        page = response.meta["playwright_page"]

        # Sayfadaki ağ (network) isteklerini dinlemek için bir işlev ekliyoruz
        video_urls = []

        async def intercept_request(route, request):
            """XHR veya diğer ağ isteklerini kontrol et"""
            video_live_regex = re.compile(r"(https?://[^\s]+(?:\.mp4|\.m3u8|\.mpd)|https?://[^\s]+(?:hls|live|video)[^\s]*)")

            if request.resource_type == "xhr":
                # Yalnızca XHR (AJAX) isteklerini kontrol et
                if video_live_regex.match(request.url):
                    print(f"Found media URL: {request.url}")
                    video_urls.append(request.url)

            await route.continue_()

        # Ağ trafiğini dinle
        await page.route("**/*", intercept_request)

        # Sayfayı yükle
        await page.goto(response.url)

        # Dinamik olarak yüklenen XHR isteklerini bekleyin
        await page.wait_for_timeout(10000)  # 10 saniye beklemek isteklere göre artırılabilir

        # Bulunan video URL'lerini ve codec bilgilerini yield ile dışarı çıkar ve bitrate analizi yap
        for video_url in video_urls:
            print(f"URL Bulundu: {video_url}")
            yield {
                "video_url": video_url,
                "bitrate_analysis": self.analyze_bitrate(video_url)
            }

        await page.close()

    def analyze_bitrate(self, video_url):
        # FFmpeg kullanarak bitrate analizi
        try:
            # FFmpeg komutu: video URL'sini alır ve bitrate bilgisini gösterir
            command = ["ffmpeg", "-i", video_url, "-f", "null", "-"]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
            # FFmpeg'in çıktısındaki bitrate bilgisini ayıkla
            bitrate_info = re.findall(r'bitrate:\s*(\d+\s*kb/s)', result.stderr)
            if bitrate_info:
                return f"Bitrate bilgisi: {bitrate_info[0]}"
            else:
                return "Bitrate bilgisi bulunamadı."
        except Exception as e:
            return f"Bitrate analizinde hata oluştu: {str(e)}"

# Scrapy projesini çalıştırmak için aşağıdaki kodu kullanın
from scrapy.crawler import CrawlerProcess

if __name__ == "__main__":
    # Kullanıcıdan URL al
    user_url = input("Lütfen bir URL girin: ")

    # Scrapy örneğini başlat
    process = CrawlerProcess()
    process.crawl(XHRVideoSpider, user_url=user_url)
    process.start()