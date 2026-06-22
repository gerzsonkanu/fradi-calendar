import requests
import os

OUTPUT_FILE = "docs/ferencvaros.ics"

SOURCE_URL = "https://ics.fixtur.es/v2/ferencvaros.ics"

def fetch_and_save():
    print(f"Letöltés: {SOURCE_URL}")
    r = requests.get(SOURCE_URL, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()

    content = r.text

    content = content.replace(
        "X-WR-CALNAME:Ferencvarosi",
        "X-WR-CALNAME:Ferencvárosi TC 2026/27"
    )

    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    count = content.count("BEGIN:VEVENT")
    print(f"Kész! {count} mérkőzés mentve → {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_save()
