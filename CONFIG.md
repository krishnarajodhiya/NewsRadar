# NewsVerify AI - Configuration Guide

## Environment Setup

### Python Environment Variables (Optional)

Create a `.env` file in the project root for custom configuration:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_PATH=data/predictions.db
MODEL_PATH=models/model.pkl
VECTORIZER_PATH=models/vectorizer.pkl
```

## Flask Configuration

Edit `backend/app.py` to customize:

```python
# Port and Host
app.run(
    debug=True,                    # Debug mode
    host='0.0.0.0',               # Listen on all interfaces
    port=5000                      # Port number
)
```

## Model Configuration

Edit `backend/train_model.py` to adjust:

```python
# TF-IDF Settings
vectorizer = TfidfVectorizer(
    max_features=5000,            # Number of features
    min_df=1,                      # Minimum document frequency
    max_df=0.8,                    # Maximum document frequency
    ngram_range=(1, 2),            # N-gram range
    sublinear_tf=True              # Sublinear TF scaling
)

# Model Settings
model = LogisticRegression(
    max_iter=200,                  # Maximum iterations
    random_state=42,               # Random seed
    class_weight='balanced'         # Balance class weights
)
```

## Database Configuration

The SQLite database is automatically created at `data/predictions.db`

To reset the database:
```bash
rm data/predictions.db
# The database will be recreated on next Flask run
```

## Frontend Configuration

Edit `frontend/script.js` API endpoint if backend is on different port:

```javascript
const API_BASE_URL = 'http://localhost:5000';
```

## CORS Configuration

To modify CORS settings in `backend/app.py`:

```python
# Allow specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

## Logging

To enable logging in `backend/app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

## Production Deployment

For production deployment:

1. Set `debug=False` in Flask
2. Use production WSGI server (Gunicorn, uWSGI)
3. Enable HTTPS/TLS
4. Add rate limiting
5. Implement authentication
6. Use environment variables for secrets

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## Performance Optimization

### Model Loading
The model is loaded once on startup to improve performance.

### Caching
Add caching for predictions (optional):
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def predict_cached(text):
    # Prediction logic
    pass
```

### Database Optimization
To optimize SQLite:
```python
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('PRAGMA synchronous=NORMAL')
```

## Troubleshooting

### Port Already in Use
Change port in `app.py`:
```python
app.run(port=5001)  # Use port 5001 instead
```

### Model Too Slow
Reduce `max_features` in train_model.py:
```python
max_features=1000  # Reduce from 5000
```

### Database Locked
Close all connections and restart Flask:
```bash
pkill -f "python.*app.py"
```

### CORS Issues
Ensure backend and frontend have proper CORS configuration

## Backup

To backup your data:
```bash
# Backup database
cp data/predictions.db data/predictions.db.backup

# Backup models
cp models/*.pkl models/backup/
```
