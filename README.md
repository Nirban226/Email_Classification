# Email Classification 

A FastAPI-based solution that:

- Detects and masks PII (Personally Identifiable Information)
- Classifies the intent of support emails using a fine-tuned BERT model

## 🔧 Features

- Regex + spaCy-based PII masking for 8 entity types
- Tiny BERT model (prajjwal1/bert-tiny) for efficient classification
- REST API built with FastAPI
- Returns masked text + original PII + category

## 🚀 How to Run

### 1. Install dependencies


pip install -r requirements.txt
python -m spacy download en_core_web_sm
2. Train the Model (Optional)
python train_bert.py
3. Start the API
uvicorn api.api:app --reload
Visit http://localhost:8000/docs for Swagger UI.

🎯 API Endpoint

POST /classify
Request Body:

{
  "email": "Hi, I’m John Doe. My email is johndoe@gmail.com and phone is 9876543210."
}
Response:

{
  "input_email_body": "Hi, I’m John Doe. My email is johndoe@gmail.com and phone is 9876543210.",
  "list_of_masked_entities": [...],
  "masked_email": "Hi, I’m [full_name]. My email is [email] and phone is [phone_number]",
  "category_of_the_email": "Request"
}
📁 Project Structure

├── api/
│   └── api.py
├── models/
│   └── bert_model.py
├── utils/
│   └── masking.py
├── data/
│   └── combined_emails_with_natural_pii.csv
├── train_bert.py
├── requirements.txt
├── README.md
