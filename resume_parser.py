import fitz  # PyMuPDF
import docx
import spacy
import spacy_stanza
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_score, recall_score, accuracy_score, f1_score
from sklearn.model_selection import KFold

# Load SpaCy models for English and Bahasa Indonesia
nlp_en = spacy.load('en_core_web_sm')
nlp_id = spacy_stanza.load_pipeline('id')

# Language detection function (dummy implementation)
def detect_language(text):
    # Simple language detection based on presence of certain words
    if any(word in text.lower() for word in ['the', 'and', 'is']):
        return 'en'
    else:
        return 'id'

# Extract text from PDF
def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)
    text = ""
    for page in document:
        text += page.get_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Enhanced feature extraction using SpaCy for multiple languages
def extract_features(text, lang='en'):
    if lang == 'en':
        doc = nlp_en(text)
    else:
        doc = nlp_id(text)
    
    features = {
        "job_title": [],
        "experience_years": 0,
        "education_level": [],
        "certifications": [],
        "location": ""
    }

    for ent in doc.ents:
        if lang == 'en':
            if ent.label_ == "JOB_TITLE":
                features["job_title"].append(ent.text)
            elif ent.label_ == "EXPERIENCE":
                features["experience_years"] = int(ent.text.split()[0])
            elif ent.label_ == "EDUCATION":
                features["education_level"].append(ent.text)
            elif ent.label_ == "CERTIFICATION":
                features["certifications"].append(ent.text)
            elif ent.label_ == "GPE":  # GPE (Geopolitical Entity) for location
                features["location"] = ent.text
        else:
            if ent.type == "JobTitle":
                features["job_title"].append(ent.text)
            elif ent.type == "Experience":
                features["experience_years"] = int(ent.text.split()[0])
            elif ent.type == "Education":
                features["education_level"].append(ent.text)
            elif ent.type == "Certification":
                features["certifications"].append(ent.text)
            elif ent.type == "GPE":  # GPE (Geopolitical Entity) for location
                features["location"] = ent.text
    
    return features

# Sample data
documents = [
    "John Doe\nSoftware Engineer\n5 years experience\nBachelor's Degree in Computer Science\nCertified Java Developer\nLocated in New York",
    "Jane Smith\nData Scientist\n3 years experience\nMaster's Degree in Data Science\nCertified Data Analyst\nLocated in San Francisco",
    "Alice Brown\nMechanical Engineer\n2 years experience\nBachelor's Degree in Mechanical Engineering\nCertified SolidWorks Professional\nLocated in Los Angeles",
    "Bob Johnson\nMarketing Specialist\n4 years experience\nBachelor's Degree in Marketing\nCertified Digital Marketing Professional\nLocated in Chicago",
    "Budi Santoso\nInsinyur Perangkat Lunak\n5 tahun pengalaman\nSarjana Teknik Informatika\nBerlisensi Pengembang Java\nBerlokasi di Jakarta",
    "Siti Nurhaliza\nIlmuwan Data\n3 tahun pengalaman\nMagister Sains Data\nBerlisensi Analis Data\nBerlokasi di Bandung"
]
labels = [1, 0, 1, 0, 1, 0]  # 1 for match, 0 for non-match

# Detect language and extract features from all documents
extracted_features = [extract_features(doc, detect_language(doc)) for doc in documents]

# Convert features to a format suitable for machine learning
def features_to_vector(features):
    # This is a simplified example, in practice, you would need a more complex method
    return [
        len(features["job_title"]),
        features["experience_years"],
        len(features["education_level"]),
        len(features["certifications"]),
        1 if features["location"] else 0
    ]

X = [features_to_vector(f) for f in extracted_features]
y = labels

# Cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Initialize lists to store evaluation metrics
precision_scores = []
recall_scores = []
accuracy_scores = []
f1_scores = []

# Perform cross-validation
for train_index, test_index in kf.split(X):
    X_train, X_test = [X[i] for i in train_index], [X[i] for i in test_index]
    y_train, y_test = [y[i] for i in train_index], [y[i] for i in test_index]

    # Logistic Regression Model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluate metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Append scores to lists
    precision_scores.append(precision)
    recall_scores.append(recall)
    accuracy_scores.append(accuracy)
    f1_scores.append(f1)

# Calculate average scores
avg_precision = sum(precision_scores) / len(precision_scores)
avg_recall = sum(recall_scores) / len(recall_scores)
avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
avg_f1 = sum(f1_scores) / len(f1_scores)

# Print average scores
print("Average Precision:", avg_precision)
print("Average Recall:", avg_recall)
print("Average Accuracy:", avg_accuracy)
print("Average F1 Score:", avg_f1)

# Print individual scores for each fold (optional for detailed analysis)
print("\nIndividual Scores for Each Fold:")
for i in range(len(precision_scores)):
    print(f"Fold {i+1}: Precision={precision_scores[i]}, Recall={recall_scores[i]}, Accuracy={accuracy_scores[i]}, F1 Score={f1_scores[i]}")

# Print classification report for the last fold (optional for detailed analysis)
print("\nClassification Report for the Last Fold:")
print(classification_report(y_test, y_pred))
