def clean_records(records: list[dict]) -> tuple[list[dict], int, int]:
    cleaned_records = []
    seen_keys = set()

    values_corrected = 0
    duplicates_removed = 0

    for row in records:
        key = (row.get("cmdCode"), row.get("refYear"), row.get("reporterDesc"),
               row.get("partnerDesc"), row.get("flowDesc"))

        if key in seen_keys:
            duplicates_removed += 1
            continue
        seen_keys.add(key)

        cleaned_row = {}
        for field, value in row.items():
            if isinstance(value, str):
                stripped = value.strip()
                if stripped != value:
                    values_corrected += 1
                cleaned_row[field] = stripped
            else:
                cleaned_row[field] = value

        cleaned_records.append(cleaned_row)

    return cleaned_records, values_corrected, duplicates_removed