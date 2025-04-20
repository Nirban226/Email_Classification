from models.bert_model import train_bert_model

if __name__ == "__main__":
    train_bert_model("data/combined_emails_with_natural_pii.csv")
