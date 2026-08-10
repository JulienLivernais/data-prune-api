from pipeline.cleaner import clean_records
from pipeline.validator import validate_records
from pipeline.business_rules import apply_business_rules
from pipeline.source_detector import detect_source


def run_pipeline(records: list[dict]) -> tuple[list[dict], list[dict], int, int]:
    cleaned, values_corrected, duplicates_removed = clean_records(records)

    source = detect_source(cleaned)
    valid_after_validation, rejected_1 = validate_records(cleaned, source)
    valid_after_rules, rejected_2 = apply_business_rules(valid_after_validation, source)

    all_rejected = rejected_1 + rejected_2

    return valid_after_rules, all_rejected, values_corrected, duplicates_removed