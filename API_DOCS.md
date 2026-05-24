# NewsVerify AI - Complete API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, no authentication is required. For production, implement API key authentication.

---

## Endpoints

### 1. Health Check

**Description:** Verify that the backend is running and healthy.

**Endpoint:**
```
GET /health
```

**Response (200 OK):**
```json
{
    "status": "healthy",
    "message": "NewsVerify AI backend is running"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Predict News

**Description:** Analyze a news article or headline and get a prediction.

**Endpoint:**
```
POST /api/predict
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "text": "Your news article or headline here..."
}
```

**Response (200 OK):**
```json
{
    "prediction": "FAKE",
    "confidence": 95.5,
    "message": "This news is predicted as FAKE with 95.5% confidence"
}
```

**Response (400 Bad Request):**
```json
{
    "error": "Text must be at least 10 characters long"
}
```

**Possible Errors:**
- `"Please provide valid text input"` - Text is empty or invalid
- `"Text must be at least 10 characters long"` - Text too short
- `"Text must not exceed 5000 characters"` - Text too long
- `"Text must contain at least 3 meaningful words"` - Not enough meaningful content
- `"Request must be JSON"` - Wrong content type

**Example with cURL:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "New study shows benefits of exercise"}'
```

**Example with JavaScript:**
```javascript
fetch('http://localhost:5000/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        text: 'Your article text here...' 
    })
})
.then(res => res.json())
.then(data => console.log(data))
```

**Example with Python:**
```python
import requests

response = requests.post('http://localhost:5000/api/predict', 
    json={'text': 'Your article text here...'})
result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}%")
```

---

### 3. Get Prediction History

**Description:** Retrieve recent predictions from the database.

**Endpoint:**
```
GET /api/history?limit=10
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 10 | Number of records to return (1-100) |

**Response (200 OK):**
```json
{
    "predictions": [
        {
            "id": 1,
            "text": "Article text here...",
            "prediction": "FAKE",
            "confidence": 0.955,
            "created_at": "2024-01-15 10:30:45"
        },
        {
            "id": 2,
            "text": "Another article text...",
            "prediction": "REAL",
            "confidence": 0.872,
            "created_at": "2024-01-15 10:25:30"
        }
    ],
    "count": 2
}
```

**Example:**
```bash
# Get last 10 predictions
curl http://localhost:5000/api/history

# Get last 20 predictions
curl http://localhost:5000/api/history?limit=20

# Get last 50 predictions
curl 'http://localhost:5000/api/history?limit=50'
```

**JavaScript Example:**
```javascript
fetch('http://localhost:5000/api/history?limit=10')
    .then(res => res.json())
    .then(data => {
        data.predictions.forEach(pred => {
            console.log(`${pred.prediction} (${(pred.confidence*100).toFixed(1)}%)`);
        });
    });
```

---

### 4. Get Dashboard Statistics

**Description:** Get overall statistics and recent predictions.

**Endpoint:**
```
GET /api/dashboard
```

**Response (200 OK):**
```json
{
    "total_predictions": 42,
    "stats": {
        "FAKE": 18,
        "REAL": 24
    },
    "recent_predictions": [
        {
            "id": 42,
            "text": "Article text...",
            "prediction": "REAL",
            "confidence": 0.89,
            "created_at": "2024-01-15 10:35:00"
        }
    ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/dashboard
```

**JavaScript Example:**
```javascript
fetch('http://localhost:5000/api/dashboard')
    .then(res => res.json())
    .then(data => {
        console.log(`Total: ${data.total_predictions}`);
        console.log(`Fake: ${data.stats.FAKE}`);
        console.log(`Real: ${data.stats.REAL}`);
    });
```

---

### 5. Clear Prediction History

**Description:** Delete all predictions from the database.

**Endpoint:**
```
POST /api/clear
```

**Response (200 OK):**
```json
{
    "message": "Prediction history cleared successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/clear
```

**Warning:** This action cannot be undone!

---

## Request/Response Details

### Confidence Score
- Range: 0-100 (percentage)
- In JSON response: 0-1 (decimal, multiply by 100 for percentage)
- Higher = more confident in the prediction

### Prediction Values
- `"FAKE"` - The model predicts the text is fake news
- `"REAL"` - The model predicts the text is real news

### Timestamps
- Format: `YYYY-MM-DD HH:MM:SS`
- Timezone: UTC/System timezone
- Example: `2024-01-15 10:30:45`

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Prediction made successfully |
| 400 | Bad Request | Invalid input provided |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Internal error occurred |
| 503 | Service Unavailable | Model not loaded |

### Error Response Format
```json
{
    "error": "Description of what went wrong"
}
```

---

## Rate Limiting (Future Enhancement)

Not currently implemented. For production:
- Implement rate limiting (e.g., 100 requests/minute)
- Add API key authentication
- Monitor usage patterns

---

## CORS Headers

The API includes CORS headers for cross-origin requests:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Performance Notes

- **Model Loading:** ~2-5 seconds on startup
- **Prediction Time:** ~100-200ms per request
- **Database:** SQLite (suitable for small-medium datasets)
- **Throughput:** ~5-10 predictions per second (single instance)

For production with higher load:
- Use connection pooling
- Implement caching
- Use multi-processing/workers
- Scale horizontally with load balancer

---

## Best Practices

1. **Input Validation:** Always validate text length on client side
2. **Error Handling:** Handle network errors gracefully
3. **Performance:** Cache results for identical predictions
4. **Security:** Don't send sensitive data in predictions
5. **Rate Limiting:** Implement on client side to be respectful
6. **Logging:** Log important events for debugging

---

## Integration Examples

### React Component
```javascript
const [result, setResult] = useState(null);

const predict = async (text) => {
    const res = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    const data = await res.json();
    setResult(data);
};
```

### Python Wrapper
```python
def predict_news(text):
    import requests
    response = requests.post(
        'http://localhost:5000/api/predict',
        json={'text': text}
    )
    return response.json()

result = predict_news("Your article here")
```

### Node.js/Express
```javascript
app.post('/analyze', async (req, res) => {
    const { text } = req.body;
    const result = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    }).then(r => r.json());
    res.json(result);
});
```

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- 5 main endpoints
- SQLite database
- TF-IDF + Logistic Regression model
- Responsive web interface

---

## Support

For issues or questions about the API:
1. Check the error message in the response
2. Verify your request format matches examples
3. Check console logs for detailed errors
4. Review QUICKSTART.md for setup help

---

**Last Updated:** January 2024
**API Version:** 1.0.0
