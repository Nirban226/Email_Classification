# models/bert_model.py

import os
import pandas as pd
import torch
import joblib
from sklearn.preprocessing import LabelEncoder
from transformers import (
    BertTokenizerFast,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset

# Define save paths
MODEL_DIR = "models/bert_model"
TOKENIZER_DIR = "models/bert-tiny-tokenizer"
PRETRAINED_MODEL_DIR = "models/bert-tiny-model"

# Create model directory if needed
os.makedirs(MODEL_DIR, exist_ok=True)

label_encoder = LabelEncoder()

def preprocess_data(csv_path):
    df = pd.read_csv(csv_path)

    # Optional: Filter out overly long emails (rare but good safety)
    df = df[df['email'].str.len() < 2000]

    # Sample for quicker training
    df = df[['email', 'type']].dropna().sample(3000, random_state=42).reset_index(drop=True)
    df['label'] = label_encoder.fit_transform(df['type'])

    joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))
    return Dataset.from_pandas(df[['email', 'label']])

# Truncation fix for long sequences
def tokenize_function(example):
    return tokenizer(
        example["email"],
        padding="max_length",
        truncation=True,
        max_length=512  # ✅ BERT max token length
    )

def train_bert_model(csv_path):
    global tokenizer
    dataset = preprocess_data(csv_path)

    # Load tokenizer and model from local dirs
    tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_DIR)
    model = BertForSequenceClassification.from_pretrained(PRETRAINED_MODEL_DIR, num_labels=4)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)

    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        logging_dir=os.path.join(MODEL_DIR, "logs"),
        save_total_limit=1,
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['test'],
        tokenizer=tokenizer
    )

    trainer.train()
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print("✅ Tiny BERT model and tokenizer saved to:", MODEL_DIR)

def predict_category(email_text):
    tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
    model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
    label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

    inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()

    return label_encoder.inverse_transform([predicted_label])[0]
