import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

MLSZ_URL = "https://adatbank.mlsz.hu/club/67/0/33586/{round}/328180.html"
OUTPUT_FILE = "docs/ferencvaros.ics"

def fetch_matches():
    matches = []
    for round_num in range(1, 34):
        url = MLSZ_URL.format(round=round_num)
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            # Mérkőzés adatok kinyerése
            date_tags = soup.find_all(string=re.compile(r"202[67]\. \d+\. \d+\."))
            location_tags = soup.select(".helyszin, .stadium, td")

            for tag in soup.find_all("div", class_=re.compile("meccs|match|sorso")):
                text = tag.get_text(" ", strip=True)
                date_match = re.search(r"(202[67])\. (\d+)\. (\d+)\.", text)
                if date_match:
                    year, month, day = date_match.groups()
                    # Keressük a helyszínt
                    location = ""
                    loc_tag = tag.find(string=re.compile("Stadion|Aréna|Pálya"))
                    if loc_tag:
                        location = loc_tag.strip()
                    
                    home = away = ""
                    teams = tag.find_all("a")
                    if len(teams) >= 2:
                        home = teams[0].get_text(strip=True)
                        away = teams[1].get_text(strip=True)
                    
                    if home and away:
                        matches.append({
                            "round": round_num,
                            "date": f"{year}-{int(month):02d}-{int(day):02d}",
                            "home": home,
                            "away": away,
                            "location": location
                        })
                        break
        except Exception as e:
            print(f"Hiba a {round_num}. fordulónál: {e}")
    
    return matches

def generate_ics(matches):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Ferencváros NB I 2026/27//HU",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Ferencváros NB I 2026/27",
        "X-WR-TIMEZONE:Europe/Budapest",
        "BEGIN:VTIMEZONE",
        "TZID:Europe/Budapest",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0200",
        "TZOFFSETTO:+0100",
        "TZNAME:CET",
        "DTSTART:19701025T030000",
        "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10",
        "END:STANDARD",
        "BEGIN:DAYLIGHT",
        "TZOFFSETFROM:+0100",
        "TZOFFSETTO:+0200",
        "TZNAME:CEST",
        "DTSTART:19700329T020000",
        "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3",
        "END:DAYLIGHT",
        "END:VTIMEZONE",
    ]

    for m in matches:
        date_str = m["date"].replace("-", "")
        uid = f"fradi-{m['date']}-{m['round']}@mlsz"
        summary = f"{m['home']} – {m['away']}"
        description = f"OTP Bank Liga – {m['round']}. forduló"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Budapest:{date_str}T180000",
            f"DTEND;TZID=Europe/Budapest:{date_str}T200000",
            f"SUMMARY:{summary}",
            f"LOCATION:{m['location']}",
            f"DESCRIPTION:{description}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)

if __name__ == "__main__":
    import os
    os.makedirs("docs", exist_ok=True)
    
    print("Adatok lekérése az MLSZ-ről...")
    matches = fetch_matches()
    print(f"{len(matches)} mérkőzés találva")
    
    ics = generate_ics(matches)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ics)
    print(f"ICS fájl generálva: {OUTPUT_FILE}")
