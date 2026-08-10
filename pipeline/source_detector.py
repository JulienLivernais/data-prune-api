def detect_source(records: list[dict]) -> str:
    if not records:
        return "unknown"

    keys = set(records[0].keys())

    if "cmdCode" in keys:
        return "un_comtrade"
    if "COMMODITY" in keys and "COUNTRY NAME" in keys:
        return "japan_customs"

    return "unknown"

