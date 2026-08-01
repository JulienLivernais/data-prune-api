REQUIRED_FIELDS = [
    "cmdCode",
    "cmdDesc",
    "refYear",
    "reporterDesc",
    "partnerDesc",
    "flowDesc",
    "primaryValue",
]

def validate_records(records: list[dict]) -> tuple[list[dict], list[dict]]: # output = 2 lists
    valid_records = []
    rejected_records = []

    for row in records:
        missing_fields = [field for field in REQUIRED_FIELDS if not row.get(field)]

        if missing_fields:
            rejected_records.append({
                "content": row,
                "rejection_reason": f"Missing required field(s): {', '.join(missing_fields)}",
            })
        else:
            valid_records.append(row)

    return valid_records, rejected_records

