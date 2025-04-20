

from fastapi import FastAPI
from pydantic import BaseModel
from utils.masking import mask_pii
from models.bert_model import predict_category

# Define request schema
class EmailRequest(BaseModel):
    email: str

# Define response schema
class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: list
    masked_email: str
    category_of_the_email: str


# Create FastAPI app
app = FastAPI(
    title="Akaike Email Classification API",
    description="Performs PII masking + BERT classification on input emails",
    version="1.0"
)

@app.post("/classify", response_model=EmailResponse)
def classify_email(request: EmailRequest):
    # Step 1: Mask the email
    masked_email, entities = mask_pii(request.email)

    # Step 2: Predict the type using BERT
    label = predict_category(masked_email)

    # Step 3: Return response
    return {
    "input_email_body": request.email,
    "list_of_masked_entities": entities,
    "masked_email": masked_email,
    "category_of_the_email": label
}
