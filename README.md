# 🚨 RESCUE-AI: Intelligent Disaster Response System

##  Overview
RESCUE-AI is a **hybrid AI-ML web application** that analyzes emergency situations in real-time, providing instant assessment, resource needs identification, and actionable recommendations during disasters. Built for **Microsoft Azure Internship** with societal impact focus.

##  Live Demo
[**🚀 Try RESCUE-AI Live Now**](https://rescue-ai-disaster-response.onrender.com)

> **Note:** Free Render instances spin down after inactivity. First request takes ~50 seconds (cold start). Subsequent requests are fast (2-3 seconds).

### 🧪 Test Examples:
- `"Major flood in Delhi! People trapped! Need rescue urgently!"`
- `"Earthquake in Mumbai, buildings collapsed, many injured"`
- `"Forest fire spreading rapidly, villages evacuated"`

##  Key Features
| Feature | Technology | Description |
|---------|------------|-------------|
| 🤖 **Hybrid AI-ML** | Rule-based + scikit-learn | Combines rule-based logic with ML models |
| ⚡ **Real-time Analysis** | Flask API | Processes emergency descriptions instantly |
| 😰 **Sentiment Detection** | TextBlob NLP | ML-based panic/urgency emotion analysis |
| 📈 **Disaster Classification** | Naive Bayes ML | Classifies flood/earthquake/fire/storm/landslide |
| 🔥 **Severity Prediction** | Decision Tree ML | Predicts severity score 1-10 |
| 📍 **Location Extraction** | Regex patterns | Automatically extracts location from text |
| 🆘 **Resource Prediction** | Keyword analysis | Identifies needs (rescue, medical, shelter, food) |
| ☁️ **Cloud Deployment** | Render.com | Production-ready cloud deployment |

# 🛠️ Technologies Used
### Backend
- Python 3.9.16
- Flask 2.3.3
- Waitress 3.0.0 (Production WSGI server)

### AI/ML Stack
- scikit-learn 1.5.2 (Naive Bayes + Decision Tree)
- TextBlob (Sentiment Analysis)
- NLTK (Natural Language Processing)

### Frontend
- HTML5
- CSS3 (Emergency color scheme)
- JavaScript (AJAX for real-time updates)

### Deployment & DevOps
- Render.com (Cloud Platform)
- Git & GitHub (Version Control)
- requirements.txt (Dependency Management)

# 🚀 Getting Started

### 📋 Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for version control)

### 🔧 Installation
1. Clone the repository:
 ```bash
git clone https://github.com/Avani-create/rescue-ai-disaster-response.git
cd rescue-ai-disaster-response...
```
2.Install dependencies:
```bash
pip install -r requirements.txt
```
3.pip install -r requirements.txt
```bash
python app.py
```
4.Open browser: http://127.0.0.1:5000

#  ☁️ Deployment on Render.com
1.Create account on Render.com
2.Connect GitHub repository
3.Create Web Service with:
  Environment: Python 3
  Build Command: pip install -r requirements.txt
  Start Command: waitress-serve --port=$PORT app:app
  Instance Type: Free

#  📁 Project Structure
rescue-ai-disaster-response/
├── app.py              # Main Flask app (300+ lines AI/ML logic)
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version specification (3.9.16)
├── README.md           # This documentation
├── templates/
│   └── index.html     # Professional UI with ML section
└── static/            # Assets (CSS/JS/Images)

#  🤖 AI/ML Components Explained
###  1. Disaster Classification Model
Algorithm: Multinomial Naive Bayes
Training Data: 15 labeled disaster examples
Classes: Flood, Earthquake, Fire, Storm, Landslide
Accuracy: ~85% on training data

### 2. Severity Prediction Model
Algorithm: Decision Tree Classifier
Output: Severity score 1-10
Features: Keyword presence + sentiment score

### 3. Sentiment Analysis
Library: TextBlob
Metrics: Polarity (-1 to 1) + Subjectivity (0 to 1)
Output: Panic level detection

### 4. Rule-based AI Engine
Keyword matching for urgency levels
Regex patterns for location extraction
Actionable recommendations based on severity

#  API Endpoints
##  Frontend Code Example
```html
<!DOCTYPE html>
<html>
<head>
    <title>RESCUE-AI</title>
</head>
<body>
    <h1>Emergency Analysis</h1>
</body>
</html>
```

## 🔄 API Endpoints
```http
POST https://rescue-ai-disaster-response.onrender.com/analyze
Content-Type: application/json

{
  "text": "Major flood in Delhi! People trapped!"
}
```
Response:
```json
{
  "urgency": "CRITICAL 🚨",
  "type": "FLOOD",
  "location": "Delhi",
  "ml_analysis": {
    "ml_disaster_type": "FLOOD",
    "severity_score": "9/10"
  }
}
```

# 👥 Contributing
1. Fork the repository
2. Create feature branch (git checkout -b feature/AmazingFeature)
3. Commit changes (git commit -m 'Add AmazingFeature')
4. Push to branch (git push origin feature/AmazingFeature)
5. Open Pull Request

# 📄 License
MIT License

# 🙏 Acknowledgments
Microsoft Azure for internship opportunity
Render.com for free hosting
scikit-learn & TextBlob teams for ML/NLP libraries
Flask community for web framework

# 📞 Contact
Developer: Avani A
GitHub: @Avani-create
Project Link: https://github.com/Avani-create/rescue-ai-disaster-response
Live Demo: https://rescue-ai-disaster-response.onrender.com








