import requests
import torch
import os
from transformers import BertTokenizer, BertForSequenceClassification

# Use absolute path to your model
# Get the current directory of this script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "geopolitical_bert")

# Initialize tokenizer and model
print(f"Loading model from: {MODEL_PATH}")
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)

# Set model to evaluation mode
model.eval()


# Create a simple wrapper for the model to use with SHAP (instead of direct integration)
def model_predict(texts):
    # Process a batch of texts
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)

    # Get probabilities
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    return probs.detach().numpy()


# ----------- News Fetching Function -----------
def fetch_latest_news(country_code='in', max_articles=10):
    API_KEY = 'da91d21637f7544b2fa4772c4daea924'  # <-- Replace this with your GNews API Key
    url = f"https://gnews.io/api/v4/top-headlines?country={country_code}&max={max_articles}&token={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        news_data = response.json()

        news_list = []
        for article in news_data.get('articles', []):
            news_list.append({
                'title': article['title'],
                'description': article.get('description', ''),
                'content': article.get('content', ''),
                'url': article['url']
            })

        return news_list

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


# ----------- Prediction Function -----------
def predict_stability(news_list):
    results = []
    for article in news_list:
        # Create input text from title and description
        text = article['title'] + " " + (article.get('description') or "")

        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            pred_class = torch.argmax(probs).item()

        # Add result to list
        results.append({
            "text": text,
            "prediction": "At Risk" if pred_class == 1 else "Safe",
            "confidence": float(probs[0][pred_class]),
            "url": article['url']
        })

    return results


# ----------- XAI Function Using Direct Token Attribution -----------
def explain_prediction(text):
    """
    Basic token importance based on logits changes
    """
    try:
        # First get the baseline prediction
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        with torch.no_grad():
            outputs = model(**inputs)
            baseline_logits = outputs.logits[0].detach().clone()
            pred_class = torch.argmax(baseline_logits).item()

        # Get token importances by masking one at a time
        token_importances = []
        for i in range(1, len(tokens) - 1):  # Skip [CLS] and [SEP]
            # Create a copy of the input with one token masked
            masked_inputs = inputs.copy()
            masked_inputs["input_ids"][0][i] = tokenizer.mask_token_id

            with torch.no_grad():
                masked_outputs = model(**masked_inputs)
                masked_logits = masked_outputs.logits[0]

            # Calculate the difference in prediction
            diff = baseline_logits[pred_class] - masked_logits[pred_class]
            token_importances.append((tokens[i], float(diff)))

        # Sort by importance (absolute value)
        token_importances = sorted(token_importances, key=lambda x: abs(x[1]), reverse=True)

        # Return top 5 tokens
        return token_importances[:5]
    except Exception as e:
        print(f"Error in explanation: {e}")
        # Return empty explanation in case of error
        return [("No explanation available", 0.0)]