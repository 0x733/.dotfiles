import m3u8
import requests
from bs4 import BeautifulSoup
import logging
import os
import subprocess
from tqdm import tqdm
import time

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AdvancedHLSParser:
    def __init__(self, url):
        self.url = url
        self.playlist_url = None
        self.playlist = None
        self.live = False

    def find_hls_url(self):
        """
        Web sayfasında HLS URL'sini bulur.
        """
        logging.info(f"Searching for HLS URL in webpage: {self.url}")
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            # Sayfa içeriğini analiz ediyoruz
            soup = BeautifulSoup(response.text, 'html.parser')

            # .m3u8 uzantılı linkleri buluyoruz
            hls_links = [link.get('src') for link in soup.find_all('source') if link.get('src') and '.m3u8' in link.get('src')]
            if not hls_links:
                hls_links = [link.get('href') for link in soup.find_all('a') if link.get('href') and '.m3u8' in link.get('href')]

            if hls_links:
                self.playlist_url = hls_links[0]
                logging.info(f"Found HLS URL: {self.playlist_url}")
            else:
                logging.warning("No HLS playlist URL found in the webpage.")
        except requests.RequestException as e:
            logging.error(f"Error fetching webpage: {e}")
            return False
        return True

    def download_playlist(self):
        """
        Playlist'i indirir ve m3u8 formatında işler.
        """
        if not self.playlist_url:
            logging.error("HLS playlist URL is not available. Please find the HLS URL first.")
            return False

        logging.info(f"Downloading HLS playlist from: {self.playlist_url}")
        try:
            response = requests.get(self.playlist_url)
            response.raise_for_status()
            self.playlist = m3u8.loads(response.text)
        except requests.RequestException as e:
            logging.error(f"Error downloading playlist: {e}")
            return False
        return True

    def parse_media_playlist(self):
        """
        HLS playlist'indeki segmentleri analiz eder.
        """
        if not self.playlist.is_variant:
            logging.info(f"Found {len(self.playlist.segments)} media segments.")
            for i, segment in enumerate(self.playlist.segments):
                logging.info(f"Segment {i+1}:")
                logging.info(f"  - URI: {segment.uri}")
                logging.info(f"  - Duration: {segment.duration} seconds")
                if segment.key:
                    logging.info(f"  - Encrypted with: {segment.key.method}")
                    logging.info(f"  - Key URI: {segment.key.uri}")
        else:
            logging.warning("This is a master playlist. To parse media segments, choose a variant playlist.")

    def download_segments(self, download_folder="segments"):
        """
        Medya segmentlerini indirir ve dosya olarak kaydeder.
        """
        if not self.playlist.is_variant:
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            logging.info(f"Downloading {len(self.playlist.segments)} segments to {download_folder}.")
            for i, segment in tqdm(enumerate(self.playlist.segments), total=len(self.playlist.segments)):
                segment_url = segment.uri
                segment_filename = os.path.join(download_folder, f"segment_{i+1}.ts")
                try:
                    with requests.get(segment_url, stream=True) as r:
                        r.raise_for_status()
                        with open(segment_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    logging.info(f"Downloaded: {segment_filename}")
                    
                    self.ask_to_play_segment(segment_filename)

                except requests.RequestException as e:
                    logging.error(f"Error downloading segment {segment_url}: {e}")
        else:
            logging.warning("Cannot download segments from a master playlist.")

    def ask_to_play_segment(self, segment_filename):
        """
        Kullanıcıya segmenti MPV ile oynatmak isteyip istemediğini sorar.
        """
        play = input(f"Do you want to play the segment {segment_filename} with MPV? (y/n): ").strip().lower()
        if play == 'y':
            self.play_with_mpv(segment_filename)
        else:
            logging.info(f"Skipping playback of {segment_filename}.")

    def play_with_mpv(self, segment_filename):
        """
        MPV ile segmenti oynatır.
        """
        try:
            logging.info(f"Playing segment {segment_filename} with MPV.")
            subprocess.run(['mpv', segment_filename], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error occurred while playing the segment with MPV: {e}")

    def parse_keys(self):
        """
        Playlist içindeki şifreleme anahtarlarını analiz eder.
        """
        if not self.playlist.is_variant and self.playlist.keys:
            logging.info("Found encryption keys:")
            for key in self.playlist.keys:
                logging.info(f"  - Method: {key.method}")
                logging.info(f"  - Key URI: {key.uri}")
                logging.info(f"  - IV: {key.iv}")
        else:
            logging.info("No encryption keys found or this is a master playlist.")

    def report_playlist(self):
        """
        Playlist'in toplam süresi, segment sayısı gibi bilgileri raporlar.
        """
        total_duration = sum(segment.duration for segment in self.playlist.segments)
        logging.info(f"Total Playlist Duration: {total_duration:.2f} seconds")
        logging.info(f"Number of Segments: {len(self.playlist.segments)}")


# Main fonksiyonu ile script'in çalışmasını başlatıyoruz
if __name__ == "__main__":
    webpage_url = input("Enter webpage URL to search for HLS stream: ")
    parser = AdvancedHLSParser(webpage_url)

    if parser.find_hls_url():
        if parser.download_playlist():
            parser.report_playlist()
            parser.parse_media_playlist()
            parser.parse_keys()

            # Segmentleri indir ve analiz et
            parser.download_segments()