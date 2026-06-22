import requests
from bs4 import BeautifulSoup
import re
import os

OUTPUT_FILE = "docs/ferencvaros.ics"

MONTH_MAP = {
    "január": "01", "február": "02", "március": "03",
    "április": "04", "május": "05", "június": "06",
    "július": "07", "augusztus": "08", "szeptember": "09",
    "október": "10", "november": "11", "december": "12"
}

def parse_date(text):
    m = re.search(
        r"(202\d)\.\s*(január|február|március|április|május|június|július|augusztus|szeptember|október|november|december)\s+(\d{1,2})\.",
        text
    )
    if m:
        year, month_hu, day = m.group(1), m.group(2), m.group(3).zfill(2)
        return f"{year}-{MONTH_MAP[month_hu]}-{day}"
    return None

def parse_time(text):
    m = re.search(r"\b(\d{1,2}):(\d{2})\b", text)
    if m:
        return f"{int(m.group(1)):02d}:{m.group(2)}"
    return None

def fetch_all_matches():
    matches = []
    page = 1

    while True:
        url = f"https://www.fradi.hu/labdarugas/elso-csapat/esemenyek?page={page}"
        print(f"Oldal: {url}")
        try:
            r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text("\n")
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            found = []
            i = 0
            while i < len(lines):
                date = parse_date(lines[i])
                if date:
                    # Az időpont ugyanabban a sorban vagy közvetlenül utána
                    time = parse_time(lines[i])
                    
                    # Következő sorokból kiszedünk mindent amit tudunk
                    competition = ""
                    location = ""
                    home = ""
                    away = ""

                    # Nézzük a következő ~8 sort
                    window = lines[i+1:i+9] if i+9 < len(lines) else lines[i+1:]
                    
                    for line in window:
                        # Időpont ha még nincs
                        if not time:
                            time = parse_time(line)
                        
                        # Versenysorozat azonosítása
                        if any(k in line for k in ["Liga", "Kupa", "UEFA", "felkészülési", "Konferencia"]):
                            if not competition:
                                competition = line
                        
                        # Helyszín: "Város, Stadionnév" mintázat
                        if re.match(r"^[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+,\s+.+", line) and not location:
                            location = line

                        # Csapatnevek: FTC vagy ismert csapat
                        if line == "FTC":
                            if not home and not away:
                                home = "Ferencvárosi TC"
                            elif home and not away:
                                away = "Ferencvárosi TC"
                        elif line not in ["", competition, location] and \
                             not parse_date(line) and \
                             not parse_time(line) and \
                             not any(k in line for k in ["Liga", "Kupa", "UEFA", "felkészülési", "Konferencia", "Következő", "Előző", "Szűr", "Összes", "Sportág", "Szakosztály", "Verseny"]) and \
                             not re.match(r"^\d+$", line) and \
                             len(line) > 2 and len(line) < 60:
                            if not home:
                                home = line
                            elif not away and line != home:
                                away = line

                    # FTC mindig szerepeljen
                    if home and not away:
                        away = "Ferencvárosi TC"
                    if away and not home:
                        home = "Ferencvárosi TC"
                    if not home and not away:
                        home = "Ferencvárosi TC"
                        away = "?"

                    # Normalizálás: ha mindkét csapat FTC, skip
                    if home == away == "Ferencvárosi TC":
                        i += 1
                        continue

                    match = {
                        "date": date,
                        "time": time or "18:00",
                        "home": home,
                        "away": away,
                        "location": location,
                        "competition": competition,
                    }
                    found.append(match)
                    i += 8  # ugrás a következő mérkőzésre
                    continue
                i += 1

            if not found:
                print(f"  Nincs több mérkőzés, leállás.")
                break

            print(f"  {len(found)} mérkőzés találva")
            matches.extend(found)

            # Következő oldal ellenőrzése
            next_btn = soup.find("a", string=re.compile(r"Következő", re.I))
            if not next_btn:
                break
            page += 1

        except Exception as e:
            print(f"Hiba: {e}")
            break

    # Deduplikálás dátum + csapatok alapján
    seen = set()
    unique = []
    for m in matches:
        key = (m["date"], m["home"], m["away"])
        if key not in seen:
            seen.add(key)
            unique.append(m)

    unique.sort(key=lambda x: (x["date"], x["time"]))
    return unique


def generate_ics(matches):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Ferencvárosi TC 2026/27//HU",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Ferencvárosi TC 2026/27",
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

    for i, m in enumerate(matches):
        date_str = m["date"].replace("-", "")
        h, mi = m["time"].split(":")
        end_h = (int(h) + 2) % 24
        uid = f"fradi-{m['date']}-{i}@ftc"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Budapest:{date_str}T{int(h):02d}{mi}00",
            f"DTEND;TZID=Europe/Budapest:{date_str}T{end_h:02d}{mi}00",
            f"SUMMARY:{m['home']} – {m['away']}",
            f"LOCATION:{m.get('location', '')}",
            f"DESCRIPTION:{m.get('competition', '')}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    print("Mérkőzések lekérése...")
    matches = fetch_all_matches()
    print(f"\nÖsszesen {len(matches)} mérkőzés:")
    for m in matches:
        print(f"  {m['date']} {m['time']} | {m['home']} – {m['away']} | {m['competition']} | {m['location']}")
    ics = generate_ics(matches)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ics)
    print(f"\nKész! {OUTPUT_FILE}")
