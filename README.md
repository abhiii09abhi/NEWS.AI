# 🌍 Geopolitical News Stability Classifier (XAI Project)

This project detects whether a **country is stable or at risk** based on recent **news headlines** using a fine-tuned BERT model. Built with deep learning and explainable AI (XAI) techniques.

---

## 📌 Project Objective

Classify geopolitical news as:
- `safe`: No critical threat or conflict.
- `at_risk`: Potential or ongoing risk such as war, violence, or political instability.

### ✅ Uses:
- Real-time monitoring of global situations
- Explainability of why a region is flagged as unstable
- Potential use in global analytics, risk assessments, or news intelligence systems

---

## 🧠 Model Details

- Base Model: [`bert-base-uncased`](https://huggingface.co/bert-base-uncased)
- Fine-tuned on: 1000+ labeled geopolitical headlines
- Task: Binary classification (`safe` vs `at_risk`)
- Tokenizer and Model saved using `safetensors` format for speed and security

---

## 🛠 Tech Stack

- **NLP**: Hugging Face Transformers, BERT
- **Backend**: Flask API (Python)
- **Frontend (Optional)**: HTML + JS (for visualization)
- **XAI**: SHAP, Attention Visualization (planned)

---

## 🚀 Features

- ✅ Live news headline classification
- ✅ Explainable results (XAI-ready)
- ✅ Lightweight REST API with Flask
- ✅ Easily deployable

---

## 📂 Folder Structure
. ├── geopolitical_bert/ # Saved model & tokenizer │ ├── config.json │ ├── model.safetensors │ ├── tokenizer_config.json │ ├── vocab.txt │ └── special_tokens_map.json ├── labeled_news.csv # Manually labeled training dataset ├── app.py # Flask backend ├── requirements.txt # Python dependencies └── README.md # Project overview (this file)








---

🙏 Acknowledgements
- Hugging Face Transformers
- BERT by Google AI
- SHAP
- PyTorch


---



👨‍💻 Author
Abhijit 

Final Year Engineering Student | AI & DS Enthusiast

✉️ abhiijitjadhav.email@example.com
