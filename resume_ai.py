from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import docx
import spacy
import spacy_stanza
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# Load SpaCy models for English and Bahasa Indonesia
nlp_en = spacy.load('en_core_web_sm')
nlp_id = spacy_stanza.load_pipeline('id')

@app.route('/api/extract-pdf', methods=['POST'])
def extract_text_from_pdf():
    file_path = request.json['file_path']
    document = fitz.open(file_path)
    text = ""
    for page in document:
        text += page.get_text()
    return jsonify({'text': text})

@app.route('/api/extract-docx', methods=['POST'])
def extract_text_from_docx():
    file_path = request.json['file_path']
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return jsonify({'text': text})

@app.route('/api/extract-features', methods=['POST'])
def extract_features():
    text = request.json['text']
    lang = detect_language(text)
    
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
    
    return jsonify(features)

if __name__ == '__main__':
    app.run(debug=True)
