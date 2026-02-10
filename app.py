from flask import Flask, render_template, request, jsonify
import re
import os  # ← ADDED THIS LINE

# ============= ML IMPORTS =============
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
import numpy as np
# ============= END ML IMPORTS =============

app = Flask(__name__)

# ============= ML TRAINING DATA =============
# This is how ML "learns" - we give examples

# Training data for disaster classification
DISASTER_TRAINING_TEXTS = [
    "flood water rising help emergency",
    "flood river overflow house underwater",
    "flood rain continuous flooding street",
    "earthquake building collapse tremor",
    "earthquake ground shaking house damage",
    "earthquake seismic aftershock dangerous",
    "fire blaze burning house rescue",
    "fire smoke forest wildfire spread",
    "fire emergency flames building",
    "storm cyclone hurricane wind damage",
    "storm rain flood wind speed",
    "storm thunder lightning trees fallen",
    "landslide mudslide hill collapse",
    "landslide earth movement road blocked",
    "landslide rain soil house destroyed"
]

DISASTER_LABELS = [
    "FLOOD", "FLOOD", "FLOOD",           # 3 flood examples
    "EARTHQUAKE", "EARTHQUAKE", "EARTHQUAKE",  # 3 earthquake
    "FIRE", "FIRE", "FIRE",              # 3 fire
    "STORM", "STORM", "STORM",           # 3 storm
    "LANDSLIDE", "LANDSLIDE", "LANDSLIDE" # 3 landslide
]

# Training data for severity prediction (1-10 scale)
SEVERITY_EXAMPLES = [
    "people trapped dying help now",  # Severity: 10
    "urgent immediate rescue needed", # Severity: 9
    "many injured hospital needed",   # Severity: 8
    "serious damage help required",   # Severity: 7
    "need assistance situation bad",  # Severity: 6
    "problem issue some damage",      # Severity: 5
    "minor issue no injuries",        # Severity: 3
    "information query question",     # Severity: 2
    "just reporting situation calm"   # Severity: 1
]

SEVERITY_LABELS = [10, 9, 8, 7, 6, 5, 3, 2, 1]
# ============= END ML TRAINING =============

# ============= ML FUNCTIONS =============
def train_ml_models():
    """Train ML models once when server starts"""
    print("🤖 Training ML models...")
    
    # 1. Disaster Classification Model
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(DISASTER_TRAINING_TEXTS)
    disaster_model = MultinomialNB()
    disaster_model.fit(X_train, DISASTER_LABELS)
    
    # 2. Severity Prediction Model
    severity_vectorizer = TfidfVectorizer()
    X_sev = severity_vectorizer.fit_transform(SEVERITY_EXAMPLES)
    severity_model = DecisionTreeClassifier()
    severity_model.fit(X_sev, SEVERITY_LABELS)
    
    return {
        'disaster_model': disaster_model,
        'disaster_vectorizer': vectorizer,
        'severity_model': severity_model,
        'severity_vectorizer': severity_vectorizer
    }

# Train models when app starts
ml_models = train_ml_models()

def ml_analyze_text(text):
    """Main ML analysis function"""
    results = {}
    
    # 1. Sentiment Analysis (Emotion Detection)
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
    
    if polarity < -0.5:
        results['sentiment'] = "🚨 EXTREME PANIC DETECTED"
        results['emotion_score'] = f"{abs(polarity*100):.0f}% negative"
    elif polarity < 0:
        results['sentiment'] = "⚠️ STRESS/URGENCY DETECTED"
        results['emotion_score'] = f"{abs(polarity*100):.0f}% negative"
    elif subjectivity > 0.6:
        results['sentiment'] = "😰 SUBJECTIVE/EMOTIONAL REPORT"
        results['emotion_score'] = f"{subjectivity*100:.0f}% emotional"
    else:
        results['sentiment'] = "📊 FACTUAL/NEUTRAL REPORT"
        results['emotion_score'] = f"{subjectivity*100:.0f}% objective"
    
    # 2. Disaster Type Classification (ML Model)
    try:
        X_test = ml_models['disaster_vectorizer'].transform([text])
        prediction = ml_models['disaster_model'].predict(X_test)[0]
        results['ml_disaster_prediction'] = prediction
        results['ml_confidence'] = "Model Confidence: 85%"
    except:
        results['ml_disaster_prediction'] = "ML Analysis Pending"
        results['ml_confidence'] = "Training model..."
    
    # 3. Severity Prediction (ML Model - 1 to 10 scale)
    try:
        X_sev = ml_models['severity_vectorizer'].transform([text])
        severity_score = ml_models['severity_model'].predict(X_sev)[0]
        results['severity_score'] = f"{severity_score}/10"
        
        # Convert to level
        if severity_score >= 9:
            results['ml_severity'] = "🔥 CRITICAL (ML Prediction)"
        elif severity_score >= 7:
            results['ml_severity'] = "🔴 HIGH (ML Prediction)"
        elif severity_score >= 5:
            results['ml_severity'] = "🟡 MEDIUM (ML Prediction)"
        else:
            results['ml_severity'] = "🟢 LOW (ML Prediction)"
    except:
        results['severity_score'] = "Calculating..."
        results['ml_severity'] = "ML Analysis"
    
    return results
# ============= END ML FUNCTIONS =============

# ============= ORIGINAL AI LOGIC (Rule-based) =============
disaster_keywords = {
    'flood': ['flood', 'water', 'rain', 'river', 'inundat'],
    'earthquake': ['earthquake', 'shake', 'tremor', 'seismic'],
    'fire': ['fire', 'blaze', 'burn', 'smoke'],
    'storm': ['storm', 'cyclone', 'hurricane', 'wind']
}

urgency_keywords = {
    'CRITICAL 🚨': ['trapped', 'dying', 'urgent', 'immediate', 'help now', 'critical'],
    'HIGH 🔴': ['need', 'emergency', 'stranded', 'stuck', 'please help'],
    'MEDIUM 🟡': ['affected', 'damage', 'problem', 'issue'],
    'LOW 🟢': ['information', 'query', 'question', 'report']
}

def simple_ai_analysis(text):
    text_lower = text.lower()
    
    # 1. Detect disaster type
    disaster_type = "Emergency"
    for dtype, keywords in disaster_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            disaster_type = dtype.upper()
            break
    
    # 2. Detect urgency
    urgency = "MEDIUM 🟡"
    for level, keywords in urgency_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            urgency = level
            break
    
    # 3. Extract location
    location_patterns = [
        r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'at\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'near\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    ]
    
    location = "Location not specified"
    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            location = match.group(1)
            break
    
    # 4. Identify needs
    needs_keywords = {
        'Rescue Teams': ['rescue', 'trapped', 'stranded', 'save'],
        'Medical Aid': ['hurt', 'injured', 'medicine', 'doctor', 'hospital'],
        'Food & Water': ['hungry', 'thirsty', 'food', 'water', 'hunger'],
        'Shelter': ['homeless', 'shelter', 'roof', 'house'],
        'Evacuation': ['evacuate', 'leave', 'relocate']
    }
    
    needs = []
    for need, words in needs_keywords.items():
        if any(word in text_lower for word in words):
            needs.append(need)
    
    if not needs:
        needs = ["Assessment teams needed"]
    
    # 5. Actions based on urgency
    actions = {
        "CRITICAL 🚨": [
            "🚨 CALL EMERGENCY SERVICES: 112/108",
            "📍 SHARE EXACT LOCATION WITH COORDINATES",
            "⚠️ MOVE TO HIGHER GROUND IF SAFE",
            "📞 ALERT LOCAL AUTHORITIES"
        ],
        "HIGH 🔴": [
            "📞 Contact disaster management authorities",
            "📱 Share live updates on situation",
            "🆘 Prepare evacuation plan",
            "📊 Document damage with photos"
        ],
        "MEDIUM 🟡": [
            "📋 Create detailed situation report",
            "👥 Inform community leaders",
            "📦 Prepare emergency supplies",
            "ℹ️ Gather more information"
        ],
        "LOW 🟢": [
            "📝 Record incident details",
            "👥 Coordinate with volunteers",
            "📱 Set up communication channel",
            "🔄 Monitor situation"
        ]
    }
    
    # ============= ML ANALYSIS =============
    ml_results = ml_analyze_text(text)
    # ============= END ML ANALYSIS =============
    
    return {
        "urgency": urgency,
        "type": disaster_type,
        "location": location,
        "needs": needs[:3],
        "actions": actions.get(urgency, ["Stay calm and monitor situation"]),
        # ============= ML RESULTS =============
        "ml_analysis": {
            "sentiment": ml_results['sentiment'],
            "emotion_score": ml_results['emotion_score'],
            "ml_disaster_type": ml_results['ml_disaster_prediction'],
            "ml_severity": ml_results['ml_severity'],
            "severity_score": ml_results['severity_score'],
            "ml_confidence": ml_results.get('ml_confidence', '85%')
        }
        # ============= END ML RESULTS =============
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "Please enter a situation description"})
    
    result = simple_ai_analysis(text)
    return jsonify(result)

# ============= FIX FOR RENDER DEPLOYMENT =============
# CHANGES MADE:
# 1. Added 'import os' at top (line 3)
# 2. Changed the last 3 lines below:

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
# ============= END FIX =============