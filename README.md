# NewsVerify AI - Fake News Detection Application

A complete web application for detecting fake news using Machine Learning. Built with Python Flask, Scikit-learn, and a modern responsive UI.

## 🎯 Features

✅ **News Analysis** - Paste any news article or headline for instant analysis
✅ **ML-Powered Detection** - TF-IDF + Logistic Regression model
✅ **Confidence Scores** - View prediction confidence percentage
✅ **Prediction History** - SQLite database stores all predictions
✅ **Dashboard Stats** - View total checks and recent predictions
✅ **Responsive UI** - Clean, modern design works on all devices
✅ **Error Handling** - Comprehensive input validation
✅ **API Routes** - RESTful API for easy integration

## 📁 Project Structure

```
NewsRadar/
├── backend/
│   ├── app.py                 # Flask application
│   ├── train_model.py         # Model training script
│   ├── database.py            # SQLite operations
│   └── preprocessor.py        # Text preprocessing
├── frontend/
│   ├── index.html             # HTML interface
│   ├── style.css              # Styling
│   └── script.js              # Client-side logic
├── models/                    # Saved ML models
│   ├── model.pkl              # Trained model
│   └── vectorizer.pkl         # TF-IDF vectorizer
├── data/
│   └── predictions.db         # SQLite database
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Tech Stack

### Backend
- **Flask** - Web framework
- **Scikit-learn** - Machine learning library
- **TF-IDF Vectorizer** - Feature extraction
- **Logistic Regression** - Classification model
- **Pandas & NumPy** - Data processing
- **NLTK** - Natural language processing
- **SQLite** - Database

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (responsive)
- **Vanilla JavaScript** - Interactivity

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Modern web browser

## ⚙️ Installation

### 1. Clone/Download the Project
```bash
cd NewsRadar
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model
```bash
cd backend
python train_model.py
```

This will:
- Create sample training dataset
- Train TF-IDF vectorizer
- Train Logistic Regression model
- Save `model.pkl` and `vectorizer.pkl` in `models/` folder

Expected output:
```
Loading training data...
Dataset size: 40
FAKE news: 20
REAL news: 20

Creating TF-IDF vectorizer...
TF-IDF features: 5000

Training Logistic Regression model...

Evaluating model...
Accuracy:  0.8500
Precision: 0.8500
Recall:    0.8500
F1-Score:  0.8500

✓ Model training complete!
```

## 🚀 Running the Application

### 1. Start Flask Backend
```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000`

Expected output:
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### 2. Open Frontend (New Terminal)
Simply open the HTML file in your browser:
```bash
# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html

# Windows
start frontend/index.html

# Or manually: Open file://path/to/NewsRadar/frontend/index.html in your browser
```

Alternatively, you can serve it with Python:
```bash
# From project root
cd frontend
python -m http.server 8000
# Then open http://localhost:8000 in your browser
```

## 📖 Usage

### 1. **Analyze News**
   - Go to the "Predictor" tab
   - Paste a news article or headline
   - Click "Analyze News"
   - View the prediction (FAKE/REAL) and confidence percentage

### 2. **View Dashboard**
   - Go to the "Dashboard" tab
   - See total predictions made
   - View statistics (FAKE vs REAL)
   - Check recent predictions

### 3. **Check History**
   - Go to the "History" tab
   - View all previous predictions
   - See timestamps and confidence scores
   - Clear history if needed

## 🔌 API Endpoints

### Health Check
```
GET /health
```
Response: `{"status": "healthy", "message": "..."}`

### Make Prediction
```
POST /api/predict
Content-Type: application/json

{
    "text": "Your news article or headline here..."
}
```
Response:
```json
{
    "prediction": "FAKE" | "REAL",
    "confidence": 95.5,
    "message": "This news is predicted as FAKE with 95.5% confidence"
}
```

### Get History
```
GET /api/history?limit=10
```
Response:
```json
{
    "predictions": [
        {
            "id": 1,
            "text": "article text",
            "prediction": "FAKE",
            "confidence": 0.95,
            "created_at": "2024-01-01 10:00:00"
        }
    ],
    "count": 1
}
```

### Get Dashboard Stats
```
GET /api/dashboard
```
Response:
```json
{
    "total_predictions": 100,
    "stats": {
        "FAKE": 45,
        "REAL": 55
    },
    "recent_predictions": [...]
}
```

### Clear History
```
POST /api/clear
```
Response: `{"message": "Prediction history cleared successfully"}`

## 🧹 Data Preprocessing

Text is processed through:
1. **Lowercase conversion** - Standardize text
2. **URL removal** - Remove web links
3. **Email removal** - Remove email addresses
4. **Special character removal** - Keep only letters and spaces
5. **Whitespace normalization** - Clean spacing
6. **Tokenization** - Split into words
7. **Stopword removal** - Remove common words (the, is, etc.)
8. **Lemmatization** - Reduce words to base form

## 🤖 Model Details

- **Algorithm**: Logistic Regression
- **Feature Extraction**: TF-IDF Vectorizer
- **Max Features**: 5000
- **N-gram Range**: 1-2 (unigrams and bigrams)
- **Train-Test Split**: 80-20
- **Class Balancing**: Balanced weights

## 📊 Example Results

**Fake News Detection:**
```
Input: "Scientists discover cure for all diseases using simple spice"
Prediction: FAKE
Confidence: 96.5%
```

**Real News Detection:**
```
Input: "New study shows benefits of regular exercise for heart health"
Prediction: REAL
Confidence: 94.2%
```

## ⚠️ Input Validation

The application validates:
- Minimum 10 characters required
- Maximum 5000 characters allowed
- Minimum 3 meaningful words (after preprocessing)
- No empty input

## 🐛 Troubleshooting

### Model not found error
```
Error: Model not found. Please train the model first.
```
**Solution:** Run `python train_model.py` in the backend folder first.

### CORS errors
If you get CORS errors, ensure the backend is running on `http://localhost:5000`

### Database errors
The SQLite database is automatically created in `data/predictions.db`

### Port already in use
If port 5000 is busy, modify in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or other port
```

## 🔐 Security Notes

- This is a demonstration application
- For production, implement:
  - Rate limiting
  - Input sanitization
  - HTTPS/TLS
  - User authentication
  - API key validation
  - CORS configuration

## 📈 Model Improvement Tips

To improve model accuracy:
1. Use larger training datasets (thousands of real articles)
2. Balance FAKE/REAL samples equally
3. Add more features (author credibility, source, etc.)
4. Try ensemble methods
5. Use deep learning (LSTM, BERT)

## 📝 Configuration

### Backend Configuration (app.py)
```python
# Flask settings
debug=True              # Development mode
host='0.0.0.0'         # Listen on all interfaces
port=5000              # Port number
```

### Model Configuration (train_model.py)
```python
max_features=5000      # Maximum TF-IDF features
min_df=1               # Minimum document frequency
max_df=0.8             # Maximum document frequency
ngram_range=(1, 2)     # Unigrams and bigrams
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs for error messages
3. Verify all dependencies are installed
4. Ensure port 5000 is available

## 📄 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

- Scikit-learn for ML models
- Flask for web framework
- NLTK for NLP capabilities

---

**Happy Fact-Checking! 🎉**
