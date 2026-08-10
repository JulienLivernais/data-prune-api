def apply_business_rules(records: list[dict], source: str) -> tuple[list[dict], list[dict]]:
    if source == "un_comtrade":
        return _apply_un_comtrade_rules(records)
    if source == "japan_customs":
        return _apply_japan_customs_rules(records)

    return records, []


def _apply_un_comtrade_rules(records: list[dict]) -> tuple[list[dict], list[dict]]:
    valid_records = []
    rejected_records = []

    for row in records:
        try:
            value = float(row["primaryValue"])
        except (ValueError, TypeError):
            rejected_records.append({
                "content": row,
                "rejection_reason": "primaryValue is not a valid number",
            })
            continue

        if value <= 0:
            rejected_records.append({
                "content": row,
                "rejection_reason": "primaryValue must be positive",
            })
            continue

        if row["flowDesc"] != "Export":
            rejected_records.append({
                "content": row,
                "rejection_reason": f"Unexpected flow type: {row['flowDesc']}",
            })
            continue

        valid_records.append(row)

    return valid_records, rejected_records


def _apply_japan_customs_rules(records: list[dict]) -> tuple[list[dict], list[dict]]:
    valid_records = []
    rejected_records = []

    for row in records:
        raw_value = row.get("CUMULATIVE YEAR TO DATE VALUE")

        try:
            value = float(str(raw_value).replace(",", ""))
        except (ValueError, TypeError):
            rejected_records.append({
                "content": row,
                "rejection_reason": "CUMULATIVE YEAR TO DATE VALUE is not a valid number",
            })
            continue

        if value <= 0:
            rejected_records.append({
                "content": row,
                "rejection_reason": "CUMULATIVE YEAR TO DATE VALUE must be positive",
            })
            continue

        valid_records.append(row)

    return valid_records, rejected_records