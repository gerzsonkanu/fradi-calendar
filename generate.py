import os

OUTPUT_FILE = "docs/ferencvaros.ics"

MATCHES = [
    # --- UEFA Európa Liga – 1. kör (ellenfél ismert) ---
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – 1. kör (1. mérkőzés)", "date": "2026-07-09", "time": "20:00", "home": "FK Vojvodina",    "away": "Ferencvárosi TC", "location": "Novi Sad, Stadion Karadjordje"},
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – 1. kör (2. mérkőzés)", "date": "2026-07-16", "time": "20:15", "home": "Ferencvárosi TC", "away": "FK Vojvodina",    "location": "Budapest, Groupama Aréna"},

    # --- UEFA Európa Liga – 2. kör (ha továbbjut) ---
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – 2. kör (1. mérkőzés)", "date": "2026-07-23", "time": "20:00", "home": "Ferencvárosi TC", "away": "UEFA EL",             "location": "Budapest, Groupama Aréna"},
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – 2. kör (2. mérkőzés)", "date": "2026-07-30", "time": "20:00", "home": "UEFA EL",             "away": "Ferencvárosi TC", "location": ""},

    # --- UEFA Európa Liga – 3. kör (ha továbbjut) ---
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – 3. kör (1. mérkőzés)", "date": "2026-08-06", "time": "20:00", "home": "Ferencvárosi TC", "away": "UEFA EL",             "location": "Budapest, Groupama Aréna"},
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – 3. kör (2. mérkőzés)", "date": "2026-08-13", "time": "20:00", "home": "UEFA EL",             "away": "Ferencvárosi TC", "location": ""},

    # --- UEFA Európa Liga – Playoff (ha továbbjut) ---
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – Playoff (1. mérkőzés)", "date": "2026-08-20", "time": "20:00", "home": "Ferencvárosi TC", "away": "UEFA EL",            "location": "Budapest, Groupama Aréna"},
    {"emoji": "🌍🏆", "competition": "UEFA Európa Liga – Playoff (2. mérkőzés)", "date": "2026-08-27", "time": "20:00", "home": "UEFA EL",             "away": "Ferencvárosi TC", "location": ""},

    # --- OTP Bank Liga ---
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 1. forduló",  "date": "2026-07-25", "time": "18:00", "home": "Paksi FC",                 "away": "Ferencvárosi TC",         "location": "Paks, Paksi FC Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 2. forduló",  "date": "2026-08-01", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Vasas FC",                "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 3. forduló",  "date": "2026-08-08", "time": "18:00", "home": "ETO FC",                   "away": "Ferencvárosi TC",         "location": "Győr, ETO Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 4. forduló",  "date": "2026-08-15", "time": "18:00", "home": "ZTE FC",                   "away": "Ferencvárosi TC",         "location": "Zalaegerszeg, ZTE Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 5. forduló",  "date": "2026-08-22", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Kispest–Honvéd FC",       "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 6. forduló",  "date": "2026-08-29", "time": "18:00", "home": "Puskás Akadémia FC",       "away": "Ferencvárosi TC",         "location": "Felcsút, Pancho Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 7. forduló",  "date": "2026-09-05", "time": "18:00", "home": "Ferencvárosi TC",          "away": "MTK Budapest",            "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 8. forduló",  "date": "2026-09-19", "time": "18:00", "home": "Nyíregyháza Spartacus FC", "away": "Ferencvárosi TC",         "location": "Nyíregyháza, Városi Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 9. forduló",  "date": "2026-10-10", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Kisvárda Master Good",    "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 10. forduló", "date": "2026-10-17", "time": "18:00", "home": "Kisvárda Master Good",     "away": "Ferencvárosi TC",         "location": "Kisvárda, Várkerti Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 11. forduló", "date": "2026-10-24", "time": "18:00", "home": "Ferencvárosi TC",          "away": "DVSC",                    "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 12. forduló", "date": "2026-10-31", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Puskás Akadémia FC",      "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 13. forduló", "date": "2026-11-07", "time": "18:00", "home": "Vasas FC",                 "away": "Ferencvárosi TC",         "location": "Budapest, Illovszky Rudolf Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 14. forduló", "date": "2026-11-21", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Nyíregyháza Spartacus FC","location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 15. forduló", "date": "2026-11-28", "time": "18:00", "home": "MTK Budapest",             "away": "Ferencvárosi TC",         "location": "Budapest, Új Hidegkuti Nándor Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 16. forduló", "date": "2026-12-05", "time": "18:00", "home": "Ferencvárosi TC",          "away": "ETO FC",                  "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 17. forduló", "date": "2026-12-12", "time": "18:00", "home": "Kispest–Honvéd FC",        "away": "Ferencvárosi TC",         "location": "Budapest, Bozsik Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 18. forduló", "date": "2026-12-19", "time": "18:00", "home": "Újpest FC",                "away": "Ferencvárosi TC",         "location": "Budapest, Szusza Ferenc Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 19. forduló", "date": "2027-01-30", "time": "18:00", "home": "Ferencvárosi TC",          "away": "ZTE FC",                  "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 20. forduló", "date": "2027-02-06", "time": "18:00", "home": "DVSC",                     "away": "Ferencvárosi TC",         "location": "Debrecen, Nagyerdei Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 21. forduló", "date": "2027-02-13", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Paksi FC",                "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 22. forduló", "date": "2027-02-20", "time": "18:00", "home": "MTK Budapest",             "away": "Ferencvárosi TC",         "location": "Budapest, Új Hidegkuti Nándor Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 23. forduló", "date": "2027-02-27", "time": "18:00", "home": "Paksi FC",                 "away": "Ferencvárosi TC",         "location": "Paks, Paksi FC Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 24. forduló", "date": "2027-03-06", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Vasas FC",                "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 25. forduló", "date": "2027-03-13", "time": "18:00", "home": "ETO FC",                   "away": "Ferencvárosi TC",         "location": "Győr, ETO Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 26. forduló", "date": "2027-03-20", "time": "18:00", "home": "ZTE FC",                   "away": "Ferencvárosi TC",         "location": "Zalaegerszeg, ZTE Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 27. forduló", "date": "2027-04-03", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Újpest FC",               "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 28. forduló", "date": "2027-04-10", "time": "18:00", "home": "Puskás Akadémia FC",       "away": "Ferencvárosi TC",         "location": "Felcsút, Pancho Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 29. forduló", "date": "2027-04-17", "time": "18:00", "home": "Ferencvárosi TC",          "away": "Kispest–Honvéd FC",       "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 30. forduló", "date": "2027-04-24", "time": "18:00", "home": "Nyíregyháza Spartacus FC", "away": "Ferencvárosi TC",         "location": "Nyíregyháza, Városi Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 31. forduló", "date": "2027-05-01", "time": "18:00", "home": "Ferencvárosi TC",          "away": "MTK Budapest",            "location": "Budapest, Groupama Aréna"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 32. forduló", "date": "2027-05-15", "time": "18:00", "home": "Kisvárda Master Good",     "away": "Ferencvárosi TC",         "location": "Kisvárda, Várkerti Stadion"},
    {"emoji": "⚽️", "competition": "OTP Bank Liga, 33. forduló", "date": "2027-05-22", "time": "18:00", "home": "Ferencvárosi TC",          "away": "DVSC",                    "location": "Budapest, Groupama Aréna"},
]

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
        summary = f"{m['emoji']}{m['home']} – {m['away']}"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;TZID=Europe/Budapest:{date_str}T{int(h):02d}{mi}00",
            f"DTEND;TZID=Europe/Budapest:{date_str}T{end_h:02d}{mi}00",
            f"SUMMARY:{summary}",
            f"LOCATION:{m['location']}",
            f"DESCRIPTION:{m['competition']}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    matches = sorted(MATCHES, key=lambda x: (x["date"], x["time"]))
    ics = generate_ics(matches)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ics)
    print(f"Kész! {len(matches)} mérkőzés mentve.")
