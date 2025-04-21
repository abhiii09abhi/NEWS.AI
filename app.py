from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import fetch_latest_news, predict_stability, explain_prediction

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/')
def index():
    # Serve the HTML file
    return send_from_directory('../frontend', 'index.html')


@app.route('/script.js')
def js():
    # Serve the JS file
    return send_from_directory('../frontend', 'script.js')


# ---- Endpoint 1: Predict from live news ----
@app.route('/predict_live', methods=['GET'])
def predict_from_live_news():
    try:
        country_code = request.args.get('country', default='in')  # Default: India
        news = fetch_latest_news(country_code=country_code)

        if not news:
            return jsonify([])

        results = predict_stability(news)

        for res in results:
            try:
                res['explanation'] = explain_prediction(res['text'])
            except Exception as e:
                print(f"Error explaining prediction: {e}")
                res['explanation'] = [("Error generating explanation", 0.0)]

        return jsonify(results)
    except Exception as e:
        print(f"Error in predict_live endpoint: {e}")
        return jsonify({"error": str(e)}), 500


# ---- Endpoint 2: Predict from manually passed news ----
@app.route('/predict', methods=['POST'])
def predict_from_input():
    try:
        data = request.json
        news = data.get("news", [])

        if not news:
            return jsonify([])

        results = predict_stability(news)

        for res in results:
            try:
                res['explanation'] = explain_prediction(res['text'])
            except Exception as e:
                print(f"Error explaining prediction: {e}")
                res['explanation'] = [("Error generating explanation", 0.0)]

        return jsonify(results)
    except Exception as e:
        print(f"Error in predict endpoint: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting Country Stability Predictor API...")
    app.run(debug=True)