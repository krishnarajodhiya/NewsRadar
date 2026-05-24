"""
Flask Backend for Fake News Detection Application
Provides API endpoints for predictions and history management
"""
import os
import pickle
import json
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

# Handle imports for both direct execution and gunicorn
try:
    from .database import init_db, save_prediction, get_recent_predictions, get_total_predictions, get_stats
    from .preprocessor import preprocess_text, validate_input
except ImportError:
    from database import init_db, save_prediction, get_recent_predictions, get_total_predictions, get_stats
    from preprocessor import preprocess_text, validate_input

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes
CORS(app, 
     origins="*",
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization"]
)

# Model paths
MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

# Global variables for model and vectorizer
model = None
vectorizer = None


def load_model():
    """Load the trained model and vectorizer"""
    global model, vectorizer
    
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        return False
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


# Database initialization flag
db_initialized = False

@app.before_request
def setup():
    """Setup on first request"""
    global db_initialized
    
    # Initialize database once
    if not db_initialized:
        init_db()
        db_initialized = True
    
    # Load model if not loaded
    if model is None:
        if not load_model():
            return jsonify({
                'error': 'Model not found. Please train the model first.'
            }), 503


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'NewsVerify AI backend is running'
    }), 200


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict whether a news article is FAKE or REAL
    
    Expected JSON:
    {
        "text": "article or headline text"
    }
    
    Returns:
    {
        "prediction": "FAKE" or "REAL",
        "confidence": 0.95,
        "message": "Success message"
    }
    """
    try:
        # Get request data
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        # Validate input
        is_valid, error_msg = validate_input(text)
        if not is_valid:
            return jsonify({
                'error': error_msg
            }), 400
        
        # Check if model is loaded
        if model is None or vectorizer is None:
            return jsonify({
                'error': 'Model not initialized'
            }), 503
        
        # Preprocess text
        processed_text = preprocess_text(text)
        
        # Vectorize
        text_tfidf = vectorizer.transform([processed_text])
        
        # Make prediction
        prediction = model.predict(text_tfidf)[0]
        
        # Get confidence scores
        confidence_scores = model.predict_proba(text_tfidf)[0]
        confidence = max(confidence_scores) * 100  # Convert to percentage
        
        # Save to database
        save_prediction(text, prediction, confidence / 100)
        
        return jsonify({
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'message': f'This news is predicted as {prediction} with {round(confidence, 2)}% confidence'
        }), 200
    
    except BadRequest as e:
        return jsonify({
            'error': 'Invalid request format'
        }), 400
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({
            'error': 'An error occurred during prediction'
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get recent prediction history
    
    Query params:
        limit: Number of records to return (default: 10)
    
    Returns:
    {
        "predictions": [
            {
                "id": 1,
                "text": "article text",
                "prediction": "FAKE",
                "confidence": 0.95,
                "created_at": "2024-01-01 10:00:00"
            }
        ]
    }
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Validate limit
        if limit < 1 or limit > 100:
            limit = 10
        
        predictions = get_recent_predictions(limit)
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions)
        }), 200
    
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({
            'error': 'Error retrieving prediction history'
        }), 500


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """
    Get dashboard statistics
    
    Returns:
    {
        "total_predictions": 100,
        "stats": {
            "FAKE": 45,
            "REAL": 55
        },
        "recent_predictions": [...]
    }
    """
    try:
        total = get_total_predictions()
        stats = get_stats()
        recent = get_recent_predictions(5)
        
        return jsonify({
            'total_predictions': total,
            'stats': stats,
            'recent_predictions': recent
        }), 200
    
    except Exception as e:
        print(f"Error getting dashboard: {e}")
        return jsonify({
            'error': 'Error retrieving dashboard data'
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """
    Clear all prediction history
    
    Returns:
    {
        "message": "History cleared successfully"
    }
    """
    try:
        try:
            from .database import clear_predictions
        except ImportError:
            from database import clear_predictions
        clear_predictions()
        
        return jsonify({
            'message': 'Prediction history cleared successfully'
        }), 200
    
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({
            'error': 'Error clearing history'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Load model
    if not load_model():
        print("Warning: Model not found. Please run train_model.py first")
    
    # Get port from command line argument or use default
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            if sys.argv[1] == '--port' and len(sys.argv) > 2:
                try:
                    port = int(sys.argv[2])
                except ValueError:
                    port = 5000
    
    print(f"Starting Flask app on port {port}...")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=port)
