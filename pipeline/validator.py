REQUIRED_FIELDS_BY_SOURCE = {
    "un_comtrade": ["cmdCode", "cmdDesc", "refYear", "reporterDesc", "partnerDesc", "flowDesc", "primaryValue"],
    "japan_customs": ["COMMODITY", "COUNTRY NAME", "CUMULATIVE YEAR TO DATE VALUE"],
}


def validate_records(records: list[dict], source: str) -> tuple[list[dict], list[dict]]:
    required_fields = REQUIRED_FIELDS_BY_SOURCE.get(source, [])
    valid_records = []
    rejected_records = []

    for row in records:
        missing_fields = [field for field in required_fields if not row.get(field)]

        if missing_fields:
            rejected_records.append({
                "content": row,
                "rejection_reason": f"Missing required field(s): {', '.join(missing_fields)}",
            })
        else:
            valid_records.append(row)

    return valid_records, rejected_records