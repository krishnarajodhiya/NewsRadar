# Quick Start Guide - NewsVerify AI

## ⚡ 5-Minute Setup

### For macOS/Linux Users:

1. **Make setup script executable:**
   ```bash
   chmod +x setup.sh run.sh
   ```

2. **Run setup (automated):**
   ```bash
   ./setup.sh
   ```
   This will:
   - Create virtual environment
   - Install dependencies
   - Train the ML model

3. **In Terminal 1 - Start Backend:**
   ```bash
   ./run.sh
   ```
   You should see:
   ```
   Running on http://0.0.0.0:5000
   ```

4. **In Terminal 2 - Open Frontend:**
   ```bash
   open frontend/index.html
   ```
   Or serve it:
   ```bash
   cd frontend && python3 -m http.server 8000
   # Open http://localhost:8000 in browser
   ```

### For Windows Users:

1. **Run setup (automated):**
   ```cmd
   setup.bat
   ```

2. **In Command Prompt 1 - Start Backend:**
   ```cmd
   run.bat
   ```

3. **In File Explorer:**
   - Double-click `frontend/index.html` or
   - In Command Prompt 2:
     ```cmd
     cd frontend
     python -m http.server 8000
     # Open http://localhost:8000
     ```

## 🧪 Test the Application

1. **Paste fake news example:**
   ```
   Scientists discover cure for all diseases using simple spice
   ```
   Expected: **FAKE** (95%+ confidence)

2. **Paste real news example:**
   ```
   New study shows benefits of regular exercise for heart health
   ```
   Expected: **REAL** (90%+ confidence)

## 📊 Dashboard Features

- **Total Analyses**: Count of all predictions made
- **Fake News Detected**: Number of FAKE predictions
- **Real News Verified**: Number of REAL predictions
- **Recent Predictions**: Latest 5 predictions

## 🗂️ File Structure Summary

```
NewsRadar/
├── backend/app.py          ← Flask API server
├── backend/train_model.py  ← Train ML model here
├── models/model.pkl        ← Trained model (auto-created)
├── models/vectorizer.pkl   ← Vectorizer (auto-created)
├── frontend/index.html     ← Web interface
├── data/predictions.db     ← Database (auto-created)
└── README.md               ← Full documentation
```

## 🔍 Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| "Model not found" | Run `python backend/train_model.py` |
| Port 5000 busy | Change port in `backend/app.py` line 80 |
| CORS errors | Ensure backend runs on `http://localhost:5000` |
| Database errors | Delete `data/predictions.db` and restart |
| Script won't run (Mac) | Run `chmod +x *.sh` first |

## 📝 Default API Endpoints

- **Predict**: `POST http://localhost:5000/api/predict`
- **History**: `GET http://localhost:5000/api/history`
- **Dashboard**: `GET http://localhost:5000/api/dashboard`
- **Clear**: `POST http://localhost:5000/api/clear`

## 🎯 Next Steps

1. ✅ Run setup.sh / setup.bat
2. ✅ Start Flask backend
3. ✅ Open frontend in browser
4. ✅ Try predicting a news article
5. ✅ Check dashboard for statistics
6. ✅ View history of predictions

## 💡 Tips

- For development: Keep both terminals open
- Check console (F12) for JavaScript errors
- Check terminal for Flask errors
- Reload browser (Ctrl+R) if UI looks broken

## 📞 Need Help?

1. Check `README.md` for full documentation
2. Check `CONFIG.md` for advanced configuration
3. Verify Python 3.8+ is installed: `python3 --version`
4. Verify dependencies: `pip list`

---

**You're all set! Start analyzing news with AI! 🚀**
