import requests
from bs4 import BeautifulSoup
import re
import os

OUTPUT_FILE = "docs/ferencvaros.ics"

# Ferencváros mérkőzései – 2026/27 OTP Bank Liga
# Forrás: adatbank.mlsz.hu
MATCHES = [
    {"round": 1,  "date": "2026-07-25", "home": "PAKSI FC",                  "away": "FERENCVÁROSI TC",         "location": "Paksi FC Stadion",                "match_id": "2186378"},
    {"round": 2,  "date": "2026-08-01", "home": "FERENCVÁROSI TC",           "away": "MTK BUDAPEST",            "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 3,  "date": "2026-08-08", "home": "VASAS FC",                  "away": "FERENCVÁROSI TC",         "location": "Illovszky Rudolf Stadion",        "match_id": ""},
    {"round": 4,  "date": "2026-08-15", "home": "FERENCVÁROSI TC",           "away": "KISVÁRDA MASTER GOOD",    "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 5,  "date": "2026-08-22", "home": "ZTE FC",                    "away": "FERENCVÁROSI TC",         "location": "ZTE Aréna",                       "match_id": ""},
    {"round": 6,  "date": "2026-08-29", "home": "FERENCVÁROSI TC",           "away": "NYÍREGYHÁZA SPARTACUS FC","location": "Groupama Aréna",                  "match_id": ""},
    {"round": 7,  "date": "2026-09-05", "home": "KISPEST–HONVÉD FC",         "away": "FERENCVÁROSI TC",         "location": "Bozsik Aréna",                    "match_id": ""},
    {"round": 8,  "date": "2026-09-19", "home": "FERENCVÁROSI TC",           "away": "DVSC",                    "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 9,  "date": "2026-10-10", "home": "FERENCVÁROSI TC",           "away": "PUSKÁS AKADÉMIA FC",      "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 10, "date": "2026-10-17", "home": "ETO FC",                    "away": "FERENCVÁROSI TC",         "location": "ETO Stadion",                     "match_id": ""},
    {"round": 11, "date": "2026-10-24", "home": "FERENCVÁROSI TC",           "away": "ÚJPEST FC",               "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 12, "date": "2026-10-31", "home": "FERENCVÁROSI TC",           "away": "ZTE FC",                  "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 13, "date": "2026-11-07", "home": "NYÍREGYHÁZA SPARTACUS FC",  "away": "FERENCVÁROSI TC",         "location": "Nyíregyháza Városi Stadion",      "match_id": ""},
    {"round": 14, "date": "2026-11-21", "home": "FERENCVÁROSI TC",           "away": "VASAS FC",                "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 15, "date": "2026-11-28", "home": "MTK BUDAPEST",              "away": "FERENCVÁROSI TC",         "location": "Új Hidegkuti Nándor Stadion",     "match_id": ""},
    {"round": 16, "date": "2026-12-05", "home": "FERENCVÁROSI TC",           "away": "KISPEST–HONVÉD FC",       "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 17, "date": "2026-12-12", "home": "KISVÁRDA MASTER GOOD",      "away": "FERENCVÁROSI TC",         "location": "Kisvárdai Várkerti Stadion",      "match_id": ""},
    {"round": 18, "date": "2026-12-19", "home": "FERENCVÁROSI TC",           "away": "PAKSI FC",                "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 19, "date": "2027-01-30", "home": "FERENCVÁROSI TC",           "away": "ETO FC",                  "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 20, "date": "2027-02-06", "home": "DVSC",                      "away": "FERENCVÁROSI TC",         "location": "Debreceni Nagyerdei Stadion",     "match_id": ""},
    {"round": 21, "date": "2027-02-13", "home": "FERENCVÁROSI TC",           "away": "KISPEST–HONVÉD FC",       "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 22, "date": "2027-02-20", "home": "PUSKÁS AKADÉMIA FC",        "away": "FERENCVÁROSI TC",         "location": "Puskás Akadémia Pancho Aréna",   "match_id": ""},
    {"round": 23, "date": "2027-02-27", "home": "FERENCVÁROSI TC",           "away": "NYÍREGYHÁZA SPARTACUS FC","location": "Groupama Aréna",                  "match_id": ""},
    {"round": 24, "date": "2027-03-06", "home": "ÚJPEST FC",                 "away": "FERENCVÁROSI TC",         "location": "Szusza Ferenc Stadion",           "match_id": ""},
    {"round": 25, "date": "2027-03-13", "home": "FERENCVÁROSI TC",           "away": "MTK BUDAPEST",            "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 26, "date": "2027-03-20", "home": "FERENCVÁROSI TC",           "away": "VASAS FC",                "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 27, "date": "2027-04-03", "home": "ZTE FC",                    "away": "FERENCVÁROSI TC",         "location": "ZTE Aréna",                       "match_id": ""},
    {"round": 28, "date": "2027-04-10", "home": "FERENCVÁROSI TC",           "away": "DVSC",                    "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 29, "date": "2027-04-17", "home": "KISVÁRDA MASTER GOOD",      "away": "FERENCVÁROSI TC",         "location": "Kisvárdai Várkerti Stadion",      "match_id": ""},
    {"round": 30, "date": "2027-04-24", "home": "FERENCVÁROSI TC",           "away": "ETO FC",                  "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 31, "date": "2027-05-01", "home": "PUSKÁS AKADÉMIA FC",        "away": "FERENCVÁROSI TC",         "location": "Puskás Akadémia Pancho Aréna",   "match_id": ""},
    {"round": 32, "date": "2027-05-15", "home": "FERENCVÁROSI TC",           "away": "ÚJPEST FC",               "location": "Groupama Aréna",                  "match_id": ""},
    {"round": 33, "date": "2027-05-22", "home": "FERENCVÁROSI TC",           "away": "PAKSI FC",                "location": "Groupama Aréna",                  "match_id": ""},
]

def fetch_kickoff_time(match_id):
    """Pontos kezdési időpont lekérése az MLSZ-ről ha elérhető."""
    if not match_id:
        return "18:00"
    try:
        url = f"https://adatbank.mlsz.hu/match/{match_id}.html"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        time_match = re.search(r"\b(\d{2}:\d{2})\b", soup.get_text())
        if time_match:
            return time_match.group(1)
    except:
        pass
    return "18:00"

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
        time_str = m.get("time", "18:00").replace(":", "")
        uid = f"fradi-{m['date']}-{m['round']}@mlsz"
        summary = f"{m['home']} – {m['away']}"
        description = f"OTP Bank Liga – {m['round']}. forduló"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Budapest:{date_str}T{time_str}00",
            f"DTEND;TZID=Europe/Budapest:{date_str}T{int(time_str[:2])+2:02d}{time_str[2:]}00",
            f"SUMMARY:{summary}",
            f"LOCATION:{m['location']}",
            f"DESCRIPTION:{description}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    print("ICS generálása...")
    ics = generate_ics(MATCHES)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ics)
    print(f"Kész! {len(MATCHES)} mérkőzés beírva.")
