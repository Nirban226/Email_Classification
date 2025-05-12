##  Email Classifier

[![Hugging Face Space](https://img.shields.io/badge/Live%20Demo-Hugging%20Face-blue)](https://nirban2206-email-classification.hf.space/docs)

---

## What This Does

This project provides a production-ready REST API that:

- Detects and masks sensitive PII (Personally Identifiable Information)  
- Classifies support emails into categories using a fine-tuned BERT-tiny model  
- Returns a structured and masked output for downstream use

---

## Features

- PII Masking using Regex + spaCy NER  
- Tiny BERT-based classifier for email categories  
- Fast and efficient: Runs on Hugging Face Spaces (CPU)  
- Swagger UI for testing your endpoint at `/docs`  
- Fully Dockerized for portability

---

## Live Demo

[Click here to open Swagger UI](https://nirban2206-email-classification.hf.space/docs)

---

## Sample Request

```bash
curl -X 'POST' \
  'https://nirban2206-email-classification.hf.space/classify' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "Hi, my name is John Doe and my phone is 9876543210."
  }'
```
---

## Sample Response
```bash
{
  "input_email_body": "Hi, my name is John Doe and my phone is 9876543210.",
  "list_of_masked_entities": [
    {
      "position": [40, 54],
      "classification": "phone_number",
      "entity": "9876543210"
    },
    {
      "position": [15, 26],
      "classification": "full_name",
      "entity": "John Doe"
    }
  ],
  "masked_email": "Hi, my name is [full_name] and my phone is [phone_number].",
  "category_of_the_email": "Incident"
}'
```
---

## How to Run Locally

1. Clone the Repository
```bash
git clone https://github.com/Nirban226/Email_Classification_Akaike_Technologies.git
cd Email_Classification_Akaike_Technologies
```


2. Install Requirements
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Start the API Locally
```bash
uvicorn app:app --reload
```
---
## Project Structure
```bash
.
├── app.py                     # FastAPI entry point
├── api/
│   └── api.py                 # (Optional alternate entry point)
├── models/
│   ├── bert_model/            # Trained model + tokenizer files
│   └── bert-tiny-tokenizer/   # Tokenizer for inference
├── utils/
│   └── masking.py             # PII masking logic
├── train_bert.py              # Training script
├── requirements.txt
├── Dockerfile
└── README.md
```

## Author

Reddi Nirban Kumar
As part of the Akaike Technologies Email Classification Assignment




