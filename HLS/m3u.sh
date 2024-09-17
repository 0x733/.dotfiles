#!/bin/bash
OUTPUT_FILE="Filmler.m3u"
[[ ! -f "$OUTPUT_FILE" ]] && echo "#EXTM3U" > "$OUTPUT_FILE"
echo "Film adı:"; read film_name
echo "Film resmi URL'si:"; read film_logo
echo "Film video URL'si:"; read film_url
echo "Referrer URL'si:"; read referrer
referrer="${referrer%/}/"
echo -e "\n#EXTINF:-1 tvg-name=\"$film_name\" tvg-language=\"Turkish\" tvg-country=\"TR\" tvg-id=\"$film_name\" tvg-logo=\"$film_logo\" group-title=\"Filmler\",$film_name" >> "$OUTPUT_FILE"
echo "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)" >> "$OUTPUT_FILE"
echo "#EXTVLCOPT:http-referrer=$referrer" >> "$OUTPUT_FILE"
echo "$film_url" >> "$OUTPUT_FILE"
echo -e "\nFilm $film_name başarıyla Filmler.m3u dosyasına eklendi."