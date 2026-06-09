def medicine_validation_prompt(
    platform_med,
    vision_med
):
    return f"""
You are a medical prescription validation expert.

Compare the following prescription medicines.

Platform Medicine:

{platform_med}

Vision Medicine:

{vision_med}

Validation Tasks:

1. Check if medicine names refer to the same medicine.
2. Handle OCR / Vision spelling mistakes.
3. Check dosage match.
4. Check frequency match.
5. Check formulation mismatch if present.
6. Determine overall semantic match.

Return ONLY valid JSON.

Format:

{{
    "semantic_match": true,
    "name_match": true,
    "dosage_match": true,
    "frequency_match": true,
    "confidence": 95,
    "reason": ""
}}

Examples:

Reason examples:

- Medicine name mismatch
- Dosage mismatch
- Frequency mismatch
- Dosage and frequency mismatch
- Vision extraction typo but same medicine
- Fully validated
"""
MEDICINE_EXTRACTION_PROMPT = """
You are a medical prescription extraction expert.

Analyze the prescription image carefully.

Extract all medicines along with dosage and frequency.

Rules:
- Do not guess medicines.
- Do not invent medicines.
- Preserve spelling exactly as seen.
- Extract medicine name.
- Extract dosage.
- Extract frequency.
- Ignore doctor details.
- Ignore patient details.
- Ignore diagnosis.
- Ignore hospital details.

Return ONLY valid JSON.

Format:

{
    "medicines": [
        {
            "name": "Medicine Name",
            "dosage": "10mg",
            "frequency": "OD"
        },
        {
            "name": "Medicine Name",
            "dosage": "500mg",
            "frequency": "BD"
        }
    ]
}
"""