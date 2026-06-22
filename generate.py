import requests
from bs4 import BeautifulSoup
import re
import os

OUTPUT_FILE = "docs/ferencvaros.ics"
BASE_URL = "https://www.fradi.hu/labdarugas/elso-csapat/esemenyek?page={}"

def fetch_all_matches():
    matches = []
    page = 1

    while True:
        url = BASE_URL.format(page)
        print(f"Oldal lekérése: {url}")
        try:
            r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")

            # Mérkőzés blokkok keresése
            blocks = soup.select("div.event-list-item, div.match-item, article, div.esemenyek-item")
            
            # Ha nem találjuk a specifikus osztályt, próbáljuk másképp
            if not blocks:
                # Dátum + csapatnév + helyszín mintázat alapján
                blocks = soup.find_all("div", class_=re.compile(r"event|match|meccs|sorso", re.I))

            # Szöveg alapú kinyerés ha a fenti nem működik
            text = soup.get_text("\n", strip=True)
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            found_on_page = []
            i = 0
            while i < len(lines):
                # Dátum keresése: "2026. július 9." vagy "2026. augusztus 1."
                date_match = re.match(
                    r"(202[67])\. (január|február|március|április|május|június|július|augusztus|szeptember|október|november|december)\s+(\d{1,2})\.",
                    lines[i]
                )
                if date_match:
                    year = date_match.group(1)
                    month_hu = date_match.group(2)
                    day = date_match.group(3).zfill(2)
                    
                    month_map = {
                        "január": "01", "február": "02", "március": "03",
                        "április": "04", "május": "05", "június": "06",
                        "július": "07", "augusztus": "08", "szeptember": "09",
                        "október": "10", "november": "11", "december": "12"
                    }
                    month = month_map.get(month_hu, "01")
                    date_str = f"{year}-{month}-{day}"

                    # Időpont keresése a következő sorokban
                    time_str = "18:00"
                    competition = ""
                    location = ""
                    home = ""
                    away = ""

                    for j in range(i, min(i + 10, len(lines))):
                        # Időpont
                        t = re.search(r"\b(\d{1,2}:\d{2})\b", lines[j])
                        if t and time_str == "18:00":
                            time_str = t.group(1)
                        # Versenysorozat és helyszín (pl. "UEFA Európa LigaNovi Sad, Stadion")
                        if "Liga" in lines[j] or "Kupa" in lines[j] or "UEFA" in lines[j] or "felkészülési" in lines[j].lower():
                            # Szétválasztjuk a versenysorozatot és helyszínt
                            comp_loc = re.split(r"(?<=[a-z])(?=[A-Z])", lines[j], maxsplit=1)
                            competition = comp_loc[0].strip()
                            if len(comp_loc) > 1:
                                location = comp_loc[1].strip()
                        # FTC és ellenfél keresése
                        if "FTC" in lines[j] and not home:
                            # Keressük az ellenfelet a szomszéd sorokban
                            for k in range(j-2, j+3):
                                if 0 <= k < len(lines) and k != j:
                                    if lines[k] not in ["FTC", ""] and not re.match(r"202[67]", lines[k]) and len(lines[k]) > 2:
                                        opponent = lines[k]
                                        # Eldöntjük ki a hazai
                                        if k < j:
                                            home = opponent
                                            away = "Ferencvárosi TC"
                                        else:
                                            home = "Ferencvárosi TC"
                                            away = opponent
                                        break

                    if home and away and date_str:
                        match = {
                            "date": date_str,
                            "time": time_str,
                            "home": home,
                            "away": away,
                            "location": location,
                            "competition": competition,
                        }
                        # Duplikátum ellenőrzés
                        if match not in found_on_page:
                            found_on_page.append(match)

                i += 1

            if not found_on_page:
                print(f"Nem találtunk mérkőzést a(z) {page}. oldalon, leállás.")
                break

            matches.extend(found_on_page)
            print(f"  {len(found_on_page)} mérkőzés találva")

            # Van-e következő oldal?
            next_link = soup.find("a", string=re.compile("Következő|Next", re.I))
            if not next_link:
                break
            page += 1

        except Exception as e:
            print(f"Hiba a(z) {page}. oldalnál: {e}")
            break

    # Duplikátumok eltávolítása és rendezés
    seen = set()
    unique = []
    for m in matches:
        key = (m["date"], m["home"], m["away"])
        if key not in seen:
            seen.add(key)
            unique.append(m)

    unique.sort(key=lambda x: x["date"])
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
        time_parts = m.get("time", "18:00").split(":")
        hour = int(time_parts[0])
        minute = time_parts[1] if len(time_parts) > 1 else "00"
        end_hour = (hour + 2) % 24

        uid = f"fradi-{m['date']}-{i}@ftc"
        summary = f"{m['home']} – {m['away']}"
        description = m.get("competition", "Ferencvárosi TC mérkőzés")

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Budapest:{date_str}T{hour:02d}{minute}00",
            f"DTEND;TZID=Europe/Budapest:{date_str}T{end_hour:02d}{minute}00",
            f"SUMMARY:{summary}",
            f"LOCATION:{m.get('location', '')}",
            f"DESCRIPTION:{description}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    print("Mérkőzések lekérése a fradi.hu-ról...")
    matches = fetch_all_matches()
    print(f"\nÖsszesen {len(matches)} mérkőzés találva")
    for m in matches:
        print(f"  {m['date']} {m['time']} – {m['home']} vs {m['away']} ({m['competition']})")
    ics = generate_ics(matches)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ics)
    print(f"\nKész! ICS fájl mentve: {OUTPUT_FILE}")
