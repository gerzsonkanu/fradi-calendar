import requests
from bs4 import BeautifulSoup
import re
import os

OUTPUT_FILE = "docs/ferencvaros.ics"

# OTP Bank Liga 2026/27 – Ferencváros mérkőzései
MATCHES = [
    {"round": "1. forduló",  "date": "2026-07-25", "home": "Paksi FC",                 "away": "Ferencvárosi TC",        "location": "Paksi FC Stadion"},
    {"round": "2. forduló",  "date": "2026-08-01", "home": "Ferencvárosi TC",          "away": "MTK Budapest",           "location": "Groupama Aréna"},
    {"round": "3. forduló",  "date": "2026-08-08", "home": "Vasas FC",                 "away": "Ferencvárosi TC",        "location": "Illovszky Rudolf Stadion"},
    {"round": "4. forduló",  "date": "2026-08-15", "home": "Ferencvárosi TC",          "away": "Kisvárda Master Good",   "location": "Groupama Aréna"},
    {"round": "5. forduló",  "date": "2026-08-22", "home": "ZTE FC",                   "away": "Ferencvárosi TC",        "location": "ZTE Aréna"},
    {"round": "6. forduló",  "date": "2026-08-29", "home": "Ferencvárosi TC",          "away": "Nyíregyháza Spartacus",  "location": "Groupama Aréna"},
    {"round": "7. forduló",  "date": "2026-09-05", "home": "Kispest–Honvéd FC",        "away": "Ferencvárosi TC",        "location": "Bozsik Aréna"},
    {"round": "8. forduló",  "date": "2026-09-19", "home": "Ferencvárosi TC",          "away": "DVSC",                   "location": "Groupama Aréna"},
    {"round": "9. forduló",  "date": "2026-10-10", "home": "Ferencvárosi TC",          "away": "Puskás Akadémia FC",     "location": "Groupama Aréna"},
    {"round": "10. forduló", "date": "2026-10-17", "home": "ETO FC",                   "away": "Ferencvárosi TC",        "location": "ETO Stadion"},
    {"round": "11. forduló", "date": "2026-10-24", "home": "Ferencvárosi TC",          "away": "Újpest FC",              "location": "Groupama Aréna"},
    {"round": "12. forduló", "date": "2026-10-31", "home": "Ferencvárosi TC",          "away": "ZTE FC",                 "location": "Groupama Aréna"},
    {"round": "13. forduló", "date": "2026-11-07", "home": "Nyíregyháza Spartacus",    "away": "Ferencvárosi TC",        "location": "Nyíregyháza Városi Stadion"},
    {"round": "14. forduló", "date": "2026-11-21", "home": "Ferencvárosi TC",          "away": "Vasas FC",               "location": "Groupama Aréna"},
    {"round": "15. forduló", "date": "2026-11-28", "home": "MTK Budapest",             "away": "Ferencvárosi TC",        "location": "Új Hidegkuti Nándor Stadion"},
    {"round": "16. forduló", "date": "2026-12-05", "home": "Ferencvárosi TC",          "away": "Kispest–Honvéd FC",      "location": "Groupama Aréna"},
    {"round": "17. forduló", "date": "2026-12-12", "home": "Kisvárda Master Good",     "away": "Ferencvárosi TC",        "location": "Kisvárdai Várkerti Stadion"},
    {"round": "18. forduló", "date": "2026-12-19", "home": "Ferencvárosi TC",          "away": "Paksi FC",               "location": "Groupama Aréna"},
    {"round": "19. forduló", "date": "2027-01-30", "home": "Ferencvárosi TC",          "away": "ETO FC",                 "location": "Groupama Aréna"},
    {"round": "20. forduló", "date": "2027-02-06", "home": "DVSC",                     "away": "Ferencvárosi TC",        "location": "Debreceni Nagyerdei Stadion"},
    {"round": "21. forduló", "date": "2027-02-13", "home": "Ferencvárosi TC",          "away": "Kispest–Honvéd FC",      "location": "Groupama Aréna"},
    {"round": "22. forduló", "date": "2027-02-20", "home": "Puskás Akadémia FC",       "away": "Ferencvárosi TC",        "location": "Puskás Akadémia Pancho Aréna"},
    {"round": "23. forduló", "date": "2027-02-27", "home": "Ferencvárosi TC",          "away": "Nyíregyháza Spartacus",  "location": "Groupama Aréna"},
    {"round": "24. forduló", "date": "2027-03-06", "home": "Újpest FC",                "away": "Ferencvárosi TC",        "location": "Szusza Ferenc Stadion"},
    {"round": "25. forduló", "date": "2027-03-13", "home": "Ferencvárosi TC",          "away": "MTK Budapest",           "location": "Groupama Aréna"},
    {"round": "26. forduló", "date": "2027-03-20", "home": "Ferencvárosi TC",          "away": "Vasas FC",               "location": "Groupama Aréna"},
    {"round": "27. forduló", "date": "2027-04-03", "home": "ZTE FC",                   "away": "Ferencvárosi TC",        "location": "ZTE Aréna"},
    {"round": "28. forduló", "date": "2027-04-10", "home": "Ferencvárosi TC",          "away": "DVSC",                   "location": "Groupama Aréna"},
    {"round": "29. forduló", "date": "2027-04-17", "home": "Kisvárda Master Good",     "away": "Ferencvárosi TC",        "location": "Kisvárdai Várkerti Stadion"},
    {"round": "30. forduló", "date": "2027-04-24", "home": "Ferencvárosi TC",          "away": "ETO FC",                 "location": "Groupama Aréna"},
    {"round": "31. forduló", "date": "2027-05-01", "home": "Puskás Akadémia FC",       "away": "Ferencvárosi TC",        "location": "Puskás Akadémia Pancho Aréna"},
    {"round": "32. forduló", "date": "2027-05-15", "home": "Ferencvárosi TC",          "away": "Újpest FC",              "location": "Groupama Aréna"},
    {"round": "33. forduló", "date": "2027-05-22", "home": "Ferencvárosi TC",          "away": "Paksi FC",               "location": "Groupama Aréna"},

    # Nemzetközi meccsek – add hozzá ide a saját adatokkal:
    # {"round": "BL selejtező", "date": "2026-07-XX", "home": "Ferencvárosi TC", "away": "Ellenfél", "location": "Groupama Aréna"},
]

def generate_ics(matches):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Ferencváros 2026/27//HU",
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
        time_str = m.get("time", "18:00").replace(":", "")
        end_hour = f"{int(time_str[:2]) + 2:02d}"
        uid = f"fradi-{m['date']}-{i}@mlsz"
        summary = f"{m['home']} – {m['away']}"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Budapest:{date_str}T{time_str}00",
            f"DTEND;TZID=Europe/Budapest:{date_str}T{end_hour}{time_str[2:]}00",
            f"SUMMARY:{summary}",
            f"LOCATION:{m['location']}",
            f"DESCRIPTION:{m['round']}",
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
