import csv
from typing import Optional


async def load_ofac_sanctions(csv_path: Optional[str] = None) -> list[dict]:
    if csv_path:
        try:
            sanctions = []
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sanctions.append(row)
            return sanctions
        except FileNotFoundError:
            pass

    return _get_mock_sanctions()


def _get_mock_sanctions() -> list[dict]:
    return [
        {"name": "IRANIAN OIL CO.", "type": "Entity", "program": "IRAN", "country": "Iran"},
        {"name": "IRGC-OPINION", "type": "Entity", "program": "IRAN", "country": "Iran"},
        {"name": "ROSNEFT OIL", "type": "Entity", "program": "UKRAINE-RUSSIA", "country": "Russia"},
        {"name": "HOUTHI MOVEMENT", "type": "Entity", "program": "YEMEN", "country": "Yemen"},
    ]


async def get_sanctions_summary() -> dict:
    sanctions = await load_ofac_sanctions()
    countries = {}
    for s in sanctions:
        country = s.get("country", "Unknown")
        countries[country] = countries.get(country, 0) + 1
    return {"total_entities": len(sanctions), "by_country": countries}
