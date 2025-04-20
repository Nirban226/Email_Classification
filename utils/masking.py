

import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns for PII
patterns = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_number": r"\b(?:\+91[\-\s]?|0)?[6-9]\d{9}\b",
    "dob": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:\d{1,2})(?:st|nd|rd|th)? (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{2,4}\b",
    "aadhar_num": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2,4})\b"
}

def mask_pii(text):
    """
    Mask PII entities in the given text.
    
    Returns:
        - masked_text: email with PII replaced
        - entities: list of masked entities with position and original text
    """
    entities = []
    masked_text = text
    offset = 0

    # 1. Regex-based masking
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            original = match.group()
            start, end = match.start(), match.end()
            replacement = f"[{label}]"

            # Adjust for changes in length
            adjusted_start = start + offset
            adjusted_end = end + offset

            masked_text = masked_text[:adjusted_start] + replacement + masked_text[adjusted_end:]

            entities.append({
                "position": [adjusted_start, adjusted_start + len(replacement)],
                "classification": label,
                "entity": original
            })

            offset += len(replacement) - (end - start)

    # 2. spaCy-based NER for full names
    doc = nlp(masked_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            original = ent.text
            replacement = "[full_name]"

            if replacement in masked_text[start:end]:  # skip already masked
                continue

            masked_text = masked_text[:start] + replacement + masked_text[end:]
            entities.append({
                "position": [start, start + len(replacement)],
                "classification": "full_name",
                "entity": original
            })

    return masked_text, entities
