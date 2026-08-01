def apply_business_rules(records: list[dict]) -> tuple[list[dict], list[dict]]:
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